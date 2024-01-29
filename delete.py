import os, sys

for filename in os.listdir(os.path.dirname(os.path.abspath(__file__))):
		base_file, ext = os.path.splitext(filename)
		if ext == ".bin":
			os.remove(filename)
		elif ext == ".pem":
			os.remove(filename)
		elif ext == ".db":
			os.remove(filename)
		elif ext == ".session-journal":
			os.remove(filename)
		elif ext == ".session":
			os.remove(filename)
			

