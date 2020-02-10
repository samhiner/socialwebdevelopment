import networkx as nx
import matplotlib.pyplot as plt

class Graph(nx.Graph):
	def populate_graph(self, nodes):
		self.add_nodes_from(range(nodes))
		for x in range(nodes):
			self.add_weighted_edges_from([x, y, 0.5] for y in range(x+1, nodes))

graph = Graph()
graph.populate_graph(50)
print(graph.edges())


#####
nx.draw(graph)
weights = nx.get_edge_attributes(graph, 'weight')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights)
plt.show()