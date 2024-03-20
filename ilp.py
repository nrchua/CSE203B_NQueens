import pulp
import csv
import sys
import time
from pathlib import Path

def setup_problem(n, initial_placements):
    # Create the problem
    prob = pulp.LpProblem("N-Queens_Problem", pulp.LpMaximize)
    
    # Define the variables
    x = pulp.LpVariable.dicts("x", ((i, j) for i in range(n) for j in range(n)), cat='Binary')
    
    # Objective: Maximize the number of queens (implicitly satisfied by constraints for a typical N-Queens problem)
    prob += pulp.lpSum(x[(i, j)] for i in range(n) for j in range(n))
    
    # Constraints for each row and column to have exactly one queen
    for i in range(n):
        prob += pulp.lpSum(x[(i, j)] for j in range(n)) == 1, f"Row_{i}_constraint"
        prob += pulp.lpSum(x[(j, i)] for j in range(n)) == 1, f"Column_{i}_constraint"
    
    # Diagonal constraints to have at most one queen
    # Forward diagonals
    for d in range(2-n, n):
        prob += pulp.lpSum(x[(i, i+d)] for i in range(max(0, -d), min(n, n-d))) <= 1, f"Forward_Diagonal_{d}_constraint"
    # Backward diagonals
    for d in range(2*n - 1):
        prob += pulp.lpSum(x[(i, d-i)] for i in range(max(0, d-n+1), min(d+1, n))) <= 1, f"Backward_Diagonal_{d}_constraint"
    
    # Initial Placements: Ensuring specific variables are set to 1 based on the initial placements
    for i, j in initial_placements:
        prob += x[(i, j)] == 1, f"Initial_Placement_{i}_{j}"

    return prob, x

def solve_problem(prob, x, n):
    # Solve the problem
    prob.solve(pulp.getSolver("PULP_CBC_CMD", timeLimit=30, msg=0))
    #print("SOLUTION TIME ", prob.solutionTime)
    # Check the solution status
    if pulp.LpStatus[prob.status] == 'Optimal':
        # Print the solution
        """
        for i in range(n):
            print(' '.join('Q' if x[(i, j)].varValue == 1 else '.' for j in range(n)))
        """
        print(f"Total Queens: {sum(x[(i, j)].varValue for i in range(n) for j in range(n))}")
    else:
        print("No solution found.")

def read_csv(filename):
    initial_placements = []
    with open(filename, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            initial_placements.append([int(item) for item in row])  # Process each row here
    return initial_placements
            
def main(folder_path):
    path = Path(folder_path)
    folder_name = path.name
    N = int(folder_name[:3])
    times = []
    count = 0
    for csv_file in path.glob("*.csv"):
        initial_placements = read_csv(csv_file)
        prob, x = setup_problem(N, initial_placements)
        start = time.time()
        solve_problem(prob, x, N)
        end = time.time()
        times.append(end - start)
    
    # Compute mean
    mean_time = (sum(times) / len(times) * 1000) # For miliseconds
    print(f"Average time for N={N} with {len(initial_placements)} queens initialized: {mean_time} miliseconds")
    
    #initial_placements = read_csv(filename)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide a folder as an argument")
    """
    n = 64  # Size of the chessboard
    initial_placements = []#[(0, 0)]  # Pre-placed queens (row, column), 0-indexed
    
    # Setup and solve the problem
    prob, x = setup_problem(n, initial_placements)
    solve_problem(prob, x, n)
    """
