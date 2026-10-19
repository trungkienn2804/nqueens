
import subprocess
import time
import csv
import sys
from pathlib import Path

folder = Path(__file__).resolve().parent

solvers = [
    "binary.py",
    "binomial.py",
    "commander.py",
    "product.py",
    "sequential.py",
]

results = []

for filename in solvers:
    filepath = folder / filename

    if not filepath.exists():
        print(f"Không tìm thấy: {filename}")
        continue

    print(f"\nĐang chạy {filename}...")

    start = time.perf_counter()

    try:
        process = subprocess.run(
            [sys.executable, str(filepath)],
            cwd=str(folder),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120
        )

        elapsed = time.perf_counter() - start

        if process.returncode == 0:
            status = "Completed"
            print(f"Thời gian: {elapsed:.4f} giây")
        else:
            status = "Error"
            print(f"Chương trình lỗi sau {elapsed:.4f} giây")
            print(process.stderr[-1000:])

        results.append([filename, status, round(elapsed, 4)])

    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - start
        print(f"Vượt quá 120 giây: {filename}")
        results.append([filename, "Timeout", round(elapsed, 4)])

# Lưu kết quả
csv_path = folder / "benchmark_results.csv"

with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["SAT Solver", "Status", "Runtime (seconds)"])
    writer.writerows(results)

print("\n===== KẾT QUẢ BENCHMARK =====")
for filename, status, elapsed in results:
    print(f"{filename:20} | {status:10} | {elapsed:.4f} giây")

print(f"\nĐã lưu kết quả tại: {csv_path}")
