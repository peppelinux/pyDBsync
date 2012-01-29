#import difflib
import os

# Stupid and useless code that could be changed with something more serious to compare
# the tablemaps from sqlalchemy... Consider it deprecated:
class File:
	def __init__(self, file_path, mode):
		self.file = open(file_path, mode)
		self.content = self.file.readlines()
		self.file.close()
	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.content == other.content
	def __hash__(self):
		return hash(self.content)
