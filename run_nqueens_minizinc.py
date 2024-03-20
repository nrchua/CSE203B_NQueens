import subprocess
import time
import sys
import ast
import numpy as np
from pathlib import Path

def printSolution(board):
	for i in range(board.shape[0]):
		for j in range(board.shape[0]):
			if board[i][j] == 1:
				print("Q",end=" ")
			else:
				print(".",end=" ")
		print()

def solve_n_queens(dzn_file):
	start = time.time()
	result = subprocess.run(
		['minizinc','--solver','Gecode','n_queens.mzn', dzn_file],stdout=subprocess.PIPE, text=True
	)
	end = time.time()

	out = result.stdout.split("\n")
	sol_str = out[0]
	if sol_str == "=====UNSATISFIABLE=====":
		# Unsolvable
		print("=====UNSATISFIABLE=====\n")
	else:
		# Solvable. Share board
		sol = ast.literal_eval(out[0])

		# Create board
		board = np.zeros((len(sol), len(sol)))

		# Insert queens at the solved positions
		for col, r in enumerate(sol):
			board[r-1][col] = 1

		# Print the board
		printSolution(board)
		print()

	return end-start

def main(queens_path):
	path = Path(queens_path)
	folder_name = path.name
	N = int(folder_name[:3])
	times = []
	count = 0
	for dzn_file in path.glob("*.dzn"):
		iter_time = solve_n_queens(dzn_file)
		times.append(iter_time)
	avg = (sum(times) / len(times)) * 1000
	print(f"==============\nAverage time: {avg}\n==============")


if __name__ == "__main__":
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		print("Please provide a folder as an argument")