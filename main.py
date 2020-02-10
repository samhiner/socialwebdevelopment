#IDEAS
#Look at how cliques form, and how this changes based on how "open" people are
#What variables affect the amount of self segregation on random traits seen.

#this models people coming into contact with "mutual" friends bc they sit with a friend who is sitting with a mutual friend
#we can examine how different amounts of people that are open/not open to strangers changes the cliquey-ness of the final graph
#
#
import math
import turtle
import random
import time

LAZINESS = 3 #not actual laziness, 
ALONE_TENDENCY = -2
SEATED_ALONE_TENDENCY = -10
STRANGER_LIKE_OPTIONS = [0, -1.5] #if you are making >2 options, edit Person.init()
STRANGER_LIKE_PROBS = [0.2, 0.8]
TABLE_CAPACITY = 5
CONNECTION_LIKELIHOOD = 0.7
CONNECTION_DECREASE_DAYS = 7
MAX_FRIEND_VALUE = 10

NUM_PEOPLE = 20
TURNS = 100

#for turtle
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

class Graph:
	def __init__(self, num_people):
		self.people_list = []
		for x in range(num_people):
			self.people_list.append(Person(x))

	#find the strength of a connection between any two people
	def get_connection_value(self, person1id, person2id):
		#the person with a higher id stores the connection, which is why we look for the smaller person inside the connection of the bigger person
		return self.people_list[max(person1id, person2id)].connections[min(person1id, person2id)]

	#doesn't do anything if value would be greater than max value
	# value (0 <= int <= 10)
	#
	#
	def set_connection_value(self, person1id, person2id, value, relative=False):
		if relative:
			value = self.people_list[max(person1id, person2id)].connections[min(person1id, person2id)] + value

		if value <= MAX_FRIEND_VALUE:
			self.people_list[max(person1id, person2id)].connections[min(person1id, person2id)] = value


	def get_person_by_id(self, personId):
		return self.people_list[personId]

	def display(self, last_frame = False):
		num_cols = math.ceil(math.sqrt(len(self.people_list)))
		
		t = turtle.Turtle()
		#doesn't update screen until drawing is done
		turtle.tracer(0, 0)

		for person in self.people_list:
			t.up()
			t.setpos(person.id % num_cols * 100 - SCREEN_WIDTH/2, math.floor(person.id / num_cols) * 100 - SCREEN_HEIGHT/2)
			t.down()
			t.fillcolor(person.color)
			t.begin_fill()
			t.circle(3)
			t.end_fill()

		for x in range(len(self.people_list)):
			for y in range(x + 1, len(self.people_list)):
				person1 = self.get_person_by_id(x)
				person2 = self.get_person_by_id(y)
				if (self.get_connection_value(x, y) != 0):
					t.up()
					t.pencolor(*[1 - (self.get_connection_value(x, y) / MAX_FRIEND_VALUE) for a in range(3)])
					t.setpos(x % num_cols * 100 - SCREEN_WIDTH/2, math.floor(x / num_cols) * 100 - SCREEN_HEIGHT/2)
					t.down()
					t.setpos(y % num_cols * 100 - SCREEN_WIDTH/2, math.floor(y / num_cols) * 100 - SCREEN_HEIGHT/2)

		t.up()
		t.setpos(SCREEN_WIDTH, SCREEN_HEIGHT)
		turtle.update()
		#time.sleep(1)

		if not last_frame:
			t.clear()

	def clear_seating(self):
		for person in self.people_list:
			person.table = None

	def fade_connections(self):
		for x in range(len(self.people_list)):
			for y in range(x + 1, len(self.people_list)):
				if self.get_connection_value(self.people_list[x].id, self.people_list[y].id) > 0:
					self.set_connection_value(self.people_list[x].id, self.people_list[y].id, -1, relative=True)

