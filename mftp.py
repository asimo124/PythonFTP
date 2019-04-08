#!/usr/bin/python

import os, sys
import glob, re
import ftplib

class MFTP:





	def __init__(self):
		self.local_path = 'C:\\Users\\alex\\'
		self.is_connected = False

	def parseCommand(self, command):
		commandArr = command.split()
		if commandArr[0] == "open":
		
			if len(commandArr) == 2:
				self.open(commandArr[1], '', '')
			else:
				#         host,          username,      password
				self.open(commandArr[1], commandArr[2], commandArr[3])
		elif commandArr[0] == "ls":
			if (self.is_connected == False):
				print("You are not connected to any host")
				return 0
			self.list()
			return 1
		elif commandArr[0] == "cd":
			if (self.is_connected == False):
				print("You are not connected to any host")
				return 0
			self.changeDir(commandArr[1])
			return 1
		elif commandArr[0] == "put":
			if (self.is_connected == False):
				print("You are not connected to any host")
				return 0
			self.putFile(commandArr[1])
		elif commandArr[0] == "get":
			if (self.is_connected == False):
				print("You are not connected to any host")
				return 0
			self.getFile(commandArr[1])
		elif commandArr[0] == "pwd":
			if (self.is_connected == False):
				print("You are not connected to any host")
				return 0
			print(self.FTP.pwd())
			return 1
		elif commandArr[0] == "lls":
			self.listLocal()
		elif commandArr[0] == "lcd":
			self.changeLocalDir(commandArr[1])
		elif commandArr[0] == "lpwd":
			print(self.local_path)
			
	def open(self, host, username, password):
		if host == '247':
			try :
				self.FTP = ftplib.FTP('71.40.14.247', 'alextest', 'gortex!22')
			except ftplib.all_errors as e:
				print("Could not connect: " + str(e))
				return 0
			self.is_connected = True
			return 1
		else:
			try :
				self.FTP = ftplib.FTP(host, username, password)
			except ftplib.all_errors as e:
				print("Could not connect: " + str(e))
				return 0
			self.is_connected = True
			return 1
						
	def list(self):
		self.FTP.retrlines('LIST')
		
	def listLocal(self):
		for f in os.listdir(self.local_path):
			if os.path.isdir(os.path.join(self.local_path, f)):
				print("<dir> " + f)
			else:
				print("----- " + f)
		
	def changeDir(self, dir):
		if not self.is_directory(dir):
			print("That is not a valid directory")
			return -1
		if ".." in dir:
			cd_path = dir.split('/')
			j = 1
			lastCD = len(cd_path)
			new_path = self.FTP.pwd()
			k = 0
			pathsArr = new_path.split('/')
			for path in pathsArr:
				if path.strip() != "":
					k = k + 1
			paths_count = k
			for get_cd in cd_path:
				if j == paths_count + 1:
					break
				if get_cd == "..":
					pathsArr = new_path.split('/')
					i = 0
					use_new_path = ''
					lastArr = len(pathsArr)
					for path in pathsArr:
						if path.strip() != "":
							if i < lastArr - 1:
								if use_new_path == '':
									use_new_path = path
								else:
									use_new_path += "/" + path
						i = i + 1
					new_path = "/" + use_new_path
					j = j + 1	
			try:
				self.FTP.cwd(new_path)
			except ftplib.all_errors as e :
				print("Remote directory " + new_path + " does not exist")
		else:
			try:
				self.FTP.cwd(self.FTP.pwd() + "/" + dir)
			except ftplib.all_errors as e :
				missing_dir = (self.FTP.pwd() + "/" + dir) if (self.FTP.pwd() != "/") else ("/" + dir) 
				print("Remote directory " + missing_dir + " does not exist")
		return 1
			
	def putFile(self, filePut):
		file_path_to_put = self.local_path + "\\" + filePut
		file_to_put = filePut
		ext = os.path.splitext(file_to_put)[1]
		if ext in (".txt", ".htm", ".html"):
			self.FTP.storlines("STOR " + file_to_put, open(file_path_to_put))
		else:
			self.FTP.storbinary("STOR " + file_to_put, open(file_path_to_put, "rb"), 1024)
		return 1	
		
	def getFile(self, fileGet):
		filename = fileGet
		local_filename = self.local_path + "\\" + fileGet
		file = open(local_filename, 'wb')
		self.FTP.retrbinary('RETR %s' % filename, file.write)
		file.close()
		
	def changeLocalDir(self, dir):
		try_new_path = ""
		if not self.is_directory(dir):
			print("That is not a valid directory")
			return -1
		if ".." in dir:
			cd_path = dir.split('/')
			j = 0
			lastCD = len(cd_path)
			new_path = self.local_path
			k = 1
			pathsArr = new_path.split('\\')
			for path in pathsArr:
				if path.strip() != "":
					k = k + 1
			paths_count = k
			for get_cd in cd_path:
				if j == paths_count - 2:
					break
				if get_cd == "..":
					pathsArr = new_path.split('\\')
					i = 0
					use_new_path = ''
					lastArr = len(pathsArr)
					for path in pathsArr:
					
						p3 = re.compile('[a-zA-Z]{1}\:[\/]{0,1}')
						m3 = p3.match(path)
						if path.strip() != "" or m3:
							if i < lastArr - 1:
								if use_new_path == '':
									use_new_path = path
								else:
									use_new_path += "\\" + path
						i = i + 1
					new_path = use_new_path
					j = j + 1
			p = re.compile('[a-zA-Z]{1}\:')
			m = p.match(new_path)
			if m:
				new_path = new_path + "\\"
			self.local_path = new_path
			return 1
		else:
			try_new_path = self.local_path + "\\" + dir.replace("/", "\\")
			try:
				for f in os.listdir(try_new_path):
					does_list = True
			except FileNotFoundError:
				self.changeLocalDir("../")
				print("Path " + try_new_path.replace("\\\\", "\\") + " does not exist")
				return 0
		self.local_path = try_new_path
		return 1
		
	def is_directory(self, dir):
		p2 = re.compile('[^\.^/]{1}')
		m2 = p2.match(dir)
		if m2:
			p = re.compile('[^a-z^A-Z^0-9^\-^_]{1}')
			m = p.match(dir)
			if m:
				return False
			else:
				return True
		else:
			return True
			
def main():
	FTP = MFTP()
	while (True):
		command = input("# ")
		if command == "exit":
			break
		FTP.parseCommand(command)
	
if __name__ == "__main__": main()       