import csv
import random
import os
import numpy as np

def check_row(board, row):
    N = board.shape[0]
    # Checks if the row already has a queen
    for i in range(N):
        if board[row,i] == 1:
            #print(f"row {row}")
            return True
    return False

def check_col(board, col):
    N = board.shape[0]
    # Checks if the column already has a queen
    for i in range(N):
        if board[i,col] == 1:
            #print(f"col {col}")
            return True
    return False

def check_diags(board, row, col):
    N = board.shape[0]
    # Checks if the diagonal already has a queen
    # Check upper main diagonal
    i,j = row, col
    while i >= 0 and j >= 0:
        if board[i,j] == 1:
            return True # Found queen along this diagonal
        i -= 1
        j -= 1
    # Check lower main diagonal
    i,j = row+1, col+1
    while i < N and j < N:
        if board[i,j] == 1:
            return True # Found queen along this diagonal
        i += 1
        j += 1

    # Check upper anti-diagonal
    i,j = row, col
    while i >= 0 and j < N:
        if board[i,j] == 1:
            return True # Found queen along this diagonal
        i -= 1
        j += 1
    # Check lower anti-diagonal
    i,j = row+1, col-1
    while i < N and j >= 0:
        if board[i,j] == 1:
            return True # Found queen along this diagonal
        i += 1
        j -= 1
    return False

def verify_placement(board, row, col, N):
    # Returns if placement is invalid or not
    if check_row(board, row):
        return False
    elif check_col(board, col):
        return False
    elif check_diags(board, row, col):
        return False
    else:
        return True
        

def make_configuration(N, num_queens):
    # Randomly select number of queens to place placed on probability
    """
    if prob=="low": # [1,N//4] queens
        num_queens = random.randint(1, N//4)
    elif prob=="mid":
        num_queens = random.randint(N//4, N//2)
    else:
        num_queens = random.randint(N//2, N-1)
    """ 
    # Initialize an empty board
    board = np.zeros((N,N))
    coords = []
    if num_queens == 0:
        print(num_queens, len(coords))
        return board, coords
    # Shuffle columns
    cols = list(range(0,N))
    random.shuffle(cols)
    count = 0
    for col in cols:
        # Randomly shuffle row ordering
        rows = list(range(0, N))
        random.shuffle(rows)
        
        # Try to place the queen in this coordinate
        for row in rows:
            # Checks if placement is valid
            if verify_placement(board, row, col, N):
                board[row, col] = 1
                coords.append((row, col))
                count += 1
                break
            # If placed num_queens queens, then break
            if count == num_queens:
                break
        
        if count == num_queens:
            break
    print(num_queens, len(coords))
    return board, coords

def create_data(N, num_data=8):
    # Create num_queens steps
    num_queens = np.linspace(0, N, 4, endpoint=False)
    num_queens = num_queens#[1:]
    
    # Create folders if it doesnt exist
    for nq in num_queens:
        folder_path = f"./{N:03}_{int(nq):02}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
    
    count = 0
    for nq in num_queens:
        for i in range(num_data):
            # Create filename
            file_name = f"./{N:03}_{int(nq):02}/{i:03d}.csv"
            # Make a configuration
            _, coords = make_configuration(N, nq)
            # Open the file
            with open(file_name, mode="w", newline="") as file:
                writer = csv.writer(file)
                #writer.writerow([len(coords)])
                # Now, add the coordinates
                for j in range(len(coords)):
                    writer.writerow(coords[j])
            count += 1    

def main():
    # Initialize parameters
    N = [8, 16, 24, 32]
    num_data = 64
    print("Making data!")
    for n in N:
        create_data(n, num_data)
    
if __name__ == "__main__":
    main()