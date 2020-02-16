![alt text](https://github.com/RicYaben/network_pathfinding/BFS.gif "BFS")

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

Once you have run the command or started the python script on your preferred way, after few seconds, depending on the amount of vertices and connections there are in the network, the script will open the view on your browser on a local server, but it does not listen to any connection, therefore you won't be able to reopen it on a new tab or access the server from any other source. If you close it, and you want to see it working again, you will need to rerun the script.

Once it is open, click on the button on the bottom-right side with the algorithm chosen as name (BFS, DFS...) and it will start showing the path taken.




