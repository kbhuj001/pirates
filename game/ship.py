
import random
from game.crewmate import *
from game.location import *
from game.context import Context

class Ship (Context):

	def __init__(self):
		super().__init__()
		self.hx = 0
		self.hy = 0
		self.medicine = 5
		self.crew = []
		self.food = 100
		self.loc = None
		n = random.randrange(3,7)
		for i in range (0,n):
			c = CrewMate()
			self.crew.append (c)
			self.nouns[c.get_name()] = c

		self.verbs['anchor'] = self
		self.verbs['north'] = self
		self.verbs['south'] = self
		self.verbs['east'] = self
		self.verbs['west'] = self
		self.verbs['give'] = self


	def process_verb (self, verb, cmd_list, nouns):
		if (verb == "north"):
			self.hx = -1
			self.hy = 0
		elif (verb == "south"):
			self.hx = 1
			self.hy = 0
		elif (verb == "east"):
			self.hx = 0
			self.hy = 1
		elif (verb == "west"):
			self.hx = 0
			self.hy = -1
		elif (verb == "anchor"):
			self.hx = 0
			self.hy = 0
		elif (verb == "give"):
			# give medicine to crewmember
			if (len(cmd_list) > 3):
				if ((cmd_list[1] == "medicine") and (cmd_list[3] in nouns.keys())):
					if (self.medicine > 0):
						nouns[cmd_list[3]].receive_medicine(1)
						self.medicine =  self.medicine - 1
					else:
						print ("no more medicine to give")
		else:
			print ("Error: Ship object doe not understand verb " + verb)


	def print (self):
		print ("ship is at: " + str(self.loc.get_x()) + ", " + str(self.loc.get_y()))
		if ((self.hx==0) and (self.hy==0)):
			print ("ship anchored")
		elif ((self.hx == 1) and (self.hy == 0)):
			print ("ship heading is east")
		elif ((self.hx == -1) and (self.hy == 0)):
			print ("ship heading is west")
		elif ((self.hx == 0) and (self.hy == 1)):
			print ("ship heading is north")
		elif ((self.hx == 0) and (self.hy == -1)):
			print ("ship heading is south")

		print ("ship has " + str (self.medicine) + " medicine")

		for crew in self.crew:
			crew.print()

	def get_loc (self):
		return self.loc

	def set_loc (self, loc):
		self.loc = loc

	def start_day (self, world):
		# crew members eat
		for crew in self.crew:
			crew.start_day (self)

	def get_food (self):
		return self.food

	def take_food (self, amt):
		self.food = self.food - amt

	def get_crew (self):
		return self.crew

	def end_day (self, world):

		if ((self.hx != 0) or (self.hy != 0)):
			# find the destination
			new_loc = world.get_loc (self.loc.get_x()+self.hx, self.loc.get_y()+self.hy)

			# change our location
			self.set_loc (new_loc)

			# tell the new location that we entered
			new_loc.enter(self)