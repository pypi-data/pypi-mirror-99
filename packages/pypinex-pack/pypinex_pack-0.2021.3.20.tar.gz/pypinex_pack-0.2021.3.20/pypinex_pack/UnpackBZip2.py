



import os
import typing
import bz2
import io

from pypine import *






class UnpackBZip2(AbstractProcessor):

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
			if f.fileName.endswith(".bz2"):
				newFileName = f.fileName[:-4]
			elif f.fileName.endswith(".tbz2"):
				newFileName = f.fileName[:-5] + ".tar"
			else:
				raise Exception("Don't know how to modify file name: '{}'".format(f.fileName))

		newRelFilePath = os.path.join(f.relDirPath, newFileName)

		f = ctx.toLocalDiskFile(f)					# TODO: implement some kind of streaming! find a better solution here!

		with bz2.BZ2File(f.absFilePath, mode="rb") as stream:
			rawData = stream.read()

		fileTypeInfo = FileTypeInfo.guessFromFileName(newFileName)
		if fileTypeInfo.isText:
			rawData = rawData.decode("utf-8")

		f2 = InMemoryFile(newRelFilePath, fileTypeInfo, rawData)
		return f2
	#

#






