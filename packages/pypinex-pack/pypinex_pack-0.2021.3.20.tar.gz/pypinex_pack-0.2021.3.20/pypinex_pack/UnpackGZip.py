



import os
import typing
import gzip
import io

from pypine import *






class UnpackGZip(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, newFileName:str = None):
		super().__init__()

		self.newFileName = newFileName
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
		return [ "file", "url" ]
	#

	def actionIfUnprocessable(self) -> EnumAction:
		return EnumAction.Warn
	#

	def processElement(self, ctx:Context, f):
		if self.newFileName:
			newFileName = self.newFileName
		else:
			if f.fileName.endswith(".gz"):
				newFileName = f.fileName[:-3]
			elif f.fileName.endswith(".tgz"):
				newFileName = f.fileName[:-4] + ".tar"
			else:
				raise Exception("Don't know how to modify file name: '{}'".format(f.fileName))

		newRelFilePath = os.path.join(f.relDirPath, newFileName)

		f = ctx.toLocalDiskFile(f)					# TODO: implement some kind of streaming! find a better solution here!

		with gzip.GzipFile(f.absFilePath, mode="rb") as stream:
			rawData = stream.read()

		fileTypeInfo = FileTypeInfo.guessFromFileName(newFileName)
		if fileTypeInfo.isText:
			rawData = rawData.decode("utf-8")

		f2 = InMemoryFile(newRelFilePath, fileTypeInfo, rawData)
		return f2
	#

#






