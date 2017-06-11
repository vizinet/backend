# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.

"""
from __future__ import unicode_literals

# Django libraries
from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage as storage

# Custom Django
from user_profile.models import AirpactUser
from TwoTargetContrast import TwoTargetContrast

# Other
from PIL import Image, ImageOps, ImageDraw
import datetime
import math
import os
from cStringIO import StringIO

# The picture model
class Picture(models.Model):

	# The image itself
	image = models.ImageField(upload_to = 'pictures/')
	
	# Thumbnail of the picture
	thumbnail = models.ImageField(upload_to = 'thumbnails/', null=True, blank=True) # the small 200x200 picture object
	
	# Time of upload
	uploadTime = models.DateTimeField(default = datetime.datetime.now)
	
	# Description of the picture
	description = models.TextField(default = " ", null=True) 
	
	# User who submitted the picture
	user = models.ForeignKey(AirpactUser, on_delete=models.CASCADE) #user object representing who uploaded this image
	
	# Which algorithm are we using? Defaults to AlgorithmOne
	algorithmType = models.TextField(default = "AlgorithmOne", null= False)
	
	# User Estimated visual range of the picture
	eVisualRange = models.FloatField(null=False, default=0)
	
	# Units either in kilometers or miles
	vrUnits = models.CharField(null = True, default = 'K', max_length = 1) 

	#GPS locations of where picture was taken, defaults to pullman
	geoX = models.FloatField(default = 46.7298) 

	geoY = models.FloatField(default =  -117.181738)
	
	# Scale image to be a thumbnail
	def generateThumbnail(self):
		thumbnailSize = (200,200)

		# see what kind of file we are dealing with 
		if self.image.name.endswith(".jpg"):
			pilImageType = "jpeg"
			fileExtension = "jpg"
			djangoType = 'image/jpeg'
		elif self.image.name.endswith(".png"):
			pilImageType = "png"
			fileExtension = "png"
			djangoType = 'image/png'

		# open big picture into PIL
		self.image.seek(0)
		OriginalImage = Image.open(StringIO(self.image.read()))
		OriginalImage.thumbnail(thumbnailSize, Image.ANTIALIAS)
		tempHandle = StringIO()
		background = Image.new('RGBA', thumbnailSize, (255,255,255,0))
		background.paste(OriginalImage,((thumbnailSize[0] - OriginalImage.size[0]) / 2, (thumbnailSize[1] - OriginalImage.size[1]) / 2))
		background.save(tempHandle, pilImageType)
		tempHandle.seek(0)
		suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],tempHandle.read(),content_type = djangoType)
		self.thumbnail.save('%s.%s'%(os.path.splitext(suf.name)[0],fileExtension), suf, save=False)

	# Escapes special characters that can affect javascript
	def cleanDescription(self):
		self.description = self.description.replace("\'", "\\\'").replace('\"',"\\\"").replace("\\","\\\\").replace("\n","")
	
	# Convert miles to KM
	def convertToKM(self):
		if self.vrUnits == 'M':
			self.farTargetDistance *= 1.60934
			self.nearTargetDistance *= 1.60934
			self.skyDistance *= 1.60934

	# Override save
	def save(self):
		self.convertToKM()
		self.cleanDescription()
		self.generateThumbnail()
		super(Picture, self).save()

	
	def __str__(self):
		return self.description

# 
class Tag(models.Model):
	picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
	text = models.TextField(null=False)


# We have done a very poor job of naming our algorithms. 
# This algorithm computes the visual range for two targets in one image
class AlgorithmOne(models.Model):

	# Foreign key reference to picture
	picture = models.ForeignKey(Picture, unique = True, on_delete=models.CASCADE)
	
	# Our calculated visual range
	calculatedVisualRange = models.FloatField(null=True, default=0)

	# X value for the far target
	farX = models.FloatField(null=False, default=0) 

	# Y value for the far target
	farY= models.FloatField(null=False, default=0)

	# X value for the near target
	nearX = models.FloatField(null=False, default=0 )

	# Y Value for the near target
	nearY = models.FloatField(null=False, default=0)

	farRadius = models.FloatField(null=True)
	
	nearRadius = models.FloatField(null = True)

	# Distance to far target
	farDistance = models.FloatField(null = True, default = 0)

	# Distance to near target
	nearDistance = models.FloatField(null = True, default = 0)

	
	# Find and assign the visual range based off the given picture object
	def findTwoTargetContrastVr(self):
		self.picture.image.seek(0)
		
		# Open image
		image = Image.open(StringIO(self.picture.image.read()))

		# Convert to RGB values for each pixel
		pixelData = image.convert('RGB')

		# Set up containers for red green and blue for each target
		hRed = []
		hGreen = []
		hBlue = []
		lRed = []
		lGreen = []
		lBlue = []

		newHX = int(self.farX)
		newHY = int(self.farY)
		newLX = int(self.nearX)
		newLY = int(self.nearY)
		radius = int(self.nearRadius)

		# The radius must be the smaller of the two radiuss
		if(int(self.farRadius) < radius):
			radius = int(self.farRadius)

		# No negative values
		if newHX < 0:
			newHX  = 0;
		if newHY < 0:
			newHY = 0;
		if newLX < 0:
			newLX = 0;
		if newLY < 0:
			newLY = 0;

		# Process high or "Far" target first
		for x in range(newHX, newHX + radius*2):
			for y in range(newHY,newHY+radius*2):
				try:
					R,G,B = pixelData.getpixel((x,y))
					hRed.append(R)
					hGreen.append(G)
					hBlue.append(B)
				except Exception:
					print("Out of bounds when getting pixel data")

		# do the same for the low or "close" target
		for x in range(newLX, newLX+radius*2):
			for y in range(newLY, newLY+radius*2):
				try:
					R,G,B = pixelData.getpixel((x,y))
					lRed.append(R)
					lGreen.append(G)
					lBlue.append(B)
				except Exception:
					print("Out of bounds at x:" + str(x) + "y:"+str(y))

		# Now we need to run the function 3 times one for each color band then average them together
		vrR = TwoTargetContrast(hRed,lRed,self.farTargetDistance,self.nearTargetDistance)
		vrG = TwoTargetContrast(hGreen,lGreen,self.farTargetDistance,self.nearTargetDistance)
		vrB = TwoTargetContrast(hBlue,lBlue,self.farTargetDistance,self.nearTargetDistance)

		self.twoTargetContrastVr = (abs((vrR[0] + vrG[0] + vrB[0]) / 3))

	# Override the save function for AlgorithmOne
	def save(self):
		try:
			self.findTwoTargetContrastVr()
		except Exception as e:
			print("ERROR CALCULATING VR: " + e.message)

		super(Picture, self).save()