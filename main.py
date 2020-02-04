#IDEAS
#Look at how cliques form, and how this changes based on how "open" people are
#What variables affect the amount of self segregation on random traits seen.
import math
import turtle

class Graph:
	def __init__(self, num_people):
		self.people_list = []
		for x in range(num_people):
			self.people_list.append(Person(x))

	#find the strength of a connection between any two people
	def get_connection_value(self, person1, person2):
		#the person with a higher id stores the connection, which is why we look for the smaller person inside the connection of the bigger person
		return self.people_list[max(person1.id, person2.id)].connections[min(person1.id, person2.id)]

	#
	# value (0 <= int <= 10)
	#
	#
	def set_connection_value(self, person1, person2, value, relative=False):
		if relative:
			self.people_list[max(person1.id, person2.id)].connections[min(person1.id, person2.id)] += value
		else:
			self.people_list[max(person1.id, person2.id)].connections[min(person1.id, person2.id)] = value


	def get_person_by_id(self, personId):
		return self.people_list[personId]

	def display_graph(self):
		SCREEN_WIDTH = 700
		SCREEN_HEIGHT = 600

		num_cols = math.ceil(math.sqrt(len(self.people_list)))
		
		t = turtle.Turtle()
		#doesn't update screen until drawing is done
		turtle.tracer(0, 0)

		for person in self.people_list:
			t.up()
			t.setpos(person.id % num_cols * 100 - SCREEN_WIDTH/2, math.floor(person.id / num_cols) * 100 - SCREEN_HEIGHT/2)
			t.down()
			t.circle(3)

		for x in range(len(self.people_list)):
			for y in range(x + 1, len(self.people_list)):
				person1 = self.get_person_by_id(x)
				person2 = self.get_person_by_id(y)
				if (self.get_connection_value(person1, person2) != 0):
					t.up()
					t.pencolor(*[1 - (self.get_connection_value(person1, person2) / 10) for x in range(3)])
					t.setpos(person1.id % num_cols * 100 - SCREEN_WIDTH/2, math.floor(person1.id / num_cols) * 100 - SCREEN_HEIGHT/2)
					t.down()
					t.setpos(person2.id % num_cols * 100 - SCREEN_WIDTH/2, math.floor(person2.id / num_cols) * 100 - SCREEN_HEIGHT/2)

		turtle.update()
		turtle.done()

class Person:
	def __init__(self, personId):
		self.id = personId
		#so the first person doesn't store any connections. The last person stores their connection with everyone in the game. Makes it easy to add people later.
		#this way every connection is only stored once
		self.connections = [0 for x in range(personId)] 

g = Graph(10)
g.set_connection_value(g.get_person_by_id(1), g.get_person_by_id(2), 10)

g.display_graph()