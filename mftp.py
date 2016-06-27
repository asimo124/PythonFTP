#!/usr/bin/python

import os, sys
import glob, re
from ftplib import FTP

class MFTP:

	def __init__(self):
		self.local_path = 'C:\\Users\\dev5\\'

	def parseCommand(self, command):
		commandArr = command.split()
		if commandArr[0] == "open":
		
			if len(commandArr) == 2:
				self.open(commandArr[1], '', '')
			else:
				#         host,          username,      password
				self.open(commandArr[1], commandArr[2], commandArr[3])
		elif commandArr[0] == "ls":
			self.list()
		elif commandArr[0] == "cd":
			self.changeDir()
		elif commandArr[0] == "lls":
			self.listLocal()
		elif commandArr[0] == "lcd":
			self.changeLocalDir(commandArr[1])
			
	def open(self, host, username, password):
		if host == '247':
			self.FTP = FTP('71.40.14.247', 'alextest', 'gortex!22')
		else:
			self.FTP = FTP(host, username, password)

	def list(self):
		self.FTP.retrlines('LIST')
		
	def listLocal(self):
		for f in os.listdir(self.local_path):
			if os.path.isdir(os.path.join(self.local_path, f)):
				print("<dir> " + f)
			else:
				print("----- " + f)
		
		
	def changeDir(self):
	
		if not self.is_directory(dir):
			print("That is not a valid directory")
			return -1
	
		if ".." in dir:
			cd_path = dir.split('/')
			j = 0
			lastCD = len(cd_path)
			new_path = self.FTP.pwd()
			
			k = 1
			pathsArr = new_path.split('/')
			for path in pathsArr:
			
				if path.strip() != "":
					k = k + 1
			paths_count = k
			
			for get_cd in cd_path:
				if j == paths_count - 2:
					break
				if get_cd == "..":
					
					pathsArr = new_path.split('/')
					i = 0
					use_new_path = ''
					lastArr = len(pathsArr)
					for path in pathsArr:
					
						p3 = re.compile('\/')
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
						
				
			self.local_path = new_path
		else:
			self.local_path = self.local_path + "\\" + dir.replace("/", "\\")
		
		return 1
	
	
		
	def changeLocalDir(self, dir):
	
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
		else:
			self.local_path = self.local_path + "\\" + dir.replace("/", "\\")
		
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