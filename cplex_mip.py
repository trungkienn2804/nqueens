
import cplex
import csv
import time

N_VALUES = [4, 8, 16, 32, 64, 100, 128, 256, 512]
TIME_LIMIT = 60


def solve_n_queens(n):
    start_total = time.perf_counter()
    model = cplex.Cplex()

    model.set_log_stream(None)
    model.set_error_stream(None)
    model.set_warning_stream(None)
    model.set_results_stream(None)

    names = [
        f"x_{r}_{col}"
        for r in range(n)
        for col in range(n)
    ]

    build_start = time.perf_counter()

    model.variables.add(
        names=names,
        types=[model.variables.type.binary] * (n * n)
    )

    model.objective.set_sense(model.objective.sense.minimize)

    rows = []
    senses = []
    rhs = []
    constraint_names = []

    for r in range(n):
        rows.append(cplex.SparsePair(
            ind=[r * n + col for col in range(n)],
            val=[1.0] * n
        ))
        senses.append("E")
        rhs.append(1.0)
        constraint_names.append(f"row_{r}")

    for col in range(n):
        rows.append(cplex.SparsePair(
            ind=[r * n + col for r in range(n)],
            val=[1.0] * n
        ))
        senses.append("E")
        rhs.append(1.0)
        constraint_names.append(f"col_{col}")

    for d in range(-(n - 1), n):
        cells = [
            r * n + col
            for r in range(n)
            for col in range(n)
            if r - col == d
        ]
        if len(cells) >= 2:
            rows.append(cplex.SparsePair(
                ind=cells, val=[1.0] * len(cells)
            ))
            senses.append("L")
            rhs.append(1.0)
            constraint_names.append(f"diag_down_{d}")

    for d in range(2 * n - 1):
        cells = [
            r * n + col
            for r in range(n)
            for col in range(n)
            if r + col == d
        ]
        if len(cells) >= 2:
            rows.append(cplex.SparsePair(
                ind=cells, val=[1.0] * len(cells)
            ))
            senses.append("L")
            rhs.append(1.0)
            constraint_names.append(f"diag_up_{d}")

    model.linear_constraints.add(
        lin_expr=rows,
        senses=senses,
        rhs=rhs,
        names=constraint_names
    )

    build_time = time.perf_counter() - build_start

    # Giới hạn thời gian giải
    model.parameters.timelimit.set(TIME_LIMIT)

    solver_start = time.perf_counter()
    status = ""
    found = 0
    solver_time = 0.0

    try:
        model.solve()
        solver_time = time.perf_counter() - solver_start

        status = model.solution.get_status_string()
        if model.solution.is_primal_feasible():
            found = 1

    except cplex.exceptions.CplexError as e:
        solver_time = time.perf_counter() - solver_start
        status = f"ERROR: {e}"

    total_time = time.perf_counter() - start_total

    result = {
        "N": n,
        "Variables": model.variables.get_num(),
        "Constraints": model.linear_constraints.get_num(),
        "Status": status,
        "SolutionsFound": found,
        "BuildTimeSeconds": round(build_time, 6),
        "SolverTimeSeconds": round(solver_time, 6),
        "TotalTimeSeconds": round(total_time, 6),
    }

    model.end()
    return result


results = []

for n in N_VALUES:
    print(f"N = {n} ...")
    result = solve_n_queens(n)
    results.append(result)

    print(
        f"N={n}, Status={result['Status']}, "
        f"Solver={result['SolverTimeSeconds']}s, "
        f"Total={result['TotalTimeSeconds']}s"
    )

with open("cplex_mip_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\nĐã lưu kết quả vào cplex_mip_results.csv")
