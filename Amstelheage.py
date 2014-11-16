# Amstelheage programmeertheorie assignment
# Thomas, Jonathan, Duncan

import math
import random
from Tkinter import *
import pylab
import time
import copy

def calculateDistance(x1,y1,x2,y2):
	"""
	Input:
 	Two points (Point_1_x, Point_1_y, Point_2_x, Point_2_y)
	Return:
	Distance between input points as float.
	Purpose:
	Computing distance between two points.
	"""
	dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
	return dist


def rect_distance((x1, y1, x1b, y1b), (x2, y2, x2b, y2b)):
	"""
	Input:
 	Two rectangles (Rec_1_BottomLeft_Corner, Rec_1_TopRight_Corner,
                      Rec_2_BottomLeft_Corner, Rec_2_TopRight_Corner)
	Return:
	Minimum distance between rectangles as float.
	Purpose:
	Computing minimum distance between rectangles.
	"""
	left = x2b < x1
	right = x1b < x2
	bottom = y2b > y1
	top = y1b > y2
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
		return y2b - y1
	elif top:
		return y1b - y2


class Position(object):
	"""
	Location in the land of the center of the house
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
		Input:
		Distance the position should be moved.
		Return:
		Position object with new position.
		Purpose:
		Getting a new posisition which is "distance_change" away and can 
		move to 8 possible locations.              
		"""
		old_x, old_y = self.getX(), self.getY()
  		new_x, new_y = 0, 0
		while new_x ==  0 and new_y == 0:
			new_x = old_x + random.sample((-distance_change,0, distance_change),1)[0]
			new_y = old_y + random.sample((-distance_change,0, distance_change),1)[0]
		
		return Position(new_x, new_y)


