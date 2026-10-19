
import runpy
import contextlib
import io
import matplotlib.pyplot as plt
import numpy as np

with contextlib.redirect_stdout(io.StringIO()):
    result = runpy.run_path("binary.py")

solution = result.get("solution")

if solution is None:
    print("Không tìm thấy nghiệm!")
else:
    board = np.array(solution)

    n = len(board)

    fig, ax = plt.subplots(figsize=(8, 8))
    colors = np.indices((n, n)).sum(axis=0) % 2
    ax.imshow(colors, cmap="Pastel2", origin="upper")

    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                ax.text(
                    j, i, "♛",
                    ha="center",
                    va="center",
                    fontsize=max(10, 300 // n),
                    color="black"
                )

    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="black", linewidth=1)
    ax.tick_params(which="both", bottom=False, left=False,
    labelbottom=False, labelleft=False)

    ax.set_title(f"N-Queens Solution (N = {n})")
    plt.tight_layout()
    plt.show()
