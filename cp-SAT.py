
from ortools.sat.python import cp_model
import time

def solve_n_queens(n):
    model = cp_model.CpModel()

    queen = [
        model.new_int_var(0, n - 1, f"q_{i}")
        for i in range(n)
    ]

    model.add_all_different(queen)
    
    model.add_all_different(
        [queen[i] + i for i in range(n)]
    )
    model.add_all_different(
        [queen[i] - i for i in range(n)]
    )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60

    start = time.perf_counter()
    status = solver.solve(model)
    total_time = time.perf_counter() - start

    status_name = solver.status_name(status)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"N = {n}")
        print("Status:", status_name)
        print("Solution:", [solver.value(q) for q in queen])
    else:
        print(f"N = {n}, Status: {status_name}")

    print(f"Total time: {total_time:.6f} seconds")

for n in [4, 8, 16, 32, 64, 100, 128, 256, 512]:
    solve_n_queens(n)
    print("-" * 40)