class Land(object):
	"""
	A rectangular field containing empty or filled areas.
	"""
	def __init__(self, houses, width, depth):
		self.houses = houses
		self.width = width
		self.depth = depth
		self.land = {}
  
  
	def getWidth(self):
		return self.width
  
  
	def getDepth(self):
		return self.depth


	def markLandAtPosition(self, house):
		"""
		Input:
		House is a house object.
		Return:
		None
		Purpose:
		Appends the location to the list of locations where the land is occupied.
		"""
		name = house.getHouseName()
		self.land[name] = house
		return 0 


	def removeLandAtPosition(self, house):
		"""
		Input:
		House is a house object.
		Return:
		None
		Purpose:
		Removes the location from the list.  
		"""
		name = house.getHouseName()
		del self.land[name]
		return 0


	def checkPosition(self, location, specifications):
		"""
		Input:
		Location is a position object.
		Specifications is a list with three values: [width, depth, min_dist]
		Return:
		Returns True if position is viable and false if not.
		Purpose:
		Checks if the house is touching any of the other houses.
		"""
		# makes a "checkhouse" based on locations and specifications
		checkHouse = House(self, specifications[0], specifications[1], 0, 0, specifications[2], location)
		# minimum distance for this type of house
		minimum_distance = specifications[2]
		# loop through all the houses
		for key,house in self.land.iteritems():
			# Calculates distance between checkhouse and all other houses
			distance = self.getMinDistance(checkHouse,house)
			# If distance is smaller than minimum distance then return False
			if distance < max(minimum_distance, house.min_dist):
       				return False
		return True
           
           
	def getMinDistance(self, house1, house2):
		"""
		Input:
		Two house objects.
		Return:
		Minimum distance between the two houses.
		Purpose:
		Computes distance between two houses.
		"""
		# getting all edges of both houses  
		edges1 = house1.getEdges()
		edges2 = house2.getEdges()
		# computing minimum distance between houses 
		return rect_distance((edges1[3][0],edges1[3][1],edges1[1][0],edges1[1][1])
                            ,(edges2[3][0],edges2[3][1],edges2[1][0],edges2[1][1]))
     
     
	def getVrijstand(self, checkHouse):
		"""
		Input:
		Location is a position object.
		Specifications is a list with three values: [width, depth, min_dist]
		Return:
		Bonus vrijstand as a float and neighbor name as a string together in a tuple
		Purpose:
		Computing the bonus vrijstand of a given house (== location, specification).
		"""
		wall = False 
		# makes a "checkhouse" based on locations and specifications
		# checkHouse = House(self, specifications[0], specifications[1], 0, 0, specifications[2], location)
		# minimum distance for this type of house
		minimum_distance = checkHouse.getHouseSpecs()[2]
		all_distances = []
		# first value is bonus vrijstand if checkhouse would be the only house in the land
		all_distances.append(checkHouse.getMaxBorderDistance() - minimum_distance)
  
  
 		neighbors = checkHouse.getHouseNeighbor()

 		#if random.random() < 0.05:
 		#	neighbors = []
   
 		if len(neighbors) > 0:
			house_names = neighbors  
 		else:
			house_names = self.getHouses().keys()
		neighbor_name = []
		neighbor_distance = []
		neighbor_name.append("start value")
		neighbor_distance.append(999)
		# loop through all the houses
		for key in house_names:
			house = self.getHouses()[key]
			# distance is zero if comparing the same  house
			if house.getHousePosition() == checkHouse.getHousePosition():
				pass
			else:
				distance = self.getMinDistance(checkHouse,house)
				#print distance
				# append the difference between the distance and the minimum distance
				all_distances.append(distance-minimum_distance)
				# save the name of the nearest house
				if distance < max(neighbor_distance):
					neighbor_name.append(house.getHouseName())
					neighbor_distance.append(distance)

					if len(neighbor_distance) > 15:
					     max_index = neighbor_distance.index(max(neighbor_distance)) 
					     neighbor_distance.remove(neighbor_distance[max_index])
					     neighbor_name.remove(neighbor_name[max_index])
     
		if wall:
			distance_wall = min(math.fabs(checkHouse.location.getX()+0.5*checkHouse.spec[0]+checkHouse.spec[2]-self.width),
								math.fabs(checkHouse.location.getX()-0.5*checkHouse.spec[0]-checkHouse.spec[2]),
								math.fabs(checkHouse.location.getY()+0.5*checkHouse.spec[1]+checkHouse.spec[2]-self.depth),
								math.fabs(checkHouse.location.getY()-0.5*checkHouse.spec[1]-checkHouse.spec[2]))
			all_distances.append(distance_wall)
		return (min(all_distances), neighbor_name)


	def getTotalVrijstand(self):
		"""
		Input:
		None
		Return:
		Total vrijstand as float.
		Purpose:
		Calculates the total vrijstand of the land.
		"""
		# set initial vrijstand to zero
		vrijstand = 0
		# loops trough all houses and adds vijstand
		for key,house in self.land.iteritems():
			vrijstand += house.getHouseVrijstand()
		# prints total vrijstand
		print "Total vrijstand is          :", vrijstand
		return vrijstand 


	def getTotalValue(self):
		"""
		Input:
		None
		Return:
		Total value as float.
		Purpose:
		Calculates the total value of the land.
		"""
		total_val = 0
		# loops trough all houses and adds value
		for key,house in self.land.iteritems():
			house.addVrijstand()   
			total_val += house.getHouseValue()[0]
   
		return total_val


	def getHouses(self):
		"""
		Input:
		None
		Return:
		List of all house objects on the land.
		Purpose:
		Getting all house objects on the given land.
		"""
		return self.land
  
  
	def getRandomPosition(self):
		"""
		Input:
		None
		Return:
		Positon object with a position on the land.
		Purpose:
		Getting a random position on the land.
		"""
		random_pos = Position(random.randint(0, self.width), random.randint(0, self.depth))
		return random_pos	