class Person:
	def __init__(self, personId):
		self.id = personId
		#so the first person doesn't store any connections. The last person stores their connection with everyone in the game. Makes it easy to add people later.
		#this way every connection is only stored once
		self.connections = [0 for x in range(personId)]
		self.stranger_openness = random.choices(STRANGER_LIKE_OPTIONS, STRANGER_LIKE_PROBS)[0]
		self.table = None

		#this does not work for >2 len(STRANGER_LIKE_OPTIONS)
		if self.stranger_openness == STRANGER_LIKE_OPTIONS[0]:
			self.color = 'blue'
		elif self.stranger_openness == STRANGER_LIKE_OPTIONS[1]:
			self.color = 'red'

class Tables:
	def __init__(self, num_tables):
		if num_tables < 1:
			raise RuntimeError('Must have at least 1 table.')
		#these tables ARE ordered in terms of closeness to the entrance.
		self.tables = [[] for x in range(num_tables)]

	def get_best_table(self, person):
		table_scores = [0] * len(self.tables)
		for x in range(len(self.tables)):
			table_scores[x] = self.table_val(self.tables[x], person)

		if self.tables == [-math.inf] * len(self.tables):
			raise RuntimeError('Cafeteria is full. Make sure there are enough seats for everyone.')

		#closest (first match) table which has highest available score
		return self.tables[table_scores.index(max(table_scores))]

	def table_val(self, table, person):
		if len(table) >= TABLE_CAPACITY:
			return -math.inf

		val = 0
		if len(table) != 0:
			for peer in table:
				if person is peer:
					continue
				if g.get_connection_value(person.id, peer.id) != 0:
					val += g.get_connection_value(person.id, peer.id)
				else:
					val += person.stranger_openness

		else:
			val = ALONE_TENDENCY if (person.table == None) else SEATED_ALONE_TENDENCY 
		return val

	#give any seated people the opportunity to leave their table
	def reconsider(self, eating_order, x):
		for y in range(x + 1):
			person = eating_order[y]
			best_table = self.get_best_table(person)
			if self.table_val(best_table, person) > self.table_val(person.table, person) + LAZINESS:
				person.table.remove(person)
				person.table = best_table
				best_table.append(person)

	def add_connections(self, graph):
		for table in self.tables:
			for x in range(len(table)):
				for y in range(x + 1, len(table)):
					#not everyone forms connections and this helps ensure that people don't immediately fall into social groups
					if random.random() > (1 - CONNECTION_LIKELIHOOD):
						graph.set_connection_value(table[x].id, table[y].id, 1, relative=True)

	'''i don't see the purpose of this but I left the half-written code if I need it later
	def display(self):
		t = turtle.Turtle()
		turtle.tracer(0, 0)


		for table in self.tables:
			for person in table:
				t.up()
				t.setx(t.xcor() + 50)
				t.down()
				t.fillcolor(person.color)
				t.circle(10)
				t.end_fill()
				t.write(person.id, font=('Courier', 10))
			t.sety(t.ycor() + 50)
	'''

	def display(self):
		for table in self.tables:
			print(' '.join([str(person.id) for person in table]))


g = Graph(NUM_PEOPLE)
#g.set_connection_value(1, 2, 10)
g.display()

for turn in range(TURNS):
	#resetting everything
	cafeteria = Tables(5)
	g.clear_seating()
	eating_order = g.people_list.copy()
	random.shuffle(eating_order)

	for x in range(len(eating_order)):
		person = eating_order[x]
		
		best_table = cafeteria.get_best_table(person)
		best_table.append(person)
		person.table = best_table
		
		cafeteria.reconsider(eating_order, x) #people sitting will decide if to move (needs to meet a higher bar that could be set with a CONST)
	
	cafeteria.add_connections(g)
	cafeteria.display()

	g.display(turn == TURNS - 1)


	if turn > 1 and turn % CONNECTION_DECREASE_DAYS == 0:
		g.fade_connections()

turtle.done()