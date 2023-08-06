


__version__ = "0.2021.3.19"



import typing

import jk_uploadpack

from .PackGZip import PackGZip
from .PackBZip2 import PackBZip2
from .PackXZ import PackXZ
from .Tar import Tar
from .UnpackGZip import UnpackGZip
from .UnpackBZip2 import UnpackBZip2
from .UnpackXZ import UnpackXZ
from .CompressUploadPack import CompressUploadPack
from .CreateUploadPack import CreateUploadPack
from .AddToUploadPack import AddToUploadPack
from .CloseUploadPack import CloseUploadPack






def gzip():
	return PackGZip()
#

def gunzip(newFileName:str = None):
	return UnpackGZip(newFileName)
#

def bzip2():
	return PackBZip2()
#

def bunzip2(newFileName:str = None):
	return UnpackBZip2(newFileName)
#

def xz():
	return PackXZ()
#

def unxz():
	return UnpackXZ()
#

def tar(fileName:str, compression:str = None):
	return Tar(fileName, compression)
#

def compressUP(fileName:str, compression:str = None):
	return CompressUploadPack(fileName, compression)
#

def createUP(fileName:str, compression:str = None):
	return CreateUploadPack(fileName, compression)
#

def closeUP():
	return CloseUploadPack()
#

def addToUP(fileGroupID:str, up:typing.Union[jk_uploadpack.Packer,None] = None):
	return AddToUploadPack(up, fileGroupID)
#



