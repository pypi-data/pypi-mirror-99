



import os
import typing
import lzma
import io

from pypine import *






class PackXZ(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, **kwargs):
		super().__init__()
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
		if f.fileName.endswith(".xz"):
			return f

		outbuf = io.BytesIO()
		with lzma.LZMAFile(filename=outbuf, mode="wb", format=lzma.FORMAT_XZ) as stream:
			rawData = f.readBinary()
			stream.write(rawData)

		f2 = InMemoryFile(f.relFilePath + ".xz", FileTypeInfo.guessFromFileName(".xz"), outbuf.getvalue())
		return f2
	#

#






