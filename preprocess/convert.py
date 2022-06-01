import numpy as np

def get_bond_type_matrix(distance_matrix, symbols):
    possible_lengths = {'BrBr': [228], 'BrC': [191], 'BrCl': [213], 'BrF': [178], 'BrH': [151], 'BrN': [188], 'BrO': [180], 'BrS': [218], 'CC': [120, 134, 154], 'CCl': [176], 'CF': [141], 'CH': [114], 'CN': [114, 132, 151], 'CO': [124, 143], 'CS': [162, 181], 'ClCl': [198], 'ClF': [163], 'ClH': [136], 'ClN': [173], 'ClO': [165], 'ClS': [203], 'FF': [128], 'FH': [101], 'FN': [138], 'FO': [130], 'FS': [168], 'HH': [74], 'HN': [111], 'HO': [103], 'HS': [141], 'NN': [108, 130, 148], 'NO': [122, 140], 'NS': [160, 178], 'OO': [114, 132], 'OS': [152, 170], 'SS': [190, 208]}
    n_atoms = len(symbols)

    bond_matrix = np.zeros_like(distance_matrix)
    
    for i in range(n_atoms - 1):
        for j in range(i, n_atoms):
            bond_name = "".join(sorted(symbols[i] + symbols[j]))
            bond_length = distance_matrix[i][j]
            
            if(abs(possible_lengths[bond_name][0] - bond_length) > 60 and
               abs(possible_lengths[bond_name][-1] - bond_length) > 60):
                bond_type = 0
            else:
                bond_type = np.argmin([abs(l - bond_length) for l in possible_lengths[bond_name]]) + 1

            bond_matrix[i][j] = bond_type
            bond_matrix[j][i] = bond_type

    return bond_matrix

def get_bond_counts(distance_matrix, symbols):
    possible_lengths = {'BrBr': [228], 'BrC': [191], 'BrCl': [213], 'BrF': [178], 'BrH': [151], 'BrN': [188], 'BrO': [180], 'BrS': [218], 'CC': [120, 134, 154], 'CCl': [176], 'CF': [141], 'CH': [114], 'CN': [114, 132, 151], 'CO': [124, 143], 'CS': [162, 181], 'ClCl': [198], 'ClF': [163], 'ClH': [136], 'ClN': [173], 'ClO': [165], 'ClS': [203], 'FF': [128], 'FH': [101], 'FN': [138], 'FO': [130], 'FS': [168], 'HH': [74], 'HN': [111], 'HO': [103], 'HS': [141], 'NN': [108, 130, 148], 'NO': [122, 140], 'NS': [160, 178], 'OO': [114, 132], 'OS': [152, 170], 'SS': [190, 208]}
    n_atoms = len(symbols)
    
    distance_matrix *= 28.4

    bond_counter = {}
    
    for i in range(n_atoms - 1):
        for j in range(i, n_atoms):
            bond_name = "".join(sorted(symbols[i] + symbols[j]))
            bond_length = distance_matrix[i][j]
            
            if(abs(possible_lengths[bond_name][0] - bond_length) > 60 and 
               abs(possible_lengths[bond_name][-1] - bond_length) > 60):
                continue
            else:
                bond_type = np.argmin([abs(l - bond_length) for l in possible_lengths[bond_name]]) + 1
                bond_name += str(bond_type)
                
                if bond_name in bond_counter:
                    bond_counter[bond_name] += 1
                else:
                    bond_counter[bond_name] = 1

    return bond_counter