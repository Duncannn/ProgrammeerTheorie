# Amstelheage programmeertheorie assignment
# Thomas, Jonathan, Duncan

import math
import random
from Tkinter import *

class Position(object):
	"""
	Location in the land of the center of the house
	SHOULD BE FINISHED WRT THE AMOUNT OF METHODS
	"""

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def getNewPosition(self, distance_change):
		"""
		Returns a new position. For now I assume that the new position is 0.5 away and can move to
		8 possible locations. 
		We should actually just draw a random number between 0 and 2 pi and move the position 0.5
		steps in that angle.

		NOTYET IMPLEMENTD!!!!
		"""
		old_x, old_y = self.getX(), self.getY()
		new_x = old_x + random.sample((-distance_change, distance_change),1)[0]
		new_y = old_y + random.sample((-distance_change, distance_change),1)[0]
		return Position(new_x, new_y)


class Land(object):
	"""
	A rectangular field containing empty or filled areas
	"""

	def __init__(self, houses, width, depth):
		self.houses = houses
		self.width = width
		self.depth = depth
		self.land = []

	def angleConvert(self, house1, house2, vrijstandMethod = True):
		"""
		Creates a list with angles
		housex is house with specs: (width, depth, min_dist)
		The vrijstandmethode assumed the required vrijstand is to be added to the
		vrijstand, so remove it from the minimum_distance

		Returns the dict {x : minimum_distance}
		"""
		# Create dict for angles
		angles = {}

		# Here I'm going to calculate the minimum distance assigned to each angle
		# Loop through angles smaller than 45 so I can use the cos (adjacent is known)
		for i in range(0,45):
			j = math.pi*i/180
			if not vrijstandMethod:
				angles[i] = ((house1[0]+house2[0])/2 + max(house1[2], house2[2]))/math.cos(j)
			else:
				angles[i] = ((house1[0]+house2[0])/2)/math.cos(j)

		# Loop through angles largeR than 45 so I can use the sin (opposite is known)
		for i in range(45,91):
			j = math.pi*i/180
			if not vrijstandMethod:
				angles[i] = ((house1[1]+house2[1])/2 + max(house1[2], house2[2]))/math.sin(j)
			else:
				angles[i] = ((house1[1]+house2[1])/2)/math.sin(j)

		# return angles with minimum distances 
		return angles

	def markLandAtPosition(self, new_location, min_dist, house_type, specifications):
		"""
		Appends the location to the list of locations where the land is occupied
		"""
		self.land.append((new_location.getX(), new_location.getY(), house_type, specifications))

	def checkPosition(self, location, min_dist, specifications, type_house):
		"""
		Checks if the house is touching any of the other houses.

		Location is a tuple with 2 elements
		MIN_DIST IS NOT USED, SHOULD BE REMOVED
		Specifications is a list with three values: [width, depth, min_dist]
		TYPE_HOUSE IS NOT USED, SHOULD BE REMOVED

		Returns True or False and edits the land list
		"""
		# Must check every house which is in the land
		for house in self.land:

			# Calculate the opposite and adjacent of the triangle 
			# Use pythagoras to calculate the hypotenuse
			x_dist = math.fabs(location.getX() - house[0])
			y_dist = math.fabs(location.getY() - house[1])
			distance = math.sqrt(x_dist**2+y_dist**2)

			# Calculate the angle the house is at wrt the location we're currently at
			if x_dist != 0 :
				angle = int(round(math.atan(y_dist/x_dist)*180/math.pi))
			# can't devide by zero.
			else:
				angle = 0

			# Create the angle list, if the distance is smaller than the minimum
			# we found in the angle list, position is not available
			angle_list = self.angleConvert(specifications, house[3], False)
			if distance < angle_list[angle]:
				return False
		# All distances where larger than the angle list: position is viable
		return True

	def getTotalVrijstand(self):
		"""
		Checks the total vrijstand of the land
		Still have to remove his own house distance
		"""
		# Set initial vrijstand to zero
		vrijstand = 0
		# We must compare all houses to eachother, so loop over them twice
		for i, house1 in enumerate(self.land):
			all_distances = []
			for j, house2 in enumerate(self.land):
				# Minimum distance of same house is zero, must remove that one!
				if i == j :
					pass
				else:
					# Again, calculate the length of all the sides of the triangle
					x_dist = math.fabs(house1[0] - house2[0])
					y_dist = math.fabs(house1[1] - house2[1])
					distance = math.sqrt(x_dist**2+y_dist**2)

					# Calculate the angles and obtain the angle list
					if x_dist != 0 :
						angle = int(round(math.atan(y_dist/x_dist)*180/math.pi))
					else:
						angle = 0
					angle_list = self.angleConvert(house1[3], house2[3])

					# Append the difference between the distance and the minimum distance
					all_distances.append(math.sqrt(x_dist**2+y_dist**2)-angle_list[angle])

			# Calculate the minimum vrijstand for this house
			vrijstand += min(all_distances)
		print "Total vrijstand is          :", vrijstand

	def getVrijstand(self, location, specifications):
		"""
		Looks for the vrijstand of the house with this location
		"""
		# Initialise variables
		vrijstand = 0
		all_distances = []
		# Loop through all the houses
		for house in self.land:
			# Distance is zero if comparing the same  house
			if (house[0], house[1]) == (location.getX(), location.getY()):
				pass
			else:
				# Again, calculate the length of all the sides of the triangle
				x_dist = math.fabs(location.getX() - house[0])
				y_dist = math.fabs(location.getY() - house[1])
				distance = math.sqrt(x_dist**2+y_dist**2)

				# Calculate the angles and obtain the angle list. This angle list
				# does assume that the required vrijstand is part of the house itself
				if x_dist != 0 :
					angle = int(round(math.atan(y_dist/x_dist)*180/math.pi))
				else:
					angle = 0
				angle_list = self.angleConvert(specifications, house[3], False)

				# Append the difference between the distance and the minimum distance
				all_distances.append(math.sqrt(x_dist**2+y_dist**2)-angle_list[angle])

		# Return the smallest distance
		return min(all_distances)



	def getRandomPosition():
		"""
		No need yet???
		"""
		pass


	def isPositionInLand(self, location, width, depth, min_dist):
		"""
		Checks if the location of the house is viable wrt the land

		Location is a tuple with 2 elements, 
		min_dist is the minimum distance the house has wrt the land
		Returns true or False
		"""
		# Obtain minimum x and y coordinates
		x_coordinate = width/2 + min_dist
		y_coordinate = depth/2 + min_dist

		# Check if all the corners of the houses are in the land
		if (location.getX() >= x_coordinate and 
		    location.getX() <= self.width - x_coordinate and
		    location.getY() >= y_coordinate and
		    location.getY() <= self.depth - y_coordinate):
			return True
		return False



