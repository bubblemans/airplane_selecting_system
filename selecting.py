import re

class Datanode():
	def __init__(self,data):
		# parse using re
		info = re.split("\W",data)
		return info

class Person(Datanode):
	def __init__(self,datanode):
		info = super(Person,self).__init__(datanode)
		self.lastname = info[0]
		self.firstname = info[1]

class Passenger(Person):
	def __init__(self,datanode):
		info = super(Person,self).__init__(datanode)
		super(Passenger,self).__init__(datanode)
		self.rowID = info[2]+info[3]
		self.row = info[2]
		self.seat = info[3]

class Seat():
	def __init__(self,datanode):
		# dic: {rowID: Passenger}
		self.passenger = Passenger(datanode)
		self.dic = {self.passenger.rowID: self.passenger}

class Row():
	# dic: {rowID: seat}
	# a list of dic
	seats = []

	def __init__(self, seats=[]):
		self.seats = list(map(lambda seat: {seat.passenger.rowID: seat},seats))

	def insert(self, seat):
		self.seats.append({seat.passenger.rowID, seat})

class Section():
	def __init__(self, rows):
		# ex: {first: row 0-5}
		# a set of rows
		self.rows = rows
		pass


class Jet():
	def __init__(self, first, business, economy):
		self.sections = [first, business, economy]

class Read_xml():
	def __init__(self):
		pass

	def opening(self, file_name):
		return open(file_name)

	def closing(self, file_data):
		file_data.close()
		pass

	def reading(self, file_data):
		return file_data.read()

def parse_data():
	manager = Read_xml()
	raw_data = manager.opening("Airline.xml")
	data = manager.reading(raw_data)
	parse_data = re.findall(">.*<", data)

	# get rid of > and <
	for i in range(len(parse_data)):
		parse_data[i] = parse_data[i][1:-1]

	passengers_info = iter(parse_data)
	seats = []
	for n in range(len(parse_data)//4):
		data = next(passengers_info)+","+next(passengers_info)+","+next(passengers_info)+","+next(passengers_info)
		seat = Seat(data)
		seats.append(seat)

	rows = []
	for _ in range(36):
		row = Row()
		rows.append(row)

	for i in range(len(seats)):
		row_number = seats[i].passenger.row
		rows[int(row_number)].insert(seats[i])

	first = Section(set(rows[0:6]))
	business = Section(set(rows[6:16]))
	economy = Section(set(rows[16:37]))
	jet = Jet(first, business, economy)


def main():
	parse_data()


main()
























		