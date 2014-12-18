# Amstelheage programmeertheorie assignment
# Duncan and Jonathan

import math
import random
import numpy as np
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
        old_x, old_y = self.x, self.y
        new_x, new_y = old_x, old_y
        while new_x ==  old_x and new_y == old_y:
            new_x = old_x + random.sample((-distance_change, 0, distance_change),1)[0]
            new_y = old_y + random.sample((-distance_change, 0, distance_change),1)[0]
        
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


    def markLandAtPosition(self, house):
        """
        Input:
        House is a house object.
        Return:
        None
        Purpose:
        Appends the location to the dictionary of locations where the land is occupied.
        """
        name = house.name
        self.land[name] = house
        return self


    def removeLandAtPosition(self, house):
        """
        Input:
        House is a house object.
        Return:
        None
        Purpose:
        Removes the location from the dictionary.  
        """
        name = house.name
        del self.land[name]
        return self


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
        # getting all corners of both houses  
        corners1 = house1.getCorners()
        corners2 = house2.getCorners()
        # computing minimum distance between houses 
        return rect_distance((corners1[3][0],corners1[3][1],corners1[1][0],corners1[1][1])
                            ,(corners2[3][0],corners2[3][1],corners2[1][0],corners2[1][1]))   
     
    def getVrijstand(self, checkHouse):
        """
        Input:
        CheckHouse is a house object.
        Return:
        Bonus vrijstand as a float (closest neighbor is also saved in the house object).
        Purpose:
        Computing the bonus vrijstand and neighbor of a given house .
        """
        # if wall is set to True, house vrijstand may not lay outside of the land
        wall = False 
        # minimum distance for this type of house
        minimum_distance = checkHouse.spec[2]
        
        # set initial stuff
        smallest_distance = 200
        for key, house in self.land.iteritems():
            if key == checkHouse.name:
                pass
            else:
                distance = self.getMinDistance(checkHouse,house) - minimum_distance
                if distance < smallest_distance:
                    smallest_distance = distance
                    name_neighbor = key

        if wall:
            distance_wall = min(math.fabs(checkHouse.location.x+0.5*checkHouse.spec[0]+checkHouse.spec[2]-self.width),
                                math.fabs(checkHouse.location.x-0.5*checkHouse.spec[0]-checkHouse.spec[2]),
                                math.fabs(checkHouse.location.y+0.5*checkHouse.spec[1]+checkHouse.spec[2]-self.depth),
                                math.fabs(checkHouse.location.y-0.5*checkHouse.spec[1]-checkHouse.spec[2]))
            if distance_wall < smallest_distance:
                smallest_distance = distance_wall
                name_neighbor = name_neighbor
        # closest neighbor of house is saved in the house object
        checkHouse.neighbor = (name_neighbor, smallest_distance)
        return smallest_distance


    def getTotalVrijstand(self):
        """
        Input:
        None
        Return:
        Total area vrijstand as float.
        Purpose:
        Calculates the total vrijstand of the land.
        """
        # set initial vrijstand to zero
        vrijstand = 0
        # loops trough all houses and adds vijstand
        for key,house in self.land.iteritems():
            vrijstand += house.vrijstand
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
        # set initial value to zero
        total_val = 0
        # loops trough all houses and adds value
        for key,house in self.land.iteritems():
            house.addVrijstand()   
            total_val += house.getHouseValue()[0]
        return total_val
  
  
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
    House object must be located within the area with regard to required space of the house
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
        self.corners = None


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
        return self


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
        if (position.x >= x_coordinate and 
            position.x <= self.land.width - x_coordinate and
            position.y >= y_coordinate and
            position.y <= self.land.depth - y_coordinate):
            return True
        return False
  
  
    def addVrijstand(self):
        """
        Input:
        None.
        Return:
        None.
        Purpose:
        Adding bonus vrijstand to house.
        """
        self.vrijstand = self.land.getVrijstand(self)


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
            if self.land.checkPosition(position, self.spec):
                return True
        # return False is the location is not viable
        return False

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
        self.total_val = self.value * (1 + self.vrijstand * self.bonus)
        return (self.total_val, self.value)
    
  
    def getCorners(self):
        """
        Input:
        None.
        Return:
        All corners of the given house object in a tuple in the format:
        (left_top,right_top,right_bottom,left_bottom)
        Purpose:
        Getting all corners of a house.
        """ 
        x_val = self.location.x
        y_val = self.location.y

        left_bottom = (x_val - (self.width/2), y_val + (self.depth/2))
        right_bottom = (x_val + (self.width/2), y_val + (self.depth/2))
        left_top = (x_val - (self.width/2), y_val - (self.depth/2))
        right_top = (x_val + (self.width/2), y_val - (self.depth/2))
        self.corners = (left_top,right_top,right_bottom,left_bottom)   
        return (left_top,right_top,right_bottom,left_bottom)


    def updatePosition(self, vrijstand_type, temperature = 0.124632563, max_temperature = 100):
        """
        Input:
        Vrijstand_type is boolian to determine if value or vrijstand has to be optimized.
        Temperature is a float that represents the actual temperature (in the SA algorithm).
        Max_temperature is float that represents the maximum temperature (mostly equal to max updates)
        Return:
        None.
        Purpose:
        Checks if the location is in the field with isPositionInLand
        Checks if any other house is already in this location with checkPosition
        Checks if the value of the house increases.
        """ 
        # saving old position
        old_pos = self.location
        # removing old position from land
        self.land.removeLandAtPosition(self)
        # create a new position
        if temperature == 0.124632563:
            if random.random() < 0.5:
                self.location = self.location.getNewPosition(random.uniform(1,2))
            else:
                self.location = self.land.getRandomPosition()
        else:
            if random.random() < 0.5:
                self.location = self.location.getNewPosition(5.5-temperature/(max_temperature/5))
            else:
                self.location = self.land.getRandomPosition()
        new_pos = self.location
        # checks is the position is in land
        if self.isPositionInLand(new_pos):
            # checks if all minimum distances are met  
            if self.land.checkPosition(new_pos, self.spec):
                # Check the houses that used to be the closest house to checkhouse 
                # addvrijstand just edits the vrijstand
                # Old values
                self.land.markLandAtPosition(self)
                old_vrijstand = self.vrijstand
                old_total_value = self.total_val
                old_neighbor = self.neighbor
                old_additional = {}
    
                additional = [self.neighbor[0]]
                # Look for houses which have the checkhouse as closest neighbor
                for key, house in self.land.land.iteritems():
                    # Check if house has checkhouse as neighbor and house is not the neighbor
                    if key != additional[0] and house.neighbor[0] == self.name:
                        additional.append(key)

                self.addVrijstand()
                # if condition that determines if value of vrijstand has to optimized
                if vrijstand_type:
                    value_change = self.vrijstand - old_vrijstand
                else:
                    value_change = self.getHouseValue()[0]- self.old_val

                for house_name in additional:
                    house = self.land.land[house_name]
                    old_additional[house_name] = (house.vrijstand, house.total_val, house.neighbor)
                    house.addVrijstand()
                    if vrijstand_type:
                        value_change += house.vrijstand - old_additional[house.name][0]
                    else:
                        value_change += house.getHouseValue()[0]- house.old_val

                # Recheck all th eother houses
                other_houses_list = []
                for key, house in self.land.land.iteritems():
                    # Already updates houses
                    if key in additional or key == self.name:
                        pass
                    else:
                        # Save values, compute distance to moved house
                        new_distance = self.land.getMinDistance(house,self) - house.spec[2]
                        # If this value is smaller, house has a new neighbor
                        if new_distance < house.neighbor[1]:
                            # Save old values
                            other_houses_list.append([house, house.vrijstand, house.total_val, house.neighbor])
                            # Edit new stuff
                            house.neighbor = (self.name, new_distance)
                            house.vrijstand = new_distance
                            if vrijstand_type:
                                value_change += house.vrijstand - other_houses_list[-1][1]
                            else:
                                value_change += house.getHouseValue()[0] - house.old_val

                if vrijstand_type:
                    try:
                        # gives overflow error sometimes, therefore try is used
                        temp_func = math.e**((value_change*1000)/(100-temperature/(float(max_temperature)/100)))
                    except:
                        temp_func = math.e**((value_change*100)/(100-temperature/(float(max_temperature)/100)))
                else:
                    try:
                        # gives overflow error sometimes, therefore try is used
                        temp_func = math.e**(value_change/(100-temperature/(float(max_temperature)/100)))
                    except:
                        temp_func = 1.0
                    
                if value_change > 0 or (random.random() < temp_func and temperature != 0.124632563):
                    return value_change
                else:
                    # MOVE NEIGHBORS BACK...
                    self.land.removeLandAtPosition(self)
                    self.location = old_pos
                    self.land.markLandAtPosition(self)
                    self.vrijstand = old_vrijstand
                    self.total_val = old_total_value
                    self.neighbor = old_neighbor
                    for house_name in additional:
                        house = self.land.land[house_name]
                        house.vrijstand = old_additional[house_name][0]
                        house.total_val = old_additional[house_name][1]
                        house.neighbor = old_additional[house_name][2]
                    for house_data in other_houses_list:
                        house_data[0].vrijstand = house_data[1]
                        house_data[0].total_val = house_data[2]
                        house_data[0].neighbor = house_data[3]
                    return 0
        # if no one of the location criterea failed, move to old position
        self.location = old_pos
         # mark house at old position again 
        self.land.markLandAtPosition(self)
        return 0
 
