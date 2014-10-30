# Amstelheage programmeertheorie assignment
# Thomas, Jonathan, Duncan

from Tkinter import *

class Land(object):
	"""
	A rectangular field containing empty or filled areas
	"""

	def __init__(self, houses, width, depth):
		self.houses = houses
		self.width = width
		self.depth = depth

		# Save locations in a dict? BTW this isn't really correct, because we have houses that have
		# floats as dimensions
		self.land = {}
		for i in range(0,120):
			for j in range(0,160):
				self.land[(i,j)] = "empty"
	
	def markLand(self, new_location, old_location):
		"""
		Marks the new location as full and old as empty
		"""
		for i in range(old_location[0], old_location[2]):
			for j in range(old_location[1], old_location[3]):
				self.land[(i,j)] = "empty"
		
		for i in range(new_location[0], new_location[2]):
			for j in range(new_location[1], new_location[3]):
				self.land[(i,j)] = "full"
		return self.land

	def otherHouseTouching(self, location):
		"""
		Checks if the house is touching any of the other houses.
		Returns True or False
		"""
		pass

	def isLocationViable(self, location, min_dist):
		"""
		Checks if the location of the house is viable wrt the land
		
		Location is a tuple with 4 elements (x0, y0, x1, y1)
		min_dist is the minimum distance the house has wrt the land
		Returns true or False
		"""
		return (location[0] + min_dist > 0 and
			location[2] + min_dist < self.width and
			location[1] + min_dist > 0 and
			location[3] + min_dist < self.depth)

class House(object):
	"""
	Represents a house located on the field.

	House object must be located within the areas of the field at all times
	Probably needs some method to move the house to a different location and
	subsequently re-evaluate the score.
	
	I'm not actually sure we need this parent class for the other houses, because the ONLY thing that differs about
	the houses are the dimensions... they all act in the exact same manner.
	"""
	
	def __init__(self, width, depth, value, bonus):
		self.width = width
		self.depth = depth
		self.value = value
		self.bonus = bonus
 

class Small(House):
	"""
	The smallest house
	"""
	def __init__(self, width, depth, value, bonus):
		House.__init__(self, width, depth, value, bonus)
		

class Medium(House):
	"""
	Medium house
	"""
	def __init__(self, width, depth, value, bonus):
		House.__init__(self, width, depth, value, bonus)

class Big(House):
	"""
	Biggest house
	"""
	def __init__(self, width, depth, value, bonus):
		House.__init__(self, width, depth, value, bonus)


def Visualisation():
	"""
	Displays the GUI of the field with houses
	"""
	master = Tk()
	master.title("Amstelheage")
	# Scaling in the GUI: 10 meters is 40 pixels, otherwise the squares are tiny.
	scaling = 40

	# Create the GUI
	w = Canvas(master, width=800, height=1000)

	# Make squares for the land. I guess I could also have done a single square:
	# w.create_rectangle(40,40,520,680)
	for j in range(1,13):
		for i in range(1,17):
			w.create_rectangle(j*scaling, i*scaling, (j+1)*scaling, (i+1)*scaling, fill="green", width=0)
			w.pack()

	# Label for explanation
	lbl = Label(text="Green is unfilled land \n Blue is a detached house \n Red is a bungalow \n Yellow is a maison")
	lbl.place(x=550, y=40)

	# maximum width and height
	max_value_width = 12*scaling
	max_value_height = 16*scaling
	# tuple[0]=length, tuple[1] = depth, tuple[2] = min distance 
	detached = (0.8*scaling, 0.8*scaling, 8)
	bungalow = (scaling, 0.75*scaling, 12)
	maison = (1.1*scaling, 1.05*scaling, 24)
	# Current house number  
	det = 0
	bun = 0
	mai = 0
	value = 0

	# draw squares. Again this is NOT the way we should do it in the end, this is just an example.
	for i in range(1,20):
		if i <= 0.6*20 and (scaling + i * detached[2] + (i-1)*detached[0]+detached[2]) <= max_value_width:
			det += 1
			w.create_rectangle(scaling + det * detached[2] + (det-1)*detached[0], 
							   scaling + detached[2], 
							   scaling + det *(detached[0] + detached[2]), 
							   scaling + detached[1]+ detached[2], 
							   fill = "blue")
			value += 285
		elif i <= 0.85*20 and i > 0.6*20:
			bun += 1
			w.create_rectangle(scaling + bun * bungalow[2] + (bun-1)*bungalow[0], 
							   scaling + detached[1]+ detached[2] + bungalow[2], 
							   scaling + bun *(bungalow[0] + bungalow[2]), 
							   scaling + detached[1]+ detached[2] + bungalow[1]+ bungalow[2], 
							   fill = "red")
			value += 399
		else:
			mai += 1
			w.create_rectangle(scaling + mai * maison[2] + (mai-1)*maison[0], 
							   scaling + detached[1]+ detached[2] + bungalow[1]+ bungalow[2] + maison[2], 
							   scaling + mai *(maison[0] + maison[2]), 
							   scaling + detached[1]+ detached[2] + bungalow[1]+ bungalow[2] + maison[2] + maison[1], 
							   fill = "yellow")
			value += 610
	value *= 1000

	# Score label
	score = StringVar()
	lbl2 = Label(textvariable = score)
	lbl2.place(x=550, y=300)
	# Setting the score should be at some time when we change the position of a house
	score.set("Value of the land is: " +str(value))

	master.mainloop()
	
def simulation(variant):
	"""
	Just starting creating the land and adding houses to it.
	"""
	# Create the land and amount of houses
	land = Land(variant, 120, 160)
	houses_amount = [house*variant for house in [0.6, 0.25, 0.15]]
	houses = []
	
	# Add houses to the house list
	for i in range(int(houses_amount[0])):
		houses.append(Small(8, 8, 285, 1.03))
	for i in range(int(houses_amount[1])):
		houses.append(Medium(10, 7.5, 399, 1.04))
	for i in range(int(houses_amount[2])):
		houses.append(Big(11, 10.5, 610, 1.06))
	
	# I guess now we've got to somehow create an initial state for all the houses and then some algorithm
	# to optimize the score.
	
if __name__ == "__main__":
	Visualisation()
