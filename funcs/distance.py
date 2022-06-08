import numpy as np
from ase.db import connect

train_db = connect("./data/train.db")

def get_dist(pos1, pos2):
    dist = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)
    return dist

def get_distance_matrix(row):
    n = row.natoms
    res_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            res_matrix[i,j] = get_dist(row.positions[i], row.positions[j])
    return res_matrix

def get_all_distances(data):
    res = []
    atoms_matrix = []
    for row in data:
        atoms = row.symbols
        dist = get_distance_matrix(row)
        res.append(dist)
        atoms_matrix.append(atoms)
    return res, atoms_matrix