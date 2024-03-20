# CSE203B_NQueens

## Make Data
Run: `python make_data.py`
The data will be stored in folders `./board_initialiations/xxx_yyy`. `xxx` is the size of the board (with leading 0s if not 3 digits long) and `yyy` is the number of queens initialized (with leading 0s if not 3 digits long). Inside each folder, each `.csv` file consists of one random initialization.

## ILP
### Dependencies
- PuLP: `pip install pulp`

### Run the ILP
Run: `python ilp.py <./board_initializations/xxx_yyy>`
This will run the ILP solver over each initialization in the `xxx_yyy` folder and print out the mean runtime.

## Constraint Programming (Gecode)
### Dependencies
- MiniZinc

### Run the MiniZinc Gecode solver
Run: `python run_nqueens_minizinc.py ./board_initializations/xxx_yyy/`
