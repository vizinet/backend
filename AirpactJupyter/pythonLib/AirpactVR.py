'''
This is an airpact fire visual range module. THe purpose of this module is to read visual range data for development.
Various images are inputted to the server for analysis. This module is meant to access that data in a user friendly manner.

-accepts lamda so you may return picture data in prefered format.
-may modify the directory.
-can either stream the data one at a time, or import all.
'''

import numpy
from os import listdir

_defaultImageFolder = '/home/admin/website/AirpactJupyter/pythonLib/defaultVisualRangeDataLocation' #to change default folder the module uses, change value here

#mutilates fileNms
def _fromRt(fileNms, RtDir):
    for a in range(len(fileNms)):
        fileNms[a] = RtDir + "/" + fileNms[a]
    return fileNms

def GetDefaultFolder():
    '''
    returns the default folder the images are retrieved from.
    This default position may be changed permanently by editing the modules source code.
    :return: string
    '''
    return _defaultImageFolder

def ReturnFileName(img):
    '''
    to be used as the lambda function if you just want the files names instead of processed results.
    :param img:
    :return:
    '''
    return img

def PicList(imageFolder = None, processFunc = None, mlen=99999999999999):
    '''
    Returns entire visual range data transformed using the processFunc.
    :param imageFolder: image folder location, defaults to default location
    :param processFunc: optional lambda function. Defaults to returnFileName
    :param mlen: num of images, defaults to all images.
    :return:
    '''
    if imageFolder == None:
        imageFolder = _defaultImageFolder
    else:
        imageFolder = imageFolder
    if processFunc == None:
        processFunc = ReturnFileName
    else:
        processFunc = processFunc
    list = numpy.array(listdir(imageFolder), dtype=object)
    list = _fromRt(list, imageFolder)
    pos = 0
    if mlen > len(list):
        mlen = len(list)
    while pos < mlen:
        list[pos] = processFunc(list[pos])
        pos += 1
    return list

class PicStream:
    '''
    visStream returns items within a selected folder in a usable format one at a time.
    '''
    def __init__(self, imageFolder = None, processFunc = None):
        '''
        initializes the stream.
        :param imageFolder: file location: defaults to the default folder, defines where the image files are stored.
        :param processFunc: lambda function: the process the images are put through before returning. Defaults to returning filename
        '''
        if imageFolder == None:
            self.imageFolder = _defaultImageFolder
        else:
            self.imageFolder = imageFolder
        if processFunc == None:
            self.processFunc = ReturnFileName
        else:
            self.processFunc = processFunc

        self._list =  numpy.array(listdir(self.imageFolder),dtype=object)
        self._list = _fromRt(self._list, self.imageFolder)
        self.len = len(self._list)
        self.pos = 0

    def next(self):
        '''
        gets the next file and processes it using the lambda
        :return:
        '''
        if self.pos < len(self._list):
            tmp = self.processFunc(self._list[self.pos])
            #print(str(tmp) + '\t' + str(self.pos) + "\t")
            self.pos += 1
            return tmp
        return None
