import re
import tkinter as tk
from tkinter import messagebox

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
		self.seat = ord(info[3])-ord("A")

class Seat():
	def __init__(self,datanode):
		# dic: {rowID: Passenger}
		self.passenger = Passenger(datanode)
		self.dic = {self.passenger.rowID: self.passenger}

	def insert(self,passenger):
		self.passenger = passenger
		self.dic = {self.passenger.rowID: self.passenger}

class Row():
	# dic: {rowID: seat}
	# a list of dic
	seats = []

	def __init__(self, seats=[]):
		self.seats = list(map(lambda seat: {seat.passenger.rowID: seat},seats))

	def insert(self, seat):
		self.seats.append({seat.passenger.rowID: seat})

class Section():
	def __init__(self, rows):
		# ex: {first: row 0-5}
		# a set of rows
		self.rows = rows
		pass

	def insert(self,seat):
		for i in self.rows:
			i.insert(seat)


class Jet():
	def __init__(self):
		pass
	def __init__(self, first, business, economy):
		self.sections = [first, business, economy]

	def insert(self,seat):
		for i in self.sections:
			i.insert(seat)

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
	economy = Section(set(rows[16:36]))
	jet = Jet(first, business, economy)
	return jet

class Airplane_view():
	def __init__(self):
		self.master = tk.Tk()
		self.master.title("bubblemans Airline")
		self.master.geometry("1300x450")

	def create_button(self,image,r,c,flag,jet):
		x = 30 * int(c)
		y = 30 * int(r)
		if c > 5:
			x = x + 40
		if c > 15:
			x = x + 40
		if r > 1:
			y = y + 40
		if r > 4:
			y = y + 40
		x = x + 30
		y = y + 80

		button = tk.Button(self.master, fg="blue")
		button.config(height=27, width=27, image=image, command = lambda: Clicked(self,flag,r,c,jet))
		button.image = image
		button.pack()
		button.place(x=x,y=y,in_=self.master)

	def create_label(self,h,w,x,y,text):
		label = tk.Label(self.master, text = text)
		label.config(height=h,width=w)
		label.pack()
		label.place(x=x,y=y)

	def insert_passenger(self,r,c,jet):
		top = tk.Toplevel()
		top.title = "Selecting the seat..."

		lastname_entry = tk.Entry(top)
		firstname_entry = tk.Entry(top)
		lastname_entry.grid(row=0, column=1)
		firstname_entry.grid(row=1, column=1)

		lastname_label = tk.Label(top,text="lastname",height=3,width=10)
		firstname_label = tk.Label(top,text="firstname",height=3,width=10)
		lastname_label.grid(row=0, column=0)
		firstname_label.grid(row=1, column=0)

		send_button = tk.Button(top, text="send", command = lambda: send_info(top,lastname_entry.get(),firstname_entry.get(),r,c,jet))
		send_button.grid(row=1, column=2)



	def show(self):
		self.master.mainloop()

	def dismiss(self):
		self.master.destroy()

def send_info(top,lastname,firstname,r,c,jet):
	top.destroy()
	datanode = lastname+","+firstname+","+str(c)+","+chr(r+65)
	seat = Seat(datanode)
	jet.insert(seat)

def Clicked(view,flag,r,c,jet):
    if flag == True:
    	# messagebox.showinfo("bubblemans Airline", "Thanks for choosing us! Have a great flight.")
    	image = tk.PhotoImage(file="close.gif")
    	flag = not flag
    	view.create_button(image,r,c,flag,jet)
    	view.insert_passenger(r,c,jet)


    else:
    	messagebox.showwarning("bubblemans Airline", "Sorry, the seat is sold out.")

def draw_seats(jet):
	airplane = Airplane_view()
	rc = []
	for section in jet.sections:
		for rows in section.rows:
			for seats in rows.seats:
				for key in seats:
					c = int(re.findall("\d+",key)[0])
					r = ord(re.findall("[a-zA-Z]",key)[0])-ord("A")
					rc.append((r,c))

					image = tk.PhotoImage(file="close.gif")
		
					airplane.create_button(image,r,c,False,jet)

	for r in range(7):
		for c in range(36):
			if (r,c) not in rc:
				image = tk.PhotoImage(file="occupy.gif")
				airplane.create_button(image,r,c,True,jet)

	alph_list = ["A","B","C","D","E","F","G"]
	for i in range(len(alph_list)):
		y = i * 30 + 85
		if i > 1:
			y = y + 40
		if i > 4:
			y = y + 40
		airplane.create_label(1,1,5,y,alph_list[i])

	for i in range(36):
		x = i * 30 + 40
		if i > 5:
			x = x + 40
		if i > 15:
			x = x + 40
		airplane.create_label(1,1,x,55,str(i))

	class_list = ["First", "Business", "Economy"]
	for i in range(len(class_list)):
		x = 0
		if i == 0:
			x = 20
		elif i == 1:
			x = 300
		else:
			x = 760
		airplane.create_label(1,20,x,10,class_list[i])
	
	airplane.show()

def main():
	jet = parse_data()
	draw_seats(jet)


main()

