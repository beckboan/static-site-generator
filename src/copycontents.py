import os
import shutil

def copy(src, dst):
	if os.path.exists(dst):
		raise ValueError("Destination already exists")
	if not os.path.exists(src):
		raise ValueError("Source does not exist")
	if not os.path.isdir(src):
		raise ValueError("Source is not a directory")
	os.mkdir(dst)
	#Recursively copy all files and directories
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d)
		else:
			shutil.copy2(s, d)
	
	