class House(object):
	"""
	Represents a house located on the field.

	House object must be located within the areas of the field at all times
	Probably needs some method to move the house to a different location and
	subsequently re-evaluate the score.
	"""
	def __init__(self, land, width, depth, value, bonus, min_dist, location, vrijstand = 0, name = None, neighbor = [], total_val = 0, old_val = 0):
		self.land = land
		self.width = width
		self.depth = depth
		self.value = value
		self.bonus = bonus
		self.min_dist = min_dist
		self.location = location
		self.vrijstand = vrijstand
		self.name = name
		self.neighbor = neighbor
		self.total_val = total_val  
		self.old_val = old_val
		self.spec = [self.width, self.depth, self.min_dist]


	def setHousePosition(self,position):
		"""
		Input:
		Position object.
		Return:
		None
		Purpose:
		Setting a house at a given position on a land and saving this position
		as the houses location.
		"""
		self.location = position
		self.land.markLandAtPosition(self) 
		return 0


	def isPositionInLand(self, position):
		"""
		Input:
		Location is a position object.
		Return:
		True if given position is in the land, false if it is not.
		Purpose:
		Evaluation whether a given position is in the land and if a given 
		type of house (within specifications) can be set there.
		"""
		# Obtain minimum x and y coordinates
		x_coordinate = self.width/2 + self.min_dist
		y_coordinate = self.depth/2 + self.min_dist

		# Check if all the corners of the houses are in the land
		if (position.getX() >= x_coordinate and 
		    position.getX() <= self.land.getWidth() - x_coordinate and
		    position.getY() >= y_coordinate and
		    position.getY() <= self.land.getDepth() - y_coordinate):
			return True
		return False


	def addHouseName(self, name):
		"""
		Input:
		Name string.
		Return:
		None
		Purpose:
		Adding a name to a house. Name is in format "x_position-y_position".
		"""
		self.name = name
		return 0
  
	def getHouseName(self):
		"""
		Input:
		None.
		Return:
		Name of house.
		Purpose:
		Returning the name of the house.
		"""
		return self.name
  
  
	def getHouseNeighbor(self):
		"""
		Input:
		None.
		Return:
		Name of neighbor house.
		Purpose:
		Returning the name of the house with the minimum distance to this house.
		"""
		return self.neighbor
  
  
	def addVrijstand(self):
		"""
		Input:
		None.
		Return:
		None.
		Purpose:
		Adding bonus vrijstand and name of neighbor to house.
		"""
		# Create a random location
		self.vrijstand = self.land.getVrijstand(self)[0]
		self.neighbor = self.land.getVrijstand(self)[1]
		return 0


	def getHouseVrijstand(self):
		"""
		Input:
		None.
		Return:
		Returning vijstand of given house as tuple. The first part is the 
		actual vijstand as float and the second element the name of the neighbor. 
		Purpose:
		Getting vijstand of house and name of neighbor.
		"""
		return self.vrijstand


	def checkHousePosition(self, position):
		"""
		Input:
		Position object.
		Return:
		Return true if position is viable and false if not. 
		Purpose:
		Evaluating if a position is viable with regard to whether position
 		is on the land and not within minimum distance of another house. 
		"""
		# checks if position is on land
		if self.isPositionInLand(position):
			# checks if the position is vaible.
		    if self.land.checkPosition(position, self.getHouseSpecs()):
				return True
		# return False is the location is not viable
		return False
  
  
	def getHouseSpecs(self):
		"""
		Input:
		None.
		Return:
		Returning the specifications of the house, [width, depth, min_dist]. 
		Purpose:
		Getting the specifications of a given house.
		"""
		return self.spec
  
  
	def getMaxBorderDistance(self):
		"""
		Input:
		None.
		Return:
		Maximum distance to a border of the land.
		Purpose:
		Getting the vijstand for a single house on a land.
		!Possibly a useless function! (purpose is testing)
		"""
		# edges of the land
		land_edges = ((0,0),(self.land.getWidth(),0),(self.land.getWidth(),
                 self.land.getDepth()),(0,self.land.getDepth()))
  		# edges of the house                    
		house_edges = self.getEdges()
		distances = []
   		# calculating distance between house and land edges
		for edgeL in land_edges:
		    min_distance = None      
		    for edgeH in house_edges:
				distance = calculateDistance(edgeL[0],edgeL[1],edgeH[0],edgeH[1])
				# getting minimum distance between house and land edges
				if distance < min_distance or min_distance == None:
					min_distance = distance
		    distances.append(min_distance)
		return max(distances)

	def getHouseValue(self):
		"""
		Input:
		None.
		Return:
		Value with bonus vrijstand and without bonus vijstand in tuple as floats.
		Purpose:
		Calculation the value of the house.
		"""     
		self.old_val = self.total_val     
		vrijstand = self.vrijstand
		self.total_val = self.value * (1 + vrijstand * self.bonus)
		return (self.total_val, self.value)

	def getOldHouseValue(self):
		"""
		Input:
		None.
		Return:
		Location of house as position object.
		Purpose:
		Returning the location of the center of the house.
		""" 
		return self.old_val
  
	def getHousePosition(self):
		"""
		Input:
		None.
		Return:
		Location of house as position object.
		Purpose:
		Returning the location of the center of the house.
		""" 
		return self.location
  
	def getEdges(self):
		"""
		Input:
		None.
		Return:
		All edges of the given house object in a tuple in the format:
		(left_top,right_top,right_bottom,left_bottom)
		Purpose:
		Getting all edges of a house.
		""" 
		x_val = self.location.getX()
		y_val = self.location.getY()
  
 		left_bottom = (x_val - (self.width/2), y_val + (self.depth/2))
 		right_bottom = (x_val + (self.width/2), y_val + (self.depth/2))
 		left_top = (x_val - (self.width/2), y_val - (self.depth/2))
 		right_top = (x_val + (self.width/2), y_val - (self.depth/2))   
		return (left_top,right_top,right_bottom,left_bottom)


	def updatePosition(self, randomUpdate = False):
    		"""
		Input:
		RandomUpdate boolian, if set to true, house gets new position
		even without increase of value.
		Return:
		None.
		Purpose:
		Checks if the location is in the field with isPositionInLand
		Checks if any other house is already in this location with checkPosition
		Checks if the value of the house increases.
		""" 
		# saving old position
		old_pos = self.location
		#old_value = self.getHouseValue()[0]
		# removing old position from land
		self.land.removeLandAtPosition(self)
		# create a new position
		if randomUpdate:
			self.location = self.location.getNewPosition(random.uniform(4,6))
		else:
			self.location = self.location.getNewPosition(0.5)
		new_pos = self.location
		# checks is the position is in land
		if self.isPositionInLand(new_pos):
			# checks if all minimum distances are met  
			if self.land.checkPosition(new_pos, self.spec):
				#self.location = new_pos
				self.land.markLandAtPosition(self)
				self.addVrijstand()
 				value_change = self.getHouseValue()[0] - self.getOldHouseValue()
 				for neighbor in self.getHouseNeighbor():
					house = self.land.getHouses()[neighbor]
					house.addVrijstand()
 					value_change += house.getHouseValue()[0] - house.getOldHouseValue()   
				# if new value is higher, move house to new position  
				if value_change > 0 or randomUpdate:
				# if new value is higher, move house to new position 
					return value_change
				# if randomUpdate is switched on, move even without
				# value increase
				else:
					self.land.removeLandAtPosition(self)
					self.location = old_pos
					self.land.markLandAtPosition(self)
					# update all neighbors with old vrijstand
					# getTotalValue loops trough all houses and updates vrijstand and value    
					self.land.getTotalValue()
					return 0
		# if no one of the location criterea failed, move to old position
		self.location = old_pos
 		# mark house at old position again 
		self.land.markLandAtPosition(self)
		return 0
 