class House(object):
	"""
	Represents a house located on the field.

	House object must be located within the areas of the field at all times
	Probably needs some method to move the house to a different location and
	subsequently re-evaluate the score
	"""
	
	def __init__(self, land, width, depth, value, bonus, min_dist):
		self.land = land
		self.width = width
		self.depth = depth
		self.value = value
		self.bonus = bonus
		self.min_dist = min_dist
		self.spec = [self.width, self.depth, self.min_dist]

	def setHousePosition(self, type_house):
		"""
		Creates a random position in the room.

		returns False if the position is not viable
		"""
		# Create a random location
		self.location = Position(random.randint(0, self.land.width), random.randint(0, self.land.depth))
		# Check is the position is in the land. Actually... if the position object is 
		# random.randint(min_dist + self.width/2, self.land.width - min_dist - self.width/2)
		# and the same for the y coordinate, we dont even need this if function....
		if self.land.isPositionInLand(self.location, self.width, self.depth, self.min_dist):
			# Check if the position is in the land, and mark the land
		    if self.land.checkPosition(self.location, self.min_dist, self.spec, type_house):
				self.land.markLandAtPosition(self.location, self.min_dist, type_house, self.spec)
				return True
		# return False is the location is not viable
		return False

	def getHouseValue(self):
		"""
		Calls some method that calculates the minimal vrijstand.

		Returns the value of the house
		"""
		vrijstand = self.land.getVrijstand(self.location, self.spec)
		return (self.value * (1 + vrijstand * self.bonus), self.value)


	def getHousePosition(self):
		"""
		Returns the location of the center of the house
		"""
		return self.location

	def updatePosition(self):
		"""
		Call the getNewPosition in the position class.

		Checks if the location is in the field with isPositionInLand
		checks if any other house is already in this location with checkPosition
		THE 0.5 IS JUST THE DISTANCE THE HOUSE MOVES
		"""
		# create a new position
		old_pos = self.location
		new_pos = self.location.getNewPosition(0.5)

		# Check is the position is viable, if so, we have a new pos, else use old pos
		if self.land.isPositionInLand(self.location, self.width, self.depth, self.min_dist):
			if self.land.checkPosition(self.location, self.min_dist, "DONT KNOW"):
				return new_pos
		return old_pos

