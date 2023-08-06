



import os
import typing
import io
import tarfile

from pypine import *






class Tar(AbstractProcessor):

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
			if compression == "bzip2":
				compression = "bz2"
			if compression == "gzip":
				compression = "gz"
			self.__compression = compression
	#

	def initializeProcessing(self, ctx:Context):
		self.__tempDirPath = ctx.newTempDir()
		self.__tempFilePath = os.path.join(self.__tempDirPath, self.__fileName)

		self.__t = tarfile.open(self.__tempFilePath, ("w:" + self.__compression) if self.__compression else "w")
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

	def processableDataTypes(self) -> list:
		return [ "file" ]							# TODO: support URLs as well
	#

	def actionIfUnprocessable(self) -> EnumAction:
		return EnumAction.Fail
	#

	def processElement(self, ctx:Context, f):
		f = ctx.toLocalDiskFile(f)					# TODO: make this unnecessary!

		tarInfo = tarfile.TarInfo(f.relFilePath)
		tarInfo.size = f.getFileSize()
		tarInfo.mtime = f.getTimeStamp()
		tarInfo.uid = f.getUID()
		tarInfo.gid = f.getGID()
		tarInfo.mode = f.getMode()

		with open(f.absFilePath, "rb") as fin:
			self.__t.addfile(tarInfo, fin)
	#

	def processingCompleted(self, ctx:Context):
		self.__t.close()

		f2 = DiskFile.fromFile(
			os.path.dirname(self.__tempFilePath),
			self.__tempFilePath,
		)

		ctx.printVerbose(self, "Archive created: " + f2.absFilePath)

		return f2
	#

#






