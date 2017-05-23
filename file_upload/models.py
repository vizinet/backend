from __future__ import unicode_literals
from user_profile.models import AirpactUser
from django.db import models
from PIL import Image, ImageOps, ImageDraw
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage as storage
from TwoTargetContrast import TwoTargetContrast
from datetime import datetime
import math
import os
# Create your models here.

#TODO:
class picture(models.Model):
	pic = models.ImageField(upload_to = 'pictures/') # the actual picture object
	thumbnail = models.ImageField(upload_to = 'thumbnails/', null=True, blank=True) # the small 200x200 picture object
	pictureWithCircles = models.ImageField(upload_to = 'circles/', null=True, blank=True) # copy of pic but with target cirlces drawn on
	uploaded = models.DateTimeField(default = datetime.now) # time in which the picture was taken
	description = models.TextField(default = " ", null=True) 
	user = models.ForeignKey(AirpactUser, on_delete=models.CASCADE) #user object representing who uploaded this image
	algorithmType = models.TextField(default = "near_far", null= True) # should only be "near_far" or "object_sky" and tells which algorithm to use to compute VR
	vr = models.FloatField(null=False, default=0) # user supplied estimation of what they think VR is
	vrUnits = models.CharField(null = True, default = 'K', max_length = 1) # should only ever be "K" or "M" defining kilometers and miles and is used for display purposes only, everything is converted to KM on upload
	objectSkyVr = models.FloatField(null = True, default = 0) # storage for object sky vr
	twoTargetContrastVr = models.FloatField(null=True,default=0)# storage for near far vr
	highColor = models.IntegerField(null=False , default=0) #"far object or sky" color selected from app, we don't need this anymore probably
	highX = models.FloatField(null=False, default=0) #center of square to be sampled for the far target or the sky
	highY= models.FloatField(null=False, default=0) # ""
	farTargetDistance = models.FloatField(null = True, default = 0) #distance to far target or sky
	nearTargetDistance = models.FloatField(null = True, default = 0) # distance to the near target
	lowColor = models.IntegerField(null=False, default=0) # color of the near target
	lowX = models.FloatField(null=False, default=0) #center of selection square for the near target
	lowY = models.FloatField(null=False,default=0) #""
	geoX = models.FloatField(default = 46.7298) #GPS locations of where picture was taken, defaults to pullman
	geoY = models.FloatField(default =  -117.181738)

	radiusHigh = models.FloatField(null=True)
	radiusLow = models.FloatField(null = True)

	def generateThumbnail(self):
		thumbnailSize = (200,200)

		#see what kind of file we are dealing with 
		if self.pic.name.endswith(".jpg"):
			pilImageType = "jpeg"
			fileExtension = "jpg"
			djangoType = 'image/jpeg'
		elif self.pic.name.endswith(".png"):
			pilImageType = "png"
			fileExtension = "png"
			djangoType = 'image/png'

		#open big picture into PIL
		self.pic.seek(0)
		OriginalImage = Image.open(StringIO(self.pic.read()))
		OriginalImage.thumbnail(thumbnailSize, Image.ANTIALIAS)
		tempHandle = StringIO()
		background = Image.new('RGBA', thumbnailSize, (255,255,255,0))
		background.paste(OriginalImage,((thumbnailSize[0] - OriginalImage.size[0]) / 2, (thumbnailSize[1] - OriginalImage.size[1]) / 2))
		
		background.save(tempHandle, pilImageType)


		tempHandle.seek(0)
		suf = SimpleUploadedFile(os.path.split(self.pic.name)[-1],tempHandle.read(),content_type = djangoType)
		self.thumbnail.save('%s.%s'%(os.path.splitext(suf.name)[0],fileExtension), suf, save=False)


	# creates a copy of the image with the circle points drawn on them 
	def generateCircles(self):

		#see what kind of file we are dealing with 
		if self.pic.name.endswith(".jpg"):
			pilImageType = "jpeg"
			fileExtension = "jpg"
			djangoType = 'image/jpeg'
		elif self.pic.name.endswith(".png"):
			pilImageType = "png"
			fileExtension = "png"
			djangoType = 'image/png'

		#get the bounding boxes for each of the circles
		highCords = [(self.highX-int(math.ceil(math.sqrt(20000))), self.highY-int(math.ceil(math.sqrt(20000)))),(self.highX+int(math.ceil(math.sqrt(20000))), self.highY+int(math.ceil(math.sqrt(20000))))]
		lowCords = [(self.lowX-int(math.ceil(math.sqrt(20000))), self.lowY-int(math.ceil(math.sqrt(20000)))),(self.lowX+int(math.ceil(math.sqrt(20000))), self.lowY+int(math.ceil(math.sqrt(20000))))]

		#open original image
		self.pic.seek(0)
		OriginalImage = Image.open(StringIO(self.pic.read()))

		#open a new drawing object with our image
		editor = ImageDraw.Draw(OriginalImage)

		#draw the cricles
		for i in range(0,10):
			outline_value = (0,0,0)
			if i > 5:
				outline_value = (255,255,255)
			editor.ellipse([highCords[0][0]-i,highCords[0][1]-i,highCords[1][0]+i,highCords[1][1]+i], outline=outline_value)
			editor.ellipse([lowCords[0][0]-i,lowCords[0][1]-i,lowCords[1][0]+i,lowCords[1][1]+i], outline=outline_value)

		#get rid of the drawer
		del editor

		#create a place to hold the new image for a second
		tempHandle = StringIO()

		#write the image to the handler
		OriginalImage.save(tempHandle, pilImageType)
		tempHandle.seek(0)

		#save the image
		suf = SimpleUploadedFile(os.path.split(self.pic.name)[-1],tempHandle.read(),content_type=djangoType)
		self.pictureWithCircles.save('%s.%s'%(os.path.splitext(suf.name)[0],fileExtension), suf, save=False)
	
	def findTwoTargetContrastVr(self):
		self.pic.seek(0)
		#open image
		image = Image.open(StringIO(self.pic.read()))

		#print("Have the image.")

		#convert to RGB values for each pixel
		pixelData = image.convert('RGB')

		#set up containers for red green and blue for each target
		hRed = []
		hGreen = []
		hBlue = []
		lRed = []
		lGreen = []
		lBlue = []

		# 
		newHX = int(self.highX)
		newHY = int(self.highY)
		newLX = int(self.lowX)
		newLY = int(self.lowY)
		radius = int(self.radiusLow)

		# The radius must be the smaller of the two radiuss
		if(int(self.radiusHigh) < radius):
			radius = int(self.radiusHigh)

		if newHX < 0:
			newHX  = 0;
		if newHY < 0:
			newHY = 0;
		if newLX < 0:
			newLX = 0;
		if newLY < 0:
			newLY = 0;

		#process high or "Far" target first
		for x in range(newHX, newHX + radius*2):
			for y in range(newHY,newHY+radius*2):
				try:
					R,G,B = pixelData.getpixel((x,y))
					hRed.append(R)
					hGreen.append(G)
					hBlue.append(B)
				except Exception:
					print("Out of bounds when getting pixel data")


		#do the same for the low or "close" target
		for x in range(newLX, newLX+radius*2):
			for y in range(newLY, newLY+radius*2):
				try:
					R,G,B = pixelData.getpixel((x,y))
					lRed.append(R)
					lGreen.append(G)
					lBlue.append(B)
				except Exception:
					print("Out of bounds at x:" + str(x) + "y:"+str(y))

		#now we need to run the function 3 times one for each color band then average them together
		vrR = TwoTargetContrast(hRed,lRed,self.farTargetDistance,self.nearTargetDistance)
		vrG = TwoTargetContrast(hGreen,lGreen,self.farTargetDistance,self.nearTargetDistance)
		vrB = TwoTargetContrast(hBlue,lBlue,self.farTargetDistance,self.nearTargetDistance)

		self.twoTargetContrastVr = (abs((vrR[0] + vrG[0] + vrB[0]) / 3))
	
	#escapes special characters that can affect javascript
	def cleanDescription(self):
		self.description = self.description.replace("\'", "\\\'").replace('\"',"\\\"").replace("\\","\\\\").replace("\n","")
	
	def convertToKM(self):
		if self.vrUnits == 'M':
			self.farTargetDistance *= 1.60934
			self.nearTargetDistance *= 1.60934
			self.skyDistance *= 1.60934

	def save(self):
		
		self.convertToKM()
		self.cleanDescription()
		self.generateCircles()
		self.generateThumbnail()

		try:
			if self.algorithmType == "near_far":
				self.findTwoTargetContrastVr()
		except Exception as e:
			print("ERROR CALCULATING VR: " + e.message)
		#else:
			#self.findObjectSkyVr() // need to create this function

		super(picture,self).save()

	
	def __str__(self):
		return self.description

# We called them tags, they are really the string representation of where a picture was taken uploaded by the user
# That sounds like an intro to a movie
# I need sleep
class tag(models.Model):
	picture = models.ForeignKey(picture, on_delete=models.CASCADE)
	text = models.TextField(null=False)