class Small(House):
	"""
	The smallest house
	"""
	def __init__(self, land, width, depth, value, bonus, min_dist):
		House.__init__(self, land, width, depth, value, bonus, min_dist)
		

class Medium(House):
	"""
	Medium house
	"""
	def __init__(self, land, width, depth, value, bonus, min_dist):
		House.__init__(self, land, width, depth, value, bonus, min_dist)
 

class Large(House):
	"""
	Biggest house
	"""
	def __init__(self, land, width, depth, value, bonus, min_dist):
		House.__init__(self, land, width, depth, value, bonus, min_dist)
 

def Visualisation(land, houses):
	"""
	Displays the GUI of the field with houses
	"""
	# Prints the total vrijstand and the total value of the land
	land.getTotalVrijstand()
	total_value_vrijstand = 0
	total_value = 0
	for house in houses:
		total_value_vrijstand += house[0].getHouseValue()[0]
		total_value += house[0].getHouseValue()[1]
	print "Total value WITH bonus is   :", "{:,}".format(total_value_vrijstand*1000)
	print "Total value WITHOUT bonus is:", "{:,}".format(total_value*1000)


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

	# Plot the houses. NOTE, because the scaling is 40 pixels for 10 meters, 
	# it is 4 pixels for 1 meter
	for coordinates in land.land:
		if coordinates[2] == "Small":
			w.create_rectangle(scaling+(coordinates[0]-4)*4, 
							   scaling+(coordinates[1]-4)*4, 
							   scaling+(coordinates[0]+4)*4, 
							   scaling+(coordinates[1]+4)*4, fill ="Blue")
		elif coordinates[2] == "Medium":
			w.create_rectangle(scaling+(coordinates[0]-5)*4, 
							   scaling+(coordinates[1]-3.75)*4, 
							   scaling+(coordinates[0]+5)*4, 
							   scaling+(coordinates[1]+3.75)*4, fill ="Red")
		else:
			w.create_rectangle(scaling+(coordinates[0]-5.5)*4, 
							   scaling+(coordinates[1]-5.25)*4, 
							   scaling+(coordinates[0]+5.5)*4, 
							   scaling+(coordinates[1]+5.25)*4, fill ="Yellow")

	master.mainloop()

def simulation():
	"""
	I'm going to try and randomize the houses and check if the algorithm we have works
	CHANGED DEPTH VARS BECAUSE OF FLOATS
	"""
	# Initialise variables
	m = 1
	variant = 40
	land = Land(variant, 120, 160)
	houses_amount = [house * variant for house in [0.6, 0.25, 0.15]]
	houses = []

	# Add houses to the house list
	for i in range(int(houses_amount[0])):
		houses.append((Small(land, 8.0, 8.0, 285.0, 0.03, 2.0), "Small"))

	for i in range(int(houses_amount[1])):
		houses.append((Medium(land, 10.0, 8.0, 399.0, 0.04, 3.0), "Medium"))

	for i in range(int(houses_amount[2])):
		houses.append((Large(land, 11.0, 11.0, 610.0, 0.06, 6.0), "Large"))

	# Set all the houses at specific initial locations. If the location is incorrect, keep
	# setting the house untill it is correct
	for house in houses:
		# Keeps track of what house we're at
		print m
		good_loc = house[0].setHousePosition(house[1])
		while good_loc == False:
			good_loc = house[0].setHousePosition(house[1])
		m +=1
	# Visualise the result
	Visualisation(land, houses)

if __name__ == "__main__":
	simulation()
