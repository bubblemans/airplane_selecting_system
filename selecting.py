import re

class Datanode():
	def __init__(self):
		# needs to parses using re
		pass

class Person(Datanode):
	def __init__(self, firstname, lastname):
		self.firstname = firstname 
		self.lastname = lastname

class Passenger(Person):
	def __init__(self, rowID, row, seat):
		self.rowID = rowID
		self.row = row
		self.seat = seat

class Seat(Passenger):
	def __init__(self, dic):
		# dic: {rowID: Passenger}
		self.dic = dic

class Row():
	def __init__(self, seats):
		# dic: {rowID: seat}
		# probably, it is a list of dic
		self.seats = seats

class Section():
	def __init__(self, dic):
		# ex: {first: row 0-5}
		# try to create a set of rows
		self.dic = dic

class Jet():
	def __init__(self, sections):
		self.sections = sections


























		