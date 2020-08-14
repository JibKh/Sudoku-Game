"""board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]"""

#Solves board
def solve(board):
	#Base Case
	position = find_empty(board)
	if not position:
		return True
	
	#Lets start
	row, col = position

	#Going to loop through every number and check if it is valid.
	#If valid, add to board, call recursively again
	#If invalid, go to next value
	#If looped through all values, backtrack
	for i in range(1, 10):
		if valid(board, i, (row, col)) == True:
			board[row][col] = i

			if solve(board):
				return True
			
			board[row][col] = 0

	return False

#Prints board
def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -  ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")

#Finds empty position and returns the row and column index
def find_empty(bo):
	for i in range(len(bo)):
		for j in range(len(bo[i])):
			if(bo[i][j] == 0):
				return (i, j) #row, col
	return None

#Checks if the number that has been input is valid or not. Row, column, grid check
def valid(board, num, pos):
	#Check row
	for i in range(len(board[0])):
		if board[pos[0]][i] == num and i != pos[1]:
			return False
	
	#Check column
	for i in range(len(board[0])):
		if board[i][pos[1]] == num and i != pos[0]:
			return False
	
	#Check grid
	row_start = pos[0] - (pos[0] % 3)
	col_start = pos[1] - (pos[1] % 3)

	for i in range(row_start, row_start + 3, 1):
		for j in range(col_start, col_start + 3, 1):
			if board[i][j] == num and (i,j) != pos:
				return False

	return True

"""print('~~~~UNSOLVED BOARD~~~~')
print_board(board)
solve(board)
print("\n  ~~~~SOLVED BOARD~~~~")
print_board(board)"""