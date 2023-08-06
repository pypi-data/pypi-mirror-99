



import os
import typing
import gzip
import io

from pypine import *






class PackGZip(AbstractProcessor):

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
		if f.fileName.endswith(".gz"):
			return f

		outbuf = io.BytesIO()
		with gzip.GzipFile(fileobj=outbuf, mode="wb", compresslevel=9) as stream:
			rawData = f.readBinary()
			stream.write(rawData)

		f2 = InMemoryFile(f.relFilePath + ".gz", FileTypeInfo.guessFromFileName(".gz"), outbuf.getvalue())
		return f2
	#

#






