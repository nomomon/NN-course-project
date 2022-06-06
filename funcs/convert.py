import numpy as np

shortest_bond_length = 80
longest_bond_length = 187

type_bond_length =  {'BrC': [191], 'BrN': [188], 'BrO': [180], 'BrS': [218], 'CC': [134, 154, 140], 'CCl': [176], 'CF': [141], 'CH': [114], 'CN': [132, 151], 'CO': [124, 143], 'CS': [162, 181], 'ClN': [173], 'ClO': [165], 'ClS': [203], 'FN': [138], 'FO': [130], 'FS': [168], 'HN': [111], 'HO': [103], 'HS': [141], 'NN': [130, 148], 'NO': [122, 140], 'NS': [160, 178], 'OO': [132], 'OS': [170], 'SS': [208]}

def get_bond_type(bond_name, bond_length):
    bond_type = np.argmin([abs(l - bond_length) for l in type_bond_length[bond_name]]) + 1
    
    # aromatic carbon - carbon bond
    if 'CC' == bond_name and bond_type == 3:
        return 1.5
    else:
        return bond_type


def convert_to_picometers(distance_matrix):
    """
    convert from dataset units to picometers
    """
    return distance_matrix * 28.4

def get_bond_type_matrix(distance_matrix, symbols):
    n_atoms = len(symbols)

    distance_matrix = convert_to_picometers(distance_matrix)
    bond_matrix = np.zeros_like(distance_matrix)
    
    for i in range(n_atoms - 1):
        for j in range(i, n_atoms):
            bond_name = "".join(sorted(symbols[i] + symbols[j]))
            bond_length = distance_matrix[i][j]
            
            if(bond_length < shortest_bond_length or 
                bond_length > longest_bond_length or
                bond_name not in type_bond_length):
                bond_type = 0
            else:
                bond_type = get_bond_type(bond_name, bond_length)

            bond_matrix[i][j] = bond_type
            bond_matrix[j][i] = bond_type

    return bond_matrix

def get_bond_counts(distance_matrix, symbols):
    n_atoms = len(symbols)
    
    distance_matrix = convert_to_picometers(distance_matrix)
    bond_counter = {}
    
    for i in range(n_atoms - 1):
        for j in range(i, n_atoms):
            bond_name = "".join(sorted(symbols[i] + symbols[j]))
            bond_length = distance_matrix[i][j]
            
            if(bond_length < shortest_bond_length or 
                bond_length > longest_bond_length or
                bond_name not in type_bond_length):
                continue
            else:
                bond_type = get_bond_type(bond_name, bond_length)
                bond_name += str(bond_type)
                
                if bond_name in bond_counter:
                    bond_counter[bond_name] += 1
                else:
                    bond_counter[bond_name] = 1

    return bond_counter