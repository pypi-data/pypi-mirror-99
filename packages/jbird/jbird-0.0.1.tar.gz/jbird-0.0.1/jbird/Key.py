import os
import hashlib
from .Jbird import Jbird


class Key(Jbird):

	# name and full path to the keys file
	file = '__keys.bin'

	# lengths of key attributes (in bytes)
	hash_len, pos_len, vol_len = 40, 5, 5
	chunk_len = hash_len, pos_len, vol_len

	# set variables, create directory and files
	def __init__(self):
		self._prepare()

		# create keys file if not exists
		if not os.path.isfile(os.path.join(self.path, self.file)):
			open(os.path.join(self.path, self.file), 'w').close()

	# return hash of the string in bytes (!)
	def hash(self, txt: str) -> bytes:
		txt_bytes = str.encode(txt)
		hash_obj = hashlib.sha1(txt_bytes)
		hash_str = hash_obj.hexdigest()
		hash_bytes = str.encode(hash_str)
		return hash_bytes

	# insert a new chunk and shift others toward the end of file
	def push(self, pos: int) -> bool:
		pass

	# delete a chunk and shift others backward to the start of file
	def pop(self, pos: int) -> bool:
		pass

	# write a chunk
	def write(self, chunk: bytes, pos: int) -> bool:
		with open(os.path.join(self.path, self.file), 'r+b') as f:
			f.seek(pos)
			f.write(chunk)
		return True

	# read a chunk
	def read(self, pos: int) -> bytes:
		pass

	def k(self):
		print('key')
		self.j()
