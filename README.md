# unchurnable
This is a program used for some results obtained in the paper "Incompressibility of H-free edge modification problems: Towards a dichotomy" by Dániel Marx and R. B. Sandeep.

Usage: python2 unchurnable.py input.g6 output.txt

The expected input file is a list of graphs in graph6 (g6) format. Please see the following link for the details of the format: https://users.cecs.anu.edu.au/~bdm/data/formats.html
The program goes through each graph H in the input list and outputs H if H \not in X U Y and H-V_\ell and H-V_h are in Y. Please see the paper for more details.

We used the input g6 files accessible from https://users.cecs.anu.edu.au/~bdm/data/graphs.html containing graphs with 5 to 11 vertices.
The output files can be found in results folder.
The output files are slightly edited to add the name of the graphs used in the paper.
The description of each file in the output file is of the form "Graph i - label", where i is the serial number and label is the name used for the graph in the paper. The next line contains two numbers - the number n of vertices and the number m of edges in the graph. The next m lines describe the edges in the graph.
