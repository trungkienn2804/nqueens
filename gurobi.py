
import time
import csv
import gurobipy as gp
from gurobipy import GRB


def solve_n_queens(n, time_limit=60):
    start = time.perf_counter()

    model = gp.Model(f"NQueens_{n}")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit

    x = model.addVars(
        n, n,
        vtype=GRB.BINARY,
        name="x"
    )

    for i in range(n):
        model.addConstr(
            gp.quicksum(x[i, j] for j in range(n)) == 1
        )

    for j in range(n):
        model.addConstr(
            gp.quicksum(x[i, j] for i in range(n)) == 1
        )

    for d in range(-(n - 1), n):
        cells = [
            (i, j)
            for i in range(n)
            for j in range(n)
            if i - j == d
        ]

        if len(cells) >= 2:
            model.addConstr(
                gp.quicksum(x[i, j] for i, j in cells) <= 1
            )

    for d in range(2 * n - 1):
        cells = [
            (i, j)
            for i in range(n)
            for j in range(n)
            if i + j == d
        ]

        if len(cells) >= 2:
            model.addConstr(
                gp.quicksum(x[i, j] for i, j in cells) <= 1
            )

    model.optimize()

    total_time = time.perf_counter() - start
    solve_time = model.Runtime

    if model.Status == GRB.OPTIMAL:
        status = "OPTIMAL"
    elif model.Status == GRB.TIME_LIMIT:
        status = "TIME_LIMIT"
    elif model.Status == GRB.INFEASIBLE:
        status = "INFEASIBLE"
    else:
        status = f"STATUS_{model.Status}"

    print(f"\nN = {n}")
    print(f"Variables: {model.NumVars}")
    print(f"Constraints: {model.NumConstrs}")
    print(f"Status: {status}")
    print(f"Solutions found: {model.SolCount}")
    print(f"Model/solve total time: {total_time:.6f} seconds")
    print(f"Solver runtime: {solve_time:.6f} seconds")

    # In bàn cờ 
    if model.SolCount > 0:
        print("Board:")
        for i in range(n):
            row = [
                "Q" if x[i, j].X > 0.5 else "."
                for j in range(n)
            ]
            print(" ".join(row))

    result = {
        "N": n,
        "Variables": model.NumVars,
        "Constraints": model.NumConstrs,
        "Status": status,
        "SolutionsFound": model.SolCount,
        "TotalTimeSeconds": total_time,
        "SolverTimeSeconds": solve_time,
    }

    model.dispose()
    return result


if __name__ == "__main__":
    sizes = [4, 8, 16, 32, 64, 100, 128, 256, 512]
    results = []

    for n in sizes:
        try:
            results.append(solve_n_queens(n, time_limit=60))
        except gp.GurobiError as e:
            print(f"N={n}: Gurobi error: {e}")

    if results:
        with open(
            "gurobi_n_queens_results.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=results[0].keys()
            )
            writer.writeheader()
            writer.writerows(results)

        print("\nSaved to gurobi_n_queens_results.csv")
