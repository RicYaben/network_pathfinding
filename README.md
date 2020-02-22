![alt text](https://github.com/RicYaben/network_pathfinding/blob/master/BFS.gif "BFS")

# USAGE

This application is written in `python 3` and makes use of the module `networkx` and `plotly` for the graphical interface of the application.

	pip install networkx plotly

## Basics

It is possible to run the application from the command line.
For this, on Linux or MacOs, you can just paste the following command on your terminal:

	python3 network_plot.py

Alternatively you could also use the `python3` interpreter, but it is not recomendable.

It is important for you to have all this documents stored in the same folder, as the application needs to fech some constants and functions spread across the documents. This documents are `graph.py`, `globals.py` and `network_plot`. Graph contains the logic behind the path finding algorithms and make it possible the creation of the graph. Globals contains a set of variables that are called across the graph to minimize the amount of time setting up the basis of the program. This variables can easily be overwritten, but mind them as they can raise errors if not changed carefully!

## GRAPHIC VIEW

Once you have run the command or started the python script on your preferred way, you will be presented with a simple command line menu in where you can choose the algorithm to use, the starting point and a goal if desired.
You can also preview the graph with the input `prev`, see the node links from the command line input `graph`, and of course, quit with one of the inputs `q`, `Q`, `Exit` or `exit` or by pressing `Ctrl+C` from your keyboard.