class NewVisualisation(object):
	def __init__(self, num_houses, width, height, delay = 0.05):
		# Initialise variables
		self.delay = delay
		self.width = width
		self.height = height
		self.num_houses = num_houses

		# Create the canvas
		self.master = Tk()
		self.w = Canvas(self.master, width=800, height=1000)
		self.w.pack()
		self.master.update()
		self.w.create_rectangle(40, 40, 520, 680, fill="green", width=0)

		# Labels for the output
		lbl = Label(self.master, text="Current land value:")
		lbl.place(x=550, y=35)
		self.var = StringVar()
		self.label = Label(self.master, textvariable=self.var)
		self.label.place(x=550, y=55)

		self.time = 0
		self.master.update()

	def draw_houses(self, inputs):
		"""
		Draws the houses
		"""
		scaling = 40
		for keys, coordinates in inputs[1].iteritems():  
			if coordinates.getHouseSpecs() == [8.0, 8.0, 2.0]:
				self.w.create_rectangle(scaling+(coordinates.getHousePosition().getX()-4)*4, 
								   scaling+(coordinates.getHousePosition().getY()-4)*4, 
								   scaling+(coordinates.getHousePosition().getX()+4)*4, 
								   scaling+(coordinates.getHousePosition().getY()+4)*4, fill ="Blue")
				self.w.create_text(scaling+(coordinates.getHousePosition().getX())*4,
							 scaling+(coordinates.getHousePosition().getY())*4, text = keys)
			elif coordinates.getHouseSpecs() == [10.0, 7.5, 3.0]:
				self.w.create_rectangle(scaling+(coordinates.getHousePosition().getX()-5)*4, 
								   scaling+(coordinates.getHousePosition().getY()-3.75)*4, 
								   scaling+(coordinates.getHousePosition().getX()+5)*4, 
								   scaling+(coordinates.getHousePosition().getY()+3.75)*4, fill ="Red")
				self.w.create_text(scaling+(coordinates.getHousePosition().getX())*4,
							 scaling+(coordinates.getHousePosition().getY())*4, text = keys)
			else:
				self.w.create_rectangle(scaling+(coordinates.getHousePosition().getX()-5.5)*4, 
								   scaling+(coordinates.getHousePosition().getY()-5.25)*4, 
								   scaling+(coordinates.getHousePosition().getX()+5.5)*4, 
								   scaling+(coordinates.getHousePosition().getY()+5.25)*4, fill ="Yellow")
				self.w.create_text(scaling+(coordinates.getHousePosition().getX())*4,
							 scaling+(coordinates.getHousePosition().getY())*4, text = keys)

	def update(self, inputs):
		"""
		Updates the GUI
		"""
		self.w.create_rectangle(40, 40, 520, 680, fill="green", width=0)
		self.draw_houses(inputs)
		self.var.set(int(inputs[0]))
		self.time += 1
		self.master.update()
		time.sleep(self.delay)

	def done(self):
		"""
		NO IDEA
		"""
		mainloop()

	def stop(self):
		"""
		Quits the GUI
		"""
		time.sleep(3)
		self.master.destroy()

