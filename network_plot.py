import plotly.graph_objects as go
import networkx as nx
from graph import *
from globals import *
import random
import sys
import os

class Network_plot:

    def __init__( self, vertices, prob_link, algorithm = None, start = None, goal = None ):

        #set the current algorithm
        self.algorithm = algorithm

        #Initialize the graph and the network geometric graph
        self.geometric_graph = nx.random_geometric_graph(vertices, prob_link)
        self.graph = Graph(vertices)

        #populate the graph
        self._populate_graph()

        #set amount of vertices and goal if they are given
        self.vertices = vertices
        self.goal = goal
        self.start = start

    def get_distances(self):

        g = defaultdict(list)

        for v in self.graph.graph:
            for edge in self.graph.graph[v]:

                x0,y0 = self.geometric_graph.nodes[v]['pos']
                x1,y1 = self.geometric_graph.nodes[edge]['pos']

                distance = ( ( x0 - x1 )**2 + ( y0 - y1 )**2 )** 0.5

                g[v].append(( distance, edge))

        return g

    def get_nodes(self):
        return self.geometric_graph.nodes

    def _populate_graph(self):

        #Variables containing the polar coordinates of edges
        self.edge_x = []
        self.edge_y = []

        for edge in self.geometric_graph.edges():
            #get the polar coordinates
            x0, y0 = self.geometric_graph.nodes[edge[0]]['pos']
            x1, y1 = self.geometric_graph.nodes[edge[1]]['pos']

            #append x coordinate to the list
            self.edge_x.append(x0)
            self.edge_x.append(x1)
            self.edge_x.append(None)

            #append y coordinate to the list
            self.edge_y.append(y0)
            self.edge_y.append(y1)
            self.edge_y.append(None)

            #intent to add the edge to the graph
            self.graph.addEdge(edge[0], edge[1])

        #Variables containing the polar coordinates of nodes
        self.node_x = []
        self.node_y = []

        for node in self.geometric_graph.nodes():
            x, y = self.geometric_graph.nodes[node]['pos']
            self.node_x.append(x)
            self.node_y.append(y)

    def change_color(self, i, color=VISITED_COLOR):
        curr_ = self.fig.data[1]
        colors = list(curr_.marker.color)
        colors[i] = color
        curr_.marker.color = tuple(colors)
        return curr_

    def set_node_trace(self):

        #define the iddle colors and add the goal color
        colors = [IDLE_COLOR] * (self.vertices)

        if self.goal is not None:
            colors[self.goal] = GOAL_COLOR

        self.node_trace = go.Scatter(
                x=self.node_x, 
                y=self.node_y,
                hovertext=[i for i in range(self.vertices)],
                hoverinfo='text',
                mode='markers',
                marker=dict(color=colors)
            )

    def set_edge_trace( self ):
        self.edge_trace = go.Scatter(
                x=self.edge_x, y=self.edge_y,
                line=dict(width=0.5, color= LINE_COLOR),
                hoverinfo='none',
                mode='lines'
            )

    def reset_frames(self, algorithm, start, goal):
        path = self.get_path(algorithm, start, goal)
        print(f'Path: {path}') 
        self.fig.frames = [go.Frame(data=[self.edge_trace, self.change_color(i,VISITED_COLOR)]) for i in path]

    def get_button(self, algorithm, start ,goal):
        #return the buttons with an embeded function that is called on click.
        #Note: this is cheatting and I don't think this is inteded to be used
        #in this way whatsoever, and it might cause some problems on runtime!
        return [dict(label=algorithm, method="animate", args=[self.reset_frames(algorithm, start, goal)])]

    def show_figure(self):

        #set edges and nodes on idle state
        self.set_edge_trace()
        self.set_node_trace()

        # create figure
        self.fig = go.Figure()
        # add the Network trace. Edges and nodes
        self.fig.add_trace(self.edge_trace)
        self.fig.add_trace(self.node_trace)

        # update plot sizing
        self.fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=False,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

        # add dropdown
        self.fig.update_layout(
            updatemenus = [dict(
                    type="buttons",
                    buttons= self.get_button( self.algorithm,self.start, self.goal) if self.algorithm is not None else [],
                    direction= "down",
                    showactive= True,
                    x= 0.1,
                    xanchor= "left",
                    y= 0.1,
                    yanchor= "top"
                )
            ] 
        )

        # change the background color so our eyes dont bleed
        self.fig.layout.plot_bgcolor = BACKGROUND_COLOR

        self.fig.show()

    # gets the path used by the algorithm to find the path
    def get_path( self, algorithm, start=None,goal=None ):

        #starting point for the algorithm to work.
        if start is None:
            start = random.randint(1, self.vertices)
        
        #pythonian switch
        if algorithm == 'BFS':
            return self.graph.BFS(start, goal)
        elif algorithm == 'DFS':
            return self.graph.DFS(start)
        elif algorithm == 'dijkstra':
            graph = self.get_distances()
            path = self.graph.dijkstra( graph, start, goal)
            path.reverse()
            return path
        elif algorithm == 'A*':
            graph = self.get_distances()
            nodes = self.get_nodes()
            path = self.graph.a_star(graph, start, goal, nodes)
            return path


    def show_menu(self):
        algs = self.graph.get_algs()

        # Client hello
        print(f'Select the algorithm to run with the chosen parameters:\nExpected Input: algorithm start goal\nExample: 2 5 70\n')
        inp = ''

        while inp is not 'Exit':
            print(*[ f'{i}) {algs[i]}' for i in range(len(algs))], sep='\n')
            print('graph) Logs the current graph\nprev) Preview the graph\nq) Quit\n')

            #declare and modify the input
            inp = input()
        
            if inp == 'Exit' or inp == 'exit' or inp == 'q' or inp=='Q':
                print('bye!')
                return
            elif inp == 'graph':
                print(*self.graph.get_graph(), sep='\n')
            elif inp == 'prev':
                self.show_figure()
            else:

                try:
                    # initialize the parameters
                    inp = list(map(int, inp.split()))
                    self.algorithm = algs[inp[0]]
                    self.start = inp[1] 
                    self.goal = inp[2] if len(inp) >= 3 else None

                    print(f'\033[92mLoading...\033[0m')
                    # show the graph and exit
                    self.show_figure()

                except Exception as e:
                    print('----------')
                    print('\033[93m[ERROR] Wrong input')
                    print(f'>>> {e}\033[0m')
                    print('----------')

def main():

#################################
#   Automatic based on pre-defined globals: 
#
#   N = Network_plot( VERTICES, PROBABILITY_OF_EDGE , ALGORITHM, START , GOAL )
#   N.show_figure()
#
#   With menu:
#
    N = Network_plot( VERTICES, PROBABILITY_OF_EDGE)
    N.show_menu()
#
#################################        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
