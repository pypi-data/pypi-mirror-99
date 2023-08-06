



import os
import typing
import bz2
import io

from pypine import *






class PackBZip2(AbstractProcessor):

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
		if f.fileName.endswith(".bz2"):
			return f

		outbuf = io.BytesIO()
		with bz2.BZ2File(filename=outbuf, mode="wb", compresslevel=9) as stream:
			rawData = f.readBinary()
			stream.write(rawData)

		f2 = InMemoryFile(f.relFilePath + ".bz2", FileTypeInfo.guessFromFileName(".bz2"), outbuf.getvalue())
		return f2
	#

#






