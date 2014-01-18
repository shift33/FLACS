import socket

class Settings:

	host="192.168.2.4"
	user=socket.gethostname()
	passwd="fablab"
	db="FabControl"

	#Generic data for visitlogging
	id = 0
	organisation = 0
	facility = 0
	location = socket.gethostname()
	hostname = socket.gethostname()
	terminal = 0
	software = 20011
	operator = 0

	
	
	
	
	#Getters and setters for properties
	def id(self): return self.id
	def organisation(self): return self.organisation
	def facility(self): return self.facility
	def location(self): return self.location
	def hostname(self): return self.hostname
	def terminal(self): return self.terminal
	def software(self): return self.software
	def operator(self): return self.operator
	def host(self): return self.host
	def user(self): return self.user
	def passwd(self): return self.passwd
	def db(self): return self.db