class NewVisualisation(object):
    """
    NewVisualisation is a class with the purpose of providing a live visualisation.
    """
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
        self.w.create_rectangle(40, 40, 520, 680, fill="#A5E57F", width=0)

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
        Input:
        Inputs is tuple with list of best solution houses and land dictionary.
        Purpose:
        Draws the houses
        """
        scaling = 40
        for keys, coordinates in inputs[1].iteritems():  
            if coordinates.spec == [8.0, 8.0, 2.0]:
                self.w.create_rectangle(scaling+(coordinates.location.x-4)*4, 
                                   scaling+(coordinates.location.y-4)*4, 
                                   scaling+(coordinates.location.x+4)*4, 
                                   scaling+(coordinates.location.y+4)*4, fill ="Blue")
                self.w.create_text(scaling+(coordinates.location.x)*4,
                             scaling+(coordinates.location.y)*4, text = keys)
            elif coordinates.spec == [10.0, 7.5, 3.0]:
                self.w.create_rectangle(scaling+(coordinates.location.x-5)*4, 
                                   scaling+(coordinates.location.y-3.75)*4, 
                                   scaling+(coordinates.location.x+5)*4, 
                                   scaling+(coordinates.location.y+3.75)*4, fill ="Red")
                self.w.create_text(scaling+(coordinates.location.x)*4,
                             scaling+(coordinates.location.y)*4, text = keys)
            else:
                self.w.create_rectangle(scaling+(coordinates.location.x-5.5)*4, 
                                   scaling+(coordinates.location.y-5.25)*4, 
                                   scaling+(coordinates.location.x+5.5)*4, 
                                   scaling+(coordinates.location.y+5.25)*4, fill ="Yellow")
                self.w.create_text(scaling+(coordinates.location.x)*4,
                             scaling+(coordinates.location.y)*4, text = keys)

    def update(self, inputs):
        """
        Input:
        Inputs is tuple with list of best solution houses and land dictionary.
        Purpose:
        Updates the GUI
        """
        self.w.create_rectangle(40, 40, 520, 680, fill="#A5E57F", width=0)
        self.draw_houses(inputs)
        self.var.set(int(inputs[0]))
        self.time += 1
        self.master.update()
        time.sleep(self.delay)

    def done(self):
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
    # Make squares for the land
    for j in range(1,13):
        for i in range(1,17):
            w.create_rectangle(j*scaling, i*scaling, (j+1)*scaling, (i+1)*scaling, fill="#A5E57F", width=0)
            w.pack()
    # Label for explanation
    lbl = Label(text="Green is unfilled land \n Blue is a detached house \n Red is a bungalow \n Yellow is a maison")
    lbl.place(x=550, y=40)
    # Plot the houses. NOTE, because the scaling is 40 pixels for 10 meters, 
    # it is 4 pixels for 1 meter
    for keys, coordinates in inputs[1].iteritems():  
        if coordinates.spec == [8.0, 8.0, 2.0]:
            w.create_rectangle(scaling+(coordinates.location.x-4)*4, 
                               scaling+(coordinates.location.y-4)*4, 
                               scaling+(coordinates.location.x+4)*4, 
                               scaling+(coordinates.location.y+4)*4, fill ="Blue")
            w.create_text(scaling+(coordinates.location.x)*4,
                             scaling+(coordinates.location.y)*4, text = keys)
        elif coordinates.spec == [10.0, 7.5, 3.0]:
            w.create_rectangle(scaling+(coordinates.location.x-5)*4, 
                               scaling+(coordinates.location.y-3.75)*4, 
                               scaling+(coordinates.location.x+5)*4, 
                               scaling+(coordinates.location.y+3.75)*4, fill ="Red")
            w.create_text(scaling+(coordinates.location.x)*4,
                             scaling+(coordinates.location.y)*4, text = keys)
        else:
            w.create_rectangle(scaling+(coordinates.location.x-5.5)*4, 
                               scaling+(coordinates.location.y-5.25)*4, 
                               scaling+(coordinates.location.x+5.5)*4, 
                               scaling+(coordinates.location.y+5.25)*4, fill ="Yellow")
            w.create_text(scaling+(coordinates.location.x)*4,
                             scaling+(coordinates.location.y)*4, text = keys)

    master.mainloop()

def performancePlots(monitoring):
    """
    Input:
    List of total values on all randomizations and updates.
    Return:
    Performance plot
    Purpose:
    Producing benchmark plots. 
    """
    length = len(monitoring)-2
    for j in range(length):
           pylab.plot(range(len(monitoring[j])), monitoring[j], linewidth=1.0, linestyle="-")
    pylab.title("Performance Plots")
    pylab.show()
    

def hillClimber(land, variant, houses, current_value, gui_updates, vrijstand_type, house_changes = 10000):
    """
    Hill Climber algorithm
    """
    # Variables for HC
    k = 0
    monitoring_help = []
    stop_list = [current_value]
    # Show the GUI
    if gui_updates:
        anim = NewVisualisation(variant, 120, 160)
    # Update some random house. Stop if no significant value increase is seen
    for i in range(house_changes):
        house = random.choice(houses)
        current_value += house.updatePosition(vrijstand_type)
        monitoring_help.append(current_value)
        # evaluating whether value change is still big enough to continue
        if i%500 == 0 and i > 1:
            #print i
            k += 1
            stop_list.append(current_value)
            if 100*(stop_list[k]/stop_list[k-1]-1) < 0.1:
                break
                #pass
        # plot list and update the GUI
        if i%50 == 0 and gui_updates:
            anim.update((current_value, land.land))

    if gui_updates:
        anim.stop()
    return land, monitoring_help, current_value


def simulatedAnnealing(land, variant, houses, current_value, gui_updates, vrijstand_type , total_updates = 30000):
    """
    SA algorithm
    """
    # Initialise variables
    monitoring_help = []
    # Show GUI
    if gui_updates:
        anim = NewVisualisation(variant, 120, 160)
    # First maximization (HC)
    for i in range(total_updates):
        house = random.choice(houses)
        # passing the iteration as the temperature and total_updates as the maximum
        # temperature to the updatePosition method
        current_value += house.updatePosition(vrijstand_type, i, total_updates)
        monitoring_help.append(current_value)
        if i%200 == 0 and gui_updates:
            anim.update((current_value, land.land))

    if gui_updates:
        anim.stop()

    return land, monitoring_help, current_value


def geneticAlgorithm(variant, population, gui_updates, generations = 150, survival = True):
    """
   Genetic algorithm
    """
    max_blue = 0.6*variant
    max_red = 0.25*variant
    max_yellow = 0.15*variant
    test = True
    for generation in range(generations):    
        #evaluation
        population = [(elem[0], rounding(elem[1]), elem[2]) for elem in population]
        no_dup = []
        var_list = []
        for elem in population:
            if elem[1] not in var_list:
                no_dup.append(elem)
                var_list.append(elem[1])
        if np.std(var_list) == 0:
            break
        print "Population:", len(no_dup)
        population = no_dup
        population = sorted(population,key=lambda x: x[1], reverse=True)
        # it is determined which candidates survive
        if survival:
            decrease_survival_rate = 0.6/(len(population)-5)
            survival_rate = 0.7
            new_pop = population[:5]
            for pop in population[5:]:
                if random.random() > survival_rate:
                    new_pop.append(pop)
                    survival_rate -= decrease_survival_rate
            population = new_pop
        else:
            population = population[:100]
        print generation+1, population[0][1], population[-1][1]
        #mutation
        population_new = []
        # 25 children are created:
        # 14 by recombination of two lands
        # 6 by a simulated annealing algorithm with 100 updates
        # 5 by a Hill Climber with 10 updates
        for i in range(25):
            parent = random.choice(population)
            # Obtaining new land children by recombination
            if i < 15:
                parent2 = random.choice(population)
                child = createNewLand(parent[0].land, variant)
                recomb_houses = []
                obj1 = random.randint(0,parent[0].depth)
                obj2 = random.randint(0,parent[0].width)
                if test:
                    recomb_land = Land(variant, 120, 160)
                    # the first parent is divided by the x or y axis
                    if random.random() < 0.5:
                        func = lambda x : x.location.y > obj1
                    else:
                        func = lambda x : x.location.x > obj2
                    for name, house in parent[0].land.iteritems():
                        if func(house):
                            for new_house in createHouses(house, recomb_land):
                                recomb_houses.append(new_house)
                    # the second parent is divided by the x or y axis
                    if random.random() < 0.5:
                        func = lambda x : x.location.y <= obj1
                    else:
                        func = lambda x : x.location.x <= obj2
                    for name, house in parent2[0].land.iteritems():
                        if func(house):
                            for new_house in createHouses(house, recomb_land):
                                recomb_houses.append(new_house)

                    j, i, m, blue, red, yellow = 0, len(recomb_houses)-1, 1, 0, 0, 0
                    
                    for k in range(len(recomb_houses)):
                        if k == variant:
                            break
                        if k%2 == 0:
                            house = recomb_houses[j][0]
                            if house.spec[2] == 2.0:
                                blue += 1
                                if blue > max_blue:
                                    blue -= 1
                                    continue
                            elif house.spec[2] == 3.0:
                                red += 1
                                if red > max_red:
                                    red -= 1
                                    continue
                            else:
                                yellow += 1
                                if yellow > max_yellow:
                                    yellow -= 1
                                    continue
                            position = Position(recomb_houses[j][1], recomb_houses[j][2])
                            good_loc = house.checkHousePosition(position)
                            if good_loc == False:
                                continue
                            # placing house on land  
                            name = "h" + str(m)
                            house.name = name
                            house.setHousePosition(position)
                            m += 1
                            j += 1
                        else:
                            house = recomb_houses[i][0]
                            if house.spec[2] == 2.0:
                                blue += 1
                                if blue > max_blue:
                                    blue -= 1
                                    continue
                            elif house.spec[2] == 3.0:
                                red += 1
                                if red > max_red:
                                    red -= 1
                                    continue
                            else:
                                yellow += 1
                                if yellow > max_yellow:
                                    yellow -= 1
                                    continue
                            position = Position(recomb_houses[i][1], recomb_houses[i][2])
                            good_loc = house.checkHousePosition(position)
                            if good_loc == False:
                                continue
                            # placing house on land  
                            name = "h" + str(m)
                            house.name = name
                            house.setHousePosition(position)
                            m += 1
                            i -= 1
                    # reparing if distribution of house types on land is incorrect
                    while blue < max_blue or red < max_red or yellow < max_yellow:
                        if yellow < max_yellow:
                            new_house = House(recomb_land, 11.0, 10.5, 610.0, 0.07, 6.0, None)
                            yellow += 1
                        elif red < max_red:
                            new_house = House(recomb_land, 10.0, 7.5, 399.0, 0.04, 3.0, None)
                            red += 1
                        else:
                            new_house = House(recomb_land, 8.0, 8.0, 285.0, 0.04, 2.0, None)
                            blue += 1
                        position = recomb_land.getRandomPosition()
                        # if position is good it is kept, otherwise enter loop
                        good_loc = new_house.checkHousePosition(position)
                        # at the 40 (but rarely) and 60 houses scenario it could be the case
                        # that no empty position is found to set a house
                        # therefore a time limit is applied, if the search for a 
                        # new position exceeds the time limit, the child land is discarded
                        while_start = time.clock()
                        while_end = time.clock()
                        while good_loc == False and while_end - while_start < 0.1:
                        # getting new positions until position is viable       
                            position = recomb_land.getRandomPosition()
                            good_loc = new_house.checkHousePosition(position)
                            while_end = time.clock()
                        # placing house on land  
                        if while_end - while_start < 0.1:
                            name = "h" + str(m)
                            new_house.name = name
                            new_house.setHousePosition(position)
                            m +=1

                    total_value = recomb_land.getTotalValue()
                    population_new.append((recomb_land, total_value, recomb_land.land))
            # obtaining land children by applying 100 SA algorithm updates
            elif i > 14 and i < 21:
                child = createNewLand(parent[0].land, variant)
                sa_child = simulatedAnnealing(child[0], variant, child[1], child[0].getTotalValue(), gui_updates, False, 100)
                population_new.append((sa_child[0], sa_child[2], sa_child[0].land))
            # obtaining land children by applying 10 HC algorithm updates
            else:   
                child = createNewLand(parent[0].land, variant)
                hill_child = hillClimber(child[0], variant, child[1], child[0].getTotalValue(), gui_updates, False, 10)
                population_new.append((hill_child[0], hill_child[2], hill_child[0].land))
                    
        population = population + population_new

    population = sorted(population,key=lambda x: x[1], reverse=True)
    return population[0][0],population[0][1],population[0][2]
    

def rounding(number, base = 2):
    """
    Rounding function, used for genetic algorithm.
    """
    return int(base * round(float(number)/base))


def createHouses(house, recomb_land):
    """
    Input:
    House is house object that should be duplicated.
    Recomb_land is land object where the house should be placed on.
    Return:
    A list with the duplicated house.
    Purpose:
    The purpose is to easily duplicate a house (and subsequently a land) 
    without having to do a deep.copy.
    """
    recomb_houses = []
    if house.spec[2] == 6.0:
        recomb_houses.append((House(recomb_land, 11.0, 10.5, 610.0, 0.07, 6.0, None), 
                             house.location.x, house.location.y))
    elif house.spec[2] == 3.0:
        recomb_houses.append((House(recomb_land, 10.0, 7.5, 399.0, 0.04, 3.0, None), 
                         house.location.x, house.location.y))
    else:
        recomb_houses.append((House(recomb_land, 8.0, 8.0, 285.0, 0.04, 2.0, None), 
                         house.location.x, house.location.y))
    return recomb_houses    
    
    
def createNewLand(land_dict, variant):
    """
    Input:
    Land_dict is a land dictionary that should be duplicated.
    Variant is the applied scenario; the integer 20, 40 or 60
    Return:
    A land object that is a duplication of the input land dictionary with the
    associated house objects.
    Purpose:
    The purpose is to easily duplicate a land
    without having to do a deep.copy.
    """
    old_houses = []
    old_land = Land(variant, 120, 160)
    for key, house in land_dict.iteritems():
        # House name and locations
        if house.spec[2] == 6.0:
            old_houses.append((key, House(old_land, 11.0, 10.5, 610.0, 0.06, 6.0, key), 
                                (house.location.x, house.location.y), house.neighbor, house.total_val, house.vrijstand))
        elif house.spec[2] == 3.0:
            old_houses.append((key, House(old_land, 10.0, 7.5, 399.0, 0.04, 3.0, key), 
                                (house.location.x, house.location.y), house.neighbor, house.total_val, house.vrijstand))
        else:
            old_houses.append((key, House(old_land, 8.0, 8.0, 285.0, 0.03, 2.0, key), 
                                (house.location.x, house.location.y), house.neighbor, house.total_val, house.vrijstand))
        
    old_house = []
    for house_specs in old_houses:
        position = Position(house_specs[2][0], house_specs[2][1])
        house_specs[1].name = house_specs[0]
        house_specs[1].setHousePosition(position)
        house_specs[1].neighbor = house_specs[3]
        house_specs[1].total_val = house_specs[4]
        house_specs[1].vrijstand = house_specs[5]
        old_house.append(house_specs[1])
    return old_land, old_house
    

def simulation(algorithm_type, variant, gui_updates, randomizations, vrijstand_type, advanced):
    """
    Input:
    None.
    Return:
    List of total values of all trails and updates.
    Purpose:
    Run a simulation of Amstelhaege case with a chosen algorithm. 
    """
    if algorithm_type == "GeneticAlgorithm":
        population = []
        randomizations = 100
    # Initialise variables
    monitoring = []
    end_list = []
    mean_list = []
    good_list = (0, None)
    bad_list = ("inf", None)
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
            if advanced:
                houses.append(House(land, 8.0, 8.0, 285.0, 0.04, 2.0, None))
            else:
                houses.append(House(land, 8.0, 8.0, 285.0, 0.03, 2.0, None))

        for i in range(int(houses_amount[1])):
            if advanced:
                houses.append(House(land, 10.0, 7.5, 399.0, 0.05, 3.0, None))
            else:
                houses.append(House(land, 10.0, 7.5, 399.0, 0.04, 3.0, None))

        for i in range(int(houses_amount[2])):
            if advanced:
                houses.append(House(land, 11.0, 10.5, 610.0, 0.07, 6.0, None))
            else:
                houses.append(House(land, 11.0, 10.5, 610.0, 0.06, 6.0, None))

        # Set all the houses at specific initial locations. If the location is incorrect, keep
        # setting the house untill it is correct
        # more expensive houses are set first
        for house in reversed(houses):
             # Uncomment and provide begin position if houses should not be placed randomly.
             #   position = [Position(12,12),Position(60,12),Position(108,12),Position(36,24) ,
             #               Position(84,24),Position(12,40),Position(60,40),Position(108,40),Position(36,52)][m-1]
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
            house.name = name
            house.setHousePosition(position)
            m +=1
        initial_value = 0
        for house in houses:
            house.addVrijstand() 
            if vrijstand_type:
                initial_value += house.vrijstand
            else:    
                initial_value += house.getHouseValue()[0]
        monitoring_help.append(initial_value)
        
        # Genetic
        if algorithm_type == "GeneticAlgorithm":
            population.append((land, initial_value, houses))
            continue
        # Simulated Annealing
        if algorithm_type == "SimulatedAnnealing":
            #land, monitoring_help, total_value = simulatedAnnealing(land, variant, houses, initial_value, gui_updates)
            land, monitoring_help, total_value = simulatedAnnealing(land, variant, houses, initial_value, gui_updates, vrijstand_type)
            mean_list.append(total_value)
        # Hill Climber
        elif algorithm_type == "HillClimber":
            #land, monitoring_help, total_value = hillClimber(land, variant, houses, initial_value, gui_updates)
            land, monitoring_help, total_value = hillClimber(land, variant, houses, initial_value, gui_updates, vrijstand_type)
            mean_list.append(total_value)
        # Without algorithm
        if algorithm_type == "Nothing":
            total_value = initial_value
            
        # Check if the previous randomization is better
        if total_value > good_list[0]:
            good_list = (total_value, land.land, land, monitoring_help)
        print j+1, total_value
        if total_value < bad_list[0]:
            bad_list = (total_value, land.land, land, monitoring_help)

        # Monitoring for the graphs
        end_list.append(total_value)
        #monitoring.append(monitoring_help)

    if algorithm_type == "GeneticAlgorithm":
        land, total_value, houses = geneticAlgorithm(variant, population, gui_updates)
        good_list = (total_value, land.land, land)
    end = time.clock()

    # Printing relevant values
    print "The best solution is           :", "{:,}".format(good_list[0]*1000)
    print "Time elapsed: " +str(round(end - start,2)) +" seconds"
    print "MEAN OF THE ALGORITHM", np.mean(mean_list)
    
    value_check = 0
    for key, house in good_list[1].iteritems():
        print "House, (neighbor, vrijstand):   ", key, house.neighbor, round(house.vrijstand,2)
    vrijstand_check = 0
    if vrijstand_type:
        for key, house in good_list[1].iteritems():
            vrijstand_check += house.vrijstand
        print "Vrijstand: ",vrijstand_check
    else:
        for key, house in good_list[1].iteritems():
            value_check += house.getHouseValue()[0]
        print "Value: ", value_check
    # visualize final result
    Visualisation(good_list)
    # computing standard error is applicable
    print "Standard error: ", np.std(end_list)
    
    if algorithm_type != "GeneticAlgorithm":
        monitoring.append(good_list[3])
        monitoring.append(bad_list[3])
        monitoring.append(good_list[2])
        monitoring.append(end_list)
    else:
        monitoring.append(good_list[2])
        monitoring.append(good_list[0])
        monitoring.append(good_list[1])
    return monitoring

if __name__ == "__main__":
    """
    Controlling simulation parameters
    """
    # Advanced case: adding 1% to the bonus value computation 
    advanced = False
    # If vrijstand_type is true, vijstand is optimized, otherwise value
    vrijstand_type = False
    # if true, an updating GUI is visualizing the algorithm
    gui_updates = True
    # if true, file output is generated
    output = False
    # if true, performance plots are displayed    
    performance = False
    
    # seeding simulations
    seed = "random" #1234321
    if seed == "random":
        random.seed()
    else:
        random.seed(seed)
    # amount of randomiztions can be chosen:
    randomizations = 1
    # which scenario should be ran
    variant = 20
    algorithm1 = "HillClimber"
    algorithm2 = "SimulatedAnnealing"
    algorithm3 = "GeneticAlgorithm"
    algorithm4 = "Nothing"
    use_algorithm = algorithm2
    monitoring = simulation(use_algorithm, variant, gui_updates, randomizations, vrijstand_type, advanced)
    
    rand_range = randomizations
    if use_algorithm != algorithm3:
        values = monitoring[3]
        best_list = (monitoring[0][-1],seed)
        
    
    """
    #This part has to be uncommented if different seeds should be tested (for replications)
      
    values = []
    rand_range = 250
    best_list = [0, None]
    for i in range(rand_range):
        print i+1
        k = random.randint(10,100000000)
        random.seed(k)
        randomizations = 1
        variant = 20
        algorithm1 = "HillClimber"
        algorithm2 = "SimulatedAnnealing"
        algorithm3 = "GeneticAlgorithm"
        algorithm4 = "Nothing"
        use_algorithm = algorithm3
        monitoring = simulation(use_algorithm, variant, gui_updates, randomizations, vrijstand_type, advanced)
        if use_algorithm == algorithm3:
            values.append(monitoring[1])
            if monitoring[1] > best_list[0]:
                best_list = (monitoring[1], k)
        else:
            values.append(monitoring[0][-1])
            if monitoring[0][-1] > best_list[0]:
                best_list = (monitoring[0][-1], k)
    print best_list
    """
    
    if performance:
        performancePlots(monitoring)
    
    if output:
        if use_algorithm == algorithm3:
            house_coordinates = []
            
            for i in range(1,variant+1):
                house = monitoring[0].land['h'+str(i)]
                house_coordinates.append('Position(' + str(house.location.x) + ',' + str(house.location.y)+')')
            print house_coordinates
            outfile = open("Output_Var"+str(variant)+"_Rand"+str(randomizations)+"_Algo"+str(use_algorithm)+"_Val"+str(best_list[0])+".txt", "w")
            outfile.write(",".join(house_coordinates))
            outfile.close()
            values_str = []
            for value in values:
                values_str.append(str(value))
            valuefile = open("Values_RandRange"+str(rand_range)+"_BestSeed"+str(best_list[1])+"_Var"+str(variant)+"_Rand"+str(randomizations)+"_Algo"+str(use_algorithm)+"_Val"+str(best_list[0])+".txt", "w")
            valuefile.write("\n".join(values_str))
            valuefile.close()
        else:
            house_coordinates = []
            
            for i in range(1,variant+1):
                house = monitoring[2].land['h'+str(i)]
                house_coordinates.append('Position(' + str(house.location.x) + ',' + str(house.location.y)+')')
            print house_coordinates
            outfile = open("Output_Var"+str(variant)+"_Rand"+str(randomizations)+"_Algo"+str(use_algorithm)+"_Val"+str(best_list[0])+".txt", "w")
            outfile.write(",".join(house_coordinates))
            outfile.close()
            values_str = []
            for value in values:
                values_str.append(str(value))
            valuefile = open("Values_RandRange"+str(rand_range)+"_BestSeed"+str(best_list[1])+"_Var"+str(variant)+"_Rand"+str(randomizations)+"_Algo"+str(use_algorithm)+"_Val"+str(best_list[0])+".txt", "w")
            valuefile.write("\n".join(values_str))
            valuefile.close()
