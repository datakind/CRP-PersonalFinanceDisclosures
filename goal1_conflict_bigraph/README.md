The following Python packages are needed to run PAC_to_PFD.py script:

- pandas
- numpy (maybe?)
- networkx

The PAC_to_PDF.py script will output a GraphML file.

For graph visualizaiton, Gephi is used (see pac_pdf.gephi)

The file 2010_conflicts_of_interest.pdf contains a visualization of the 
bipartite graph.

Each edge corresponds to a conflict of interest relationship (see PAC_to_PDF.py
for definition of conflict of interest)

Each purple node corresponds to a CID (politician)
Each orange node corresponds to a PACID (a PAC)

The size of the node corresponds to the degree of the node.
