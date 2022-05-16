# coding: utf-8

from ase.db import connect

if __name__ == '__main__':

    
    database_path = "train.db"  # path to file
    database = connect(database_path)  # loading database
    row = database.get(1)  # take first element in the database
    n_atoms = row.natoms  # number of atoms in a molecule
    numbers = row.numbers  # atomic numbers of a molecule
    symbols = row.symbols  # atom names in a molecule
    positions = row.positions  # atom coordinates. np.array with shape n_atoms x 3
    energy = row.data.get('energy') # energy. np.array shape 1, contaning energy