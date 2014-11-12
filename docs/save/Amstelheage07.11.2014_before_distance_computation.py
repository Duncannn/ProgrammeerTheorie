# Amstelheage programmeertheorie assignment
# Thomas, Jonathan, Duncan

import math
import random
from Tkinter import *
import pylab

def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist

def rect_distance((x1, y1, x1b, y1b), (x2, y2, x2b, y2b)):
    left = x2b < x1
    right = x1b < x2
    bottom = y2b < y1
    top = y1b < y2
    if top and left:
        return calculateDistance(x1, y1b, x2b, y2)
    elif left and bottom:
        return calculateDistance(x1, y1, x2b, y2b)
    elif bottom and right:
        return calculateDistance(x1b, y1, x2, y2b)
    elif right and top:
        return calculateDistance(x1b, y1b, x2, y2)
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif bottom:
        return y1 - y2b
    elif top:
        return y2 - y1b
        

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
  		new_x, new_y = 0, 0
		while new_x ==  0 and new_y == 0:
			new_x = old_x + random.sample((-distance_change,0, distance_change),1)[0]
			new_y = old_y + random.sample((-distance_change,0, distance_change),1)[0]
		
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

	def markLandAtPosition(self, location, specifications, class_var):
		"""
		Appends the location to the list of locations where the land is occupied
		Removes the old location
		"""
		self.land.append((location.getX(), location.getY(), specifications, class_var))

	def removeLandAtPosition(self, location, specifications, class_var):
		"""
		Removes the location from the list
		"""
		self.land.remove((location.getX(), location.getY(), specifications, class_var))


	def checkPosition(self, location, min_dist, specifications):
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

			# Find the minimum distances
			if angle < 45:
				minimum_dist = ((specifications[0]+house[2][0])/2 + 
								max(specifications[2], house[2][2]))/math.cos(math.pi*angle/180)
			else:
				minimum_dist = ((specifications[1]+house[2][1])/2 + 
								max(specifications[2], house[2][2]))/math.sin(math.pi*angle/180)
			# First position only needs to know if
			if distance < minimum_dist:
				return False

		# All distances where larger than the minimum distance: position is viable
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
					if angle < 45:
						minimum_dist = ((house1[2][0]+house2[2][0])/2)/math.cos(math.pi*angle/180)
					else:
						minimum_dist = ((house1[2][1]+house2[2][1])/2)/math.sin(math.pi*angle/180)

					# Append the difference between the distance and the minimum distance
					all_distances.append(math.sqrt(x_dist**2+y_dist**2)-minimum_dist)

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
				# Find the minimum distances
				if angle < 45:
					minimum_dist = ((specifications[0]+house[2][0])/2 + 
									max(specifications[2], house[2][2]))/math.cos(math.pi*angle/180)
				else:
					minimum_dist = ((specifications[1]+house[2][1])/2 + 
									max(specifications[2], house[2][2]))/math.sin(math.pi*angle/180)

				# Append the difference between the distance and the minimum distance
				all_distances.append(distance-minimum_dist)

		# Return the smallest distance
		return min(all_distances)

	def getTotalValue(self):
		"""
		Calculates the total value of the land
		"""
		total_val = 0
		for house in self.land:
			total_val += house[3].getHouseValue()[0]
			#print total_val
		return total_val


	def getHouses(self):
		"""
		No need yet???
		"""
		return self.land
  
	def getRandomPosition(self):
		"""
		No need yet???
		"""
		random_pos = Position(random.randint(0, self.width), random.randint(0, self.depth))
		return random_pos	



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
	
	def __init__(self, land, width, depth, value, bonus, min_dist, location):
		self.land = land
		self.width = width
		self.depth = depth
		self.value = value
		self.bonus = bonus
		self.min_dist = min_dist
		self.location = location
		self.spec = [self.width, self.depth, self.min_dist]

	def setHousePosition(self,position):
		"""
		Creates a random position in the room.

		returns False if the position is not viable
		"""
		# Create a random location
		self.location = position
		self.land.markLandAtPosition(self.location, self.spec, self)       
		# Check is the position is in the land. Actually... if the position object is 
		# random.randint(min_dist + self.width/2, self.land.width - min_dist - self.width/2)
		# and the same for the y coordinate, we dont even need this if function....


	def checkHousePosition(self, position):
		"""
		Check if house position is viable.

		Returns true if house is on good position, false otherwise
		"""
		if self.land.isPositionInLand(position, self.width, self.depth, self.min_dist):
			# Check if the position is in the land, and mark the land
		    if self.land.checkPosition(position, self.min_dist, self.spec):
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
  
	def getEdges(self):
		"""
		Returns the edgeds of a house as four x and y coordinate tuples.
		First tuple is left top corner.
		Second tuple is right top corner.  
		Third tuple is right bottom corner.
		Fourth tuple is left bottom corner.             
		"""
		x_val = self.location.getX()
		y_val = self.location.getY()
  
 		left_bottom = (x_val - (self.width/2), y_val - (self.depth/2))
 		right_bottom = (x_val + (self.width/2), y_val - (self.depth/2))
 		left_top = (x_val - (self.width/2), y_val + (self.depth/2))
 		right_top = (x_val + (self.width/2), y_val + (self.depth/2))   
		return (left_top,right_top,right_bottom,left_bottom)

	def updatePosition(self):
		"""
		Call the getNewPosition in the position class.

		Checks if the location is in the field with isPositionInLand
		checks if any other house is already in this location with checkPosition
		checks if the value of the house increases
		THE 0.5 IS JUST THE DISTANCE THE HOUSE MOVES
		STIL HAVE TO CHECK IF ALL THE OTHER HOUSES ALSO HAVE THE SAME VALUE
		SO ACTUALLY HAVE TO CHECK THE TOTAL VALUE
		"""
		# create a new position
		old_pos = self.location
		old_value = self.getHouseValue()[0]
		#old_value = self.land.getTotalValue()
		self.land.removeLandAtPosition(self.location, self.spec, self)
		self.location = self.location.getNewPosition(0.5)
		new_pos = self.location

		# Check is the position is viable, if so, we have a new pos, else use old pos
		if self.land.isPositionInLand(new_pos, self.width, self.depth, self.min_dist):
			if self.land.checkPosition(new_pos, self.min_dist, self.spec):
				self.location = new_pos
				#new_value = self.land.getTotalValue()
				new_value = self.getHouseValue()[0]	
				if new_value > old_value:
					self.land.markLandAtPosition(self.location, self.spec, self)
					return new_value-old_value
		#print "Was not a better position!!!"
		self.location = old_pos
		self.land.markLandAtPosition(self.location, self.spec, self)
		return 0
 

