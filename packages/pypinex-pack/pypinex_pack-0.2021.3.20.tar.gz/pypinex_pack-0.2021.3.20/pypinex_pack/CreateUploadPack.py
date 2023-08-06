



import os
import typing
import io

import jk_uploadpack

from pypine import *






class CreateUploadPack(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, fileName:str, compression:str = None):
		super().__init__()

		assert isinstance(fileName, str)
		assert fileName
		self.__fileName = fileName
		for c in "\\/:|":
			assert c not in fileName

		if fileName.endswith(".gz"):
			compressionFromFileName = "gz"
		elif fileName.endswith(".tgz"):
			compressionFromFileName = "gz"
		elif fileName.endswith(".xz"):
			compressionFromFileName = "xz"
		elif fileName.endswith(".txz"):
			compressionFromFileName = "xz"
		elif fileName.endswith(".bz2"):
			compressionFromFileName = "bz2"
		else:
			compressionFromFileName = None

		if compression is None:
			self.__compression = compressionFromFileName
		else:
			assert isinstance(compression, str)
			assert compression in [ "gz", "gzip", "xz", "bz2", "bzip2" ]
			self.__compression = compression
	#

	def initializeProcessing(self, ctx:Context):
		self.__tempDirPath = ctx.newTempDir()
		self.__tempFilePath = os.path.join(self.__tempDirPath, self.__fileName)

		self.__up = jk_uploadpack.Packer(self.__tempFilePath, self.__compression)

		ctx.localData["uploadpack"] = self.__up
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#






