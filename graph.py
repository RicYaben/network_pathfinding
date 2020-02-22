from collections import defaultdict
from heapq import *

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
		return ['BFS', 'DFS', 'dijkstra']

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