def Visualisation(inputs):
	"""
	Input:
 	Inputs is tuple with list of best solution houses and land.
	Return:
	GUI
	Purpose:
	Displays the GUI of the field with houses.
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

	# Plot the houses. NOTE, because the scaling is 40 pixels for 10 meters, 
	# it is 4 pixels for 1 meter
	for keys, coordinates in inputs[1].iteritems():  
		if coordinates.getHouseSpecs() == [8.0, 8.0, 2.0]:
			w.create_rectangle(scaling+(coordinates.getHousePosition().getX()-4)*4, 
							   scaling+(coordinates.getHousePosition().getY()-4)*4, 
							   scaling+(coordinates.getHousePosition().getX()+4)*4, 
							   scaling+(coordinates.getHousePosition().getY()+4)*4, fill ="Blue")
 			w.create_text(scaling+(coordinates.getHousePosition().getX())*4,
							 scaling+(coordinates.getHousePosition().getY())*4, text = keys)
		elif coordinates.getHouseSpecs() == [10.0, 7.5, 3.0]:
			w.create_rectangle(scaling+(coordinates.getHousePosition().getX()-5)*4, 
							   scaling+(coordinates.getHousePosition().getY()-3.75)*4, 
							   scaling+(coordinates.getHousePosition().getX()+5)*4, 
							   scaling+(coordinates.getHousePosition().getY()+3.75)*4, fill ="Red")
 			w.create_text(scaling+(coordinates.getHousePosition().getX())*4,
							 scaling+(coordinates.getHousePosition().getY())*4, text = keys)
		else:
			w.create_rectangle(scaling+(coordinates.getHousePosition().getX()-5.5)*4, 
							   scaling+(coordinates.getHousePosition().getY()-5.25)*4, 
							   scaling+(coordinates.getHousePosition().getX()+5.5)*4, 
							   scaling+(coordinates.getHousePosition().getY()+5.25)*4, fill ="Yellow")
 			w.create_text(scaling+(coordinates.getHousePosition().getX())*4,
							 scaling+(coordinates.getHousePosition().getY())*4, text = keys)

	master.mainloop()

def performancePlots(monitoring):
	"""
	Input:
 	List of total values on all trails and updates.
	Return:
	Performance plots.
	Purpose:
	Producing benchmark plots.
	!NOT DONE YET, has to be improved. Does not account for value decrease (of other houses) while updating houses! 
	"""
 	length = len(monitoring)
   	for j in range(length):
   		pylab.plot(range(len(monitoring[j])), monitoring[j], linewidth=1.0, linestyle="-")
    	pylab.title("Performance Plots")
	pylab.show()
    
def createNewLand(land_dict, variant):
	old_houses = []
	old_land = Land(variant, 120, 160)
	for key, house in land_dict.iteritems():
		# House name and locations
		#old_houses.append((key, house.position.getX(), house.position.getY()))
		if int(key[1:]) <= 3:
			old_houses.append((key, House(old_land, 11.0, 10.5, 610.0, 0.06, 6.0, None), 
						  	  (house.location.getX(), house.location.getY())))
		elif 4 <= int(key[1:]) <= 8:
			old_houses.append((key, House(old_land, 10.0, 7.5, 399.0, 0.04, 3.0, None), 
						  	  (house.location.getX(), house.location.getY())))
		else:
			old_houses.append((key, House(old_land, 8.0, 8.0, 285.0, 0.03, 2.0, None), 
						  	  (house.location.getX(), house.location.getY())))
	# Put houses on land
	old_house = []
	for house_specs in old_houses:
		position = Position(house_specs[2][0], house_specs[2][1])
		house_specs[1].addHouseName(house_specs[0])
		house_specs[1].setHousePosition(position)
		old_house.append(house_specs[1])
	return old_land, old_house

def hillClimber(land, variant, houses, current_value, gui_updates):
	"""
	Hill Climber algorithm
	"""
	# Variables for HC
	house_changes = 1000
	k = 0
	monitoring_help = []
	stop_list = [current_value]

	# Show the GUI
	if gui_updates:
		anim = NewVisualisation(variant, 120, 160)

	# Update some random house. Stop if no significant value increase is seen
	for i in range(house_changes):
		house = random.choice(houses)
		current_value += house.updatePosition()   
		if i%200 == 0 and i > 1:
			k += 1
			stop_list.append(current_value)
			if 100*(stop_list[k]/stop_list[k-1]-1) < 0.1:
				print "Stopped at", i
				break

		# plot list and update the GUI
		monitoring_help.append(current_value)
		if i%50 == 0 and gui_updates:
			anim.update((current_value, land.land))

	if gui_updates:
		anim.stop()
	return land, monitoring_help, current_value

def simulatedAnnealing(land, variant, houses, current_value, gui_updates):
	"""
	SA algorithm
	DOES NOT WORK AT ALL...
	"""
	# Initialise variables
	monitoring_help = []
	k = 0
	redraws = 5
	total_updates = 2000
	redraw = 0
	goback = True

	# Show GUI
	if gui_updates:
		anim = NewVisualisation(variant, 120, 160)

	# First maximization (HC)
	for i in range(3000):
		house = random.choice(houses)
		current_value += house.updatePosition()
		monitoring_help.append(current_value)
		if i%50 == 0 and gui_updates:
			anim.update((current_value, land.land))
	# Use the old land as reference, continue with new land
	good_list = (current_value, land.land)

	while redraw < redraws:
		k += 1
		# This is the current best land, make a copy to work on
		if goback:
			best_land, best_houses = createNewLand(land.land, variant)

		# This section should set the currentvalue and vrijstand of the new land
		current_value = 0
		for house in best_houses:
			house.addVrijstand()
			current_value += house.getHouseValue()[0]

		#print k, current_value
		house = random.choice(best_houses)

		# Allow negative increases half of the time, for half of the total updates
		random_num = 0.0
		if (k%total_updates < total_updates/2) and (random.random() < random.random()):
			current_value += house.updatePosition(True)
		else:
			current_value += house.updatePosition()
		monitoring_help.append(current_value)

		# Vrijstanden arent reverting back... So we go to the old land with new vrijstand.
		# Continues with land.land but houses are changing
		if k%total_updates == 0:
			print current_value
			# Save if this is the best land, continue the simulation with this best land
			if current_value > good_list[0]:
				land = best_land
				good_list = (current_value, land.land)
				goback = False
			# revert to old land by again creating a land which is the best land
			else:
				goback = True
			redraw += 1
			print redraw

		if k%50 == 0 and redraw < redraws and gui_updates:
			anim.update((current_value, best_land.land))

	if gui_updates:
		anim.stop()
	return good_list, monitoring_help

	# We create a copy of the land we are going to work with.

def simulation(algorithm_type, variant, gui_updates, randomizations):
	"""
	Input:
 	None.
	Return:
	List of total values of all trails and updates.
	Purpose:
	I'm going to try and randomize the houses and check if the algorithm we have works
	"""
	# Initialise variables
 	monitoring = []
	good_list = (0, None)
 	start = time.clock()  
	for j in range(randomizations):
		# create land
		m = 1
		monitoring_help = []
		land = Land(variant, 120, 160)
		houses_amount = [house * variant for house in [0.6, 0.25, 0.15]]
		houses = []
		# Add houses to the house list
		for i in range(int(houses_amount[0])):
			houses.append(House(land, 8.0, 8.0, 285.0, 0.03, 2.0, None))

		for i in range(int(houses_amount[1])):
			houses.append(House(land, 10.0, 7.5, 399.0, 0.04, 3.0, None))

		for i in range(int(houses_amount[2])):
			houses.append(House(land, 11.0, 10.5, 610.0, 0.06, 6.0, None))

		# Set all the houses at specific initial locations. If the location is incorrect, keep
		# setting the house untill it is correct
		# more expensive houses are set first
		for house in reversed(houses):
			# get random position on land for house
			position = land.getRandomPosition()
			# if position is good it is kept, otherwise enter loop
			good_loc = house.checkHousePosition(position)
			while good_loc == False:
				# getting new positions until position is viable       
				position = land.getRandomPosition()
				good_loc = house.checkHousePosition(position)
			# placing house on land  
			name = "h" + str(m)
			house.addHouseName(name)
			house.setHousePosition(position)
			m +=1
			#print m

		initial_value = 0
		for house in houses:
			house.addVrijstand()
			# computing value of each house
			initial_value += house.getHouseValue()[0]
			# adding their vijstand and neighbors to houses
		monitoring_help.append(initial_value)

		# Simulated Annealing
		if algorithm_type == "SimulatedAnnealing":
			good_list, monitoring_help = simulatedAnnealing(land, variant, houses, initial_value, gui_updates)

   		# Hill Climber
		elif algorithm_type == "HillClimber":
			land, monitoring_help, total_value = hillClimber(land, variant, houses, initial_value, gui_updates)

			# Check if the previous randomization is better
			if total_value > good_list[0]:
				good_list = (total_value, land.land)
			print j+1, total_value

		# Genetic algorithm
		else:
			pass

		# Monitoring for the graphs
		monitoring.append(monitoring_help)
		if algorithm_type == "SimulatedAnnealing":
			break
	# Visualise the result
 	end = time.clock()
	print "The best solution is           :", "{:,}".format(good_list[0]*1000)
	print "Time elapsed: " +str(round(end - start,2)) +" seconds"
	Visualisation(good_list)

	value_check = 0
	for key, house in good_list[1].iteritems(): 
		value_check += house.getHouseValue()[0]
	print value_check
	return monitoring

def test():
	times = 0
	reps = 20000000
	for i in range(reps):
		if random.random()< random.random():
			times += 1
	print times/float(reps)*100


if __name__ == "__main__":
	gui_updates = True
	#random.seed(3)
	randomizations = 1
	variant = 20
	algorithm1 = "HillClimber"
	algorithm2 = "SimulatedAnnealing"
	algorithm3 = "GeneticAlgorithm"
	monitoring = simulation(algorithm2, variant, gui_updates, randomizations)
	performancePlots(monitoring)
	#test()