def Visualisation(inputs):
	"""
	Displays the GUI of the field with houses
	"""

	# Prints the total vrijstand and the total value of the land
	#total_value_vrijstand = 0
	#total_value = 0
	#for house in houses:
	#	total_value_vrijstand += house[0].getHouseValue()[0]
	#	total_value += house[0].getHouseValue()[1]
	#print "Total value WITH bonus is   :", "{:,}".format(total_value_vrijstand*1000)
	#print "Total value WITHOUT bonus is:", "{:,}".format(total_value*1000)
	#land.getTotalVrijstand()


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
	for coordinates in inputs[1]:
		if coordinates[2] == [8.0, 8.0, 2.0]:
			w.create_rectangle(scaling+(coordinates[0]-4)*4, 
							   scaling+(coordinates[1]-4)*4, 
							   scaling+(coordinates[0]+4)*4, 
							   scaling+(coordinates[1]+4)*4, fill ="Blue")
		elif coordinates[2] == [10.0, 7.5, 3.0]:
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

def performancePlots(monitoring):
    
    length = len(monitoring)
    pylab.figure()
    pylab.subplot(1,1,1)
    pylab.plot(range(length),monitoring,color="blue", linewidth=1.0, linestyle="-",label="20 Huizen ")
    pylab.legend(loc='upper left')
    pylab.title("Performance Plots")
    pylab.show()
    

def simulation():
	"""
	I'm going to try and randomize the houses and check if the algorithm we have works
	CHANGED DEPTH VARS BECAUSE OF FLOATS
	"""
	# Initialise variables
	m = 0
	variant = 60
 	monitoring = []
	best_solution = (0, None)
	for j in range(5):
		land = Land(variant, 120, 160)
		houses_amount = [house * variant for house in [0.6, 0.25, 0.15]]
		houses = []
		total_value_vrijstand = 0

		# Add houses to the house list
		for i in range(int(houses_amount[0])):
			houses.append((House(land, 8.0, 8.0, 285.0, 0.03, 2.0, None), "Small"))

		for i in range(int(houses_amount[1])):
			houses.append((House(land, 10.0, 7.5, 399.0, 0.04, 3.0, None), "Medium"))

		for i in range(int(houses_amount[2])):
			houses.append((House(land, 11.0, 10.5, 610.0, 0.06, 6.0, None), "Large"))

		# Set all the houses at specific initial locations. If the location is incorrect, keep
		# setting the house untill it is correct
		for house in reversed(houses):
			# Keeps track of what house we're at
			position = land.getRandomPosition()
			good_loc = house[0].checkHousePosition(position)
			while good_loc == False:
				position = land.getRandomPosition()
				good_loc = house[0].checkHousePosition(position)
			house[0].setHousePosition(position)
			m +=1
			#print m

		initial_value = 0
		for house in houses:
			initial_value += house[0].getHouseValue()[0]

		monitoring.append(initial_value)
      
		current_value = initial_value  
		for i in range(5000):
			#print i
			house = random.choice(houses)
   			current_value += house[0].updatePosition()
			monitoring.append(current_value)
			   
		for house in houses:
			total_value_vrijstand += house[0].getHouseValue()[0]
		if total_value_vrijstand > best_solution[0]:
			best_solution = (total_value_vrijstand, land.land)
		print j+1, total_value_vrijstand
	# Visualise the result
	land.getTotalValue()
	print initial_value
	print "The best solution is           :", "{:,}".format(best_solution[0]*1000)
	Visualisation(best_solution)
	return monitoring

if __name__ == "__main__":
	#random.seed(3)
	monitoring = simulation()
	performancePlots(monitoring)
         
