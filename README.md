*Protein Folding on a 2D Lattice*

Based on Lau and Dill, 1989

The files `setup.py` and `node.py` contains all of the machinery for reproducing results found in Lau and Dill's paper:
- Generating all self-avoiding walks of a given size
- Converting walks to graphs (lists of node objects)
- Calculating average values and protein metrics (i.e. number of topological contacts)

This paper is being expanded upon by using Monte Carlo sampling to create ensembles of proteins, this is contained in `mc.py`.

