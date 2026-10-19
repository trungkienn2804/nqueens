import time

from pysat.solvers import Glucose3

start_time = time.time()
def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]


def at_most_one(clauses, variables):
    for i in range(0, len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])
    return clauses


def exactly_one(clauses, variables):
    clauses.append(variables)
    at_most_one(clauses, variables)


def generate_clauses(n, variables):
    clauses = []

    # Exactly one queen in each row
    for i in range(n):
        exactly_one(clauses, variables[i])

    # Exactly one queen in each column
    for j in range(n):
        exactly_one(clauses, [variables[i][j] for i in range(n)])


    # At most one queen in each diagonal
    for i in range(n):
        for j in range(n):
            for k in range(1, n):
                if i + k < n and j + k < n:
                    at_most_one(clauses, [variables[i][j], variables[i + k][j + k]])
                if i + k < n and j - k >= 0:
                    at_most_one(clauses, [variables[i][j], variables[i + k][j - k]])

    return clauses

def print_formula_stats(clauses, n):
    used_variables = {
        abs(literal)
        for clause in clauses
        for literal in clause
    }

    primary_count = n * n
    primary_variables = set(range(1, primary_count + 1))

    auxiliary_variables = {
        variable
        for variable in used_variables
        if variable > primary_count
    }

    max_variable_id = max(used_variables, default=0)

    print(f"N: {n}")
    print(f"Distinct variables appearing in clauses: {len(used_variables)}")
    print(f"Number of clauses: {len(clauses)}")


def solve_n_queens(n):
    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)
    print(clauses)

    print_formula_stats(clauses, n)
    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
    else:
        return None


def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        print(solution)
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


n = 4
solution = solve_n_queens(n)
print_solution(solution)
print("Run time:  %s seconds" % (time.time() - start_time))