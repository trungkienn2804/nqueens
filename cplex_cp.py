
from docplex.cp.model import CpoModel

N = 4

mdl = CpoModel(name="NQueens_Test")

q = [mdl.integer_var(0, N - 1, name=f"q_{i}") for i in range(N)]

from docplex.cp.model import all_diff

mdl.add(all_diff(q))

mdl.add(all_diff([q[i] + i for i in range(N)]))
mdl.add(all_diff([q[i] - i for i in range(N)]))

solver_path = r"D:\cpoptimizer\bin\x64_win64\cpoptimizer.exe"

try:
    solution = mdl.solve(
        execfile=solver_path,
        TimeLimit=10
    )

    if solution:
        print("CPLEX-CP chạy thành công!")
        print("N =", N)
        print("Vị trí hàng của các quân hậu:",
            [solution.get_value(q[i]) for i in range(N)])
    else:
        print("Solver không trả về nghiệm.")

except Exception as e:
    print("Lỗi khi chạy CP Optimizer:")
    print(type(e).__name__, e)
