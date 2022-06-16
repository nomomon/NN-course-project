from .convert import *
from .distance import *

class Constraint():
    # The variables that the constraint is between
    def __init__(self, variables):
        self.variables = variables

    # Must be overridden by subclasses
    def satisfied(self, assignment):
        ...

class CSP():
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = domains
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError(f"Variable '{variable}' in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment = {}, find_all = False):
        # assignment is complete if every variable is assigned (our base case)
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned = [v for v in self.variables if v not in assignment]
        if find_all: all_solutions = []
        # get the every possible domain value of the first unassigned variable
        first = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    if find_all: all_solutions.append(result)
                    else: return result
        if find_all and len(all_solutions): return all_solutions
        else: return None

class AtomBondsConstraint(Constraint):
    def __init__(self, bond_ids, total_bonds, ):
        super().__init__(bond_ids)
        self.bond_ids = bond_ids
        self.total_bonds = total_bonds

    def satisfied(self, assignment):
        if any([(bond_id not in assignment) for bond_id in self.bond_ids]):
            return True

        sum_of_bonds = sum([assignment[bond_id] for bond_id in self.bond_ids])

        if type(self.total_bonds) is list:
            return sum_of_bonds in self.total_bonds
        else:
            return sum_of_bonds == self.total_bonds

def csp_solve_bond_matrix(row, find_all=False):
    symbols = row.symbols
    n_atoms = row.natoms
    bond_matrix = get_bond_type_matrix(get_distance_matrix(row), row.symbols) > 0

    variables = []
    for i in range(n_atoms-1):
        for j in range(i+1, n_atoms):
            if bond_matrix[i][j]:
                variables.append(" ".join(sorted([str(i), str(j)])))

    domains = {}
    for variable in variables:
        i, j = variable.split(" ")
        i = int(i)
        j = int(j)

        bond_name = get_bond_name(symbols[i], symbols[j])
        domains[variable] = list(range(len(type_bond_length[bond_name])+1))
        if bond_name == 'CC':
            domains[variable] = [0, 1, 1.5, 2]


    csp = CSP(variables, domains)

    obj = {
        'Br':1, 
        'C':4, 
        'Cl':1, 
        'F':1, 
        'H':1, 
        'N':3, 
        'O':2, 
        'S':[2, 4, 6]
    }

    for i in range(n_atoms):
        bonds = [" ".join(sorted([str(i), str(j)])) for j in np.where(bond_matrix[i])[0]]
        csp.add_constraint(AtomBondsConstraint(bonds, obj[symbols[i]]))

    solution = csp.backtracking_search(find_all=find_all)

    return solution

def get_csp_bond_type_matrix(row):
    n_atoms = row.natoms
    solution = csp_solve_bond_matrix(row)

    if solution is None:
        return None
    else:
        csp_bond_type_matrix = np.zeros((n_atoms, n_atoms))
        
        for variable in solution:
            i, j = variable.split(" ")
            i = int(i)
            j = int(j)

            csp_bond_type_matrix[i][j] = solution[variable]
            csp_bond_type_matrix[j][i] = solution[variable]
        return csp_bond_type_matrix

def get_csp_bond_type_count(row):
    n_atoms = row.natoms
    symbols = row.symbols
    solution = csp_solve_bond_matrix(row)

    if solution is None:
        return None
    else:
        bond_counter = {}
    
        for i in range(n_atoms - 1):
            for j in range(i, n_atoms):
                if " ".join(sorted([str(i), str(j)])) in solution:
                    bond_name = get_bond_name(symbols[i], symbols[j])
                    bond_type = solution[" ".join(sorted([str(i), str(j)]))]
                    bond_name += str(bond_type)
                    
                    if bond_name in bond_counter:
                        bond_counter[bond_name] += 1
                    else:
                        bond_counter[bond_name] = 1

        return bond_counter