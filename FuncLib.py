class FuncLib:

	def connectDatabase(self,h,u,p,d)
		#MySQL Database variables
		db=mdb.connect(
				host=h,
				user=u,
				passwd=p,
				db=d,
				);
		return db.cursor()
		
	#Define scanning for numbers only
	def scan(self):
		while (True):
			try:
				x = int(raw_input('\033[94m' + "BARCODE: " + '\033[0m'))
			except ValueError:
				print '\033[91m' + "NOT A VALID USER" + '\033[0m'
				print ""
				continue
			else:
				return (x)
	def logContact(self,db,id,member,logBit,organisation, facility, location, hostname, terminal, software, operator)
		logtime = strftime("%Y-%m-%d %H:%M:%S")
		db.execute("""INSERT INTO visitlog (id, member, logtime,
		logcode, organisation, facility, location, hostname,
		terminal, software, operator)
		values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
		(id, member, logtime, logBit, organisation,
		facility, location, hostname, terminal, software, operator))
		db.commit()
		
	def objidGet(self,c,barcode)
		c.execute("""SELECT objid FROM scancode WHERE code = %s""",(barcode))
		return c.fetchone()
	
	def binidGet(self,c,machineName)
		c.execute("""SELECT binid FROM fabstatus WHERE machine = %s""",machineName)
		return c.fetchone()
	
	def flagsAndNameGet(c,rs)
		c.execute("""SELECT name, surname, flags FROM contact WHERE id = %s""",
		rs)
		return c.fetchone()
		