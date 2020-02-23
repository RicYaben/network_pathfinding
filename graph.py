from collections import defaultdict
from heapq import heappush, heappop
from itertools import count

class Graph:
	def __init__(self , vertices):

		#We use a defaultdict so we don't have to handle exceptions 
		#when we try to sdd a new edge to an edge, in the case that
		#for example, the vertice we are trying to add the edge does
		#not exists on our dictionary
		# more info: 
		# https://docs.python.org/3/library/collections.html#collections.defaultdict
		self.graph = defaultdict(list)
		self.vertices = vertices

	def addEdge(self, vertice, edge):
		#add a new edge to a vertice, whether it exists or it does not.
		if edge not in self.graph[vertice] and vertice not in self.graph[edge]:
			self.graph[vertice].append(edge)
			#make it bi-directional
			self.graph[edge].append(vertice)

	def get_length(self):
		return len(self.graph)

	def get_graph(self):
		return sorted([ [i,self.graph[i]] for i in self.graph if self.graph[i] != self.graph.default_factory()])

	def get_algs(self):
		return ['BFS', 'DFS', 'dijkstra', 'A*']

	def BFS(self, start, goal):
		#make a list of length equal to the amount 
		#vertices inside our graph with a falsy value for each entry.
		#this list represents the whole amount of vertices that haven't
		#been discovered yet. Then, at the starting vertice index, we put
		#a truly value since we have discovered the start.
		discovered = [False] * (self.vertices)
		discovered[start] = True

		#make an empty queue and append the starting vertice.
		queue = []
		queue.append(start)

		#define a set containing how the list of vertices
		#was discovered.
		path = []

		if goal is None:
			while queue:
				#Set the current starting vertice to the returned
				#list from removing the first entry from the queue
				start = queue.pop(0)
				#Add the current vertice to a set, so we ca print it later
				path.append(start)

				#get the list of edges
				#inside the current vertice
				#for each, if they have not been visited
				#yet, we add them to the queue
				#and change their visibility in the 
				#discovered list to True.
				for i in self.graph[start]:
					if discovered[i] == False:
						discovered[i] = True
						queue.append(i)
				
			#return path
			return path

		else:
			print(f'Goal: {goal}')
			while queue:
				start = queue.pop(0)
				path.append(start)
				if start == goal:
					return path
				for i in self.graph[start]:
					if discovered[i] == False:
						discovered[i] = True
						queue.append(i)
			return path

	def DFSUtil(self,v,visited, path):
		
		#set the current node as visited
		visited[v] = True
		path.append(v)
		for i in self.graph[v]:
			if visited[i] == False:
				self.DFSUtil(i, visited, path)

	def DFS(self,v):
		path = []
		visited = [False] * (self.vertices)
		self.DFSUtil(v, visited, path)
		return path

	def dijkstra( self,g, start, destination ):

		q, seen, mins = [(0,start,[])], set(), { start:0}
		while q:
			( cost, v1, path) = heappop(q)

			if v1 not in seen:
				seen.add(v1)
				path = [v1] + path

				if v1 == destination:
					return(path)

				for c, v2 in g.get(v1, ()):
					if v2 in seen:
						continue
					prev = mins.get(v2, None)
					next = cost + c
					if prev is None or next < prev:
						mins[v2] = next
						heappush(q, (next, v2, path))

		return ([])


	def a_star(self, g, start, destination, nodes):
		''' Return a list of nodes ordered in a shortest path from source
		destination using A* slgorithm or nothing if the path does not
		exists.
		'''

		def heuristic(v, e):

			x0, y0 = nodes[v]['pos']
			x1, y1 = nodes[e]['pos']

			return ( ( x0 - x1 )**2 + ( y0 - y1 )**2 )** 0.5

		# A queue `q`that stores the priority, current node, distance to the
		# destination and parent.
		# Using a heapq to preserve the priority.
		# The counter is used to prevent circular dependencies.
		
		c = count()
		q = [ (0, next(c), start, 0, None) ]

		# enq distance from the discovered nodes to the destination

		enq = {}
		exp = {}

		while q:
			_,__,curr_node, dist, parent = heappop(q)

			# Check if we are at the destination
			if curr_node == destination:
				path = [curr_node]
				node = parent

				while node is not None:
					path.append(node)
					node = exp[node]
				path.reverse()
				return path

			# Check if we have already visited the current node
			if curr_node in exp:

				# If we have, but the current node is empty continue
				# with the next
				if exp[curr_node] is None:
					continue

				# enq the cost and the heuristic distance
				qcost, h = enq[curr_node]
				if qcost < dist:
					continue

			# Accept the current path and add the current node
			# as the next parent
			exp[curr_node] = parent

			# iterate through the items
			for distance, edge in g[curr_node]:
				# declare the cost of the current node
				ncost = dist + distance
				
				if edge in enq:
					qcost, h = enq[edge]

					# check if the qcost is lower
					# than the ncost, and if so, the
					# edge won't be queued
					if qcost <= ncost:
						continue

				else:
					h = heuristic(edge, destination)

				enq[edge] = ncost, h
				heappush(q, (ncost + h, next(c), edge, ncost, curr_node) )

		return []
