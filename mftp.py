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
		
	def changeLocalDir(self, dir):
	
		if ".." in dir:
			cd_path = dir.split('/')
			j = 0
			lastCD = len(cd_path)
			new_path = self.local_path
			for get_cd in cd_path:
				if j < lastCD:
					pathsArr = new_path.split('\\')
					i = 0
					new_path = ''
					lastArr = len(pathsArr)
					for path in pathsArr:
						if i < lastArr - 1:
							if new_path == '':
								new_path = pathsArr[i]
							else:
								new_path += "\\" + pathsArr[i] 
						i = i + 1
				j = j + 1
			self.local_path = new_path
			
def main():
	FTP = MFTP()
	while (True):
		command = input("# ")
		if command == "exit":
			break
		FTP.parseCommand(command)
	


	
	
if __name__ == "__main__": main()       