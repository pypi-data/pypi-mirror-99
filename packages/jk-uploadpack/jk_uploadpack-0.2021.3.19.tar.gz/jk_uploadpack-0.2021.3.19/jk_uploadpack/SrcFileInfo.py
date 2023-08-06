


import io
import stat
import os
import typing
import hashlib

import jk_typing
import jk_utils

from .helpers import sha256_bytesiter, file_read_blockiter






#
# This class represents a source file to store. It provides essential information about that file for storing.
#
class SrcFileInfo(object):

	__DEFAULT_MODE = jk_utils.ChModValue("rwxrwxr-x").toInt()

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, size:int, hashID:str, srcFilePath:typing.Union[str,None], mode:int, mtime:float):
		assert isinstance(size, int)
		assert size >= 0
		assert isinstance(hashID, str)
		assert hashID
		if srcFilePath is not None:
			assert isinstance(srcFilePath, str)
			assert srcFilePath
		assert isinstance(mode, int)
		assert isinstance(mtime, (int, float))

		self.mode = mode
		self.size = size
		self.mtime = mtime
		self.hashID = hashID
		self.srcFilePath = srcFilePath
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

	@staticmethod
	def fromFile(filePath:str):
		statStruct = os.lstat(filePath)
		mode = statStruct.st_mode
		size = statStruct.st_size
		uid = statStruct.st_uid
		gid = statStruct.st_gid
		mtime = float(statStruct.st_mtime)

		hashAlg = hashlib.sha256()
		with open(filePath, "rb") as fin:
			for chunk in iter(lambda: fin.read(4096), b""):
				hashAlg.update(chunk)
		hashDigest = hashAlg.hexdigest()
		hashID = "sha256:{}:{}".format(hashDigest, size)

		return SrcFileInfo(size, hashID, filePath, mode, mtime)
	#

	@staticmethod
	def fromRaw(raw:typing.Union[bytes,bytearray,io.BytesIO]):
		mode = SrcFileInfo.__DEFAULT_MODE
		size = len(raw)
		uid = 1000
		gid = 1000
		mtime = 0

		hashAlg = hashlib.sha256()
		hashAlg.update(raw)
		hashDigest = hashAlg.hexdigest()
		hashID = "sha256:{}:{}".format(hashDigest, size)

		return SrcFileInfo(size, hashID, None, mode, mtime)
	#

#







