



import os
import typing
import io

import jk_uploadpack
import jk_typing

from pypine import *






class AddToUploadPack(AbstractProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, up:typing.Union[jk_uploadpack.Packer,None], fileGroupID:str):
		assert fileGroupID

		super().__init__()

		self.__up = up
		self.__fileGroupID = fileGroupID
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
		if self.__up:
			up = self.__up
		else:
			up = ctx.localData["uploadpack"]
			assert isinstance(up, jk_uploadpack.Packer)

		rawData = f.readBinary()
		assert rawData is not None
		assert self.__fileGroupID

		up.fileGroup(self.__fileGroupID).addStream(rawData, f.relFilePath)
	#

#






