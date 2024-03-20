include "globals.mzn";

% Parameters
int: N; % Size of the chessboard
int: K; % Number of initially placed queens
array[1..K] of 1..N: initial_rows;
array[1..K] of 1..N: initial_cols;

% Decision variable: the row position of each queen
array[1..N] of var 1..N: queen_row;

% Constraints to ensure initially placed queens are respected
constraint forall(k in 1..K)(
  queen_row[initial_cols[k]] = initial_rows[k]
);

% Constraints to ensure no two queens attack each other
constraint forall(i, j in 1..N where i < j)(
  queen_row[i] != queen_row[j] /\
  queen_row[i] + i != queen_row[j] + j /\
  queen_row[i] - i != queen_row[j] - j
);

solve satisfy;

% Output solution
output ["\(queen_row)"];
