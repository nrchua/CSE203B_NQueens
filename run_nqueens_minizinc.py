import subprocess
import time

def solve_n_queens(n):
	start = time.time()
	result = subprocess.run(
		['minizinc','--solver','Gecode','n_queens.mzn','placements.dzn'],stdout=subprocess.PIPE, text=True
	)
	end = time.time()
	return result.stdout, end-start

output, time_elapsed = solve_n_queens(8)
print(output, time_elapsed)