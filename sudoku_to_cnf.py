'''
Written by Lukasz Komza for Artificial Intellgence 1 at the Bergen County Academies

sudoku_to_cnf.py generates a CNF expression for a sudoku puzzle.

'''
sudoku_board = []
clauses = []
num_clauses=0

def print_board(sudoku_board):
	print("----------------------------")
	for i in range(len(sudoku_board)):
		print(sudoku_board[i])
	print("----------------------------\n")

for i in range(9):
	sudoku_board.append(input().split())
	for j in range(9):
		sudoku_board[i][j]=(int)(sudoku_board[i][j])

# Checking values
for i in range(9):
	for j in range(9):
		temp=""
		if(not sudoku_board[i][j]):
			for n in range(1,10):
				temp+=(str(i+1)+str(j+1)+str(n)+" ")
		else:
			temp+=(str(i+1)+str(j+1)+str(sudoku_board[i][j])+" ")
		clauses.append(temp+"0")

# Checking rows
for x in range(1,10):
	for y in range(1,10):
		for i in range(1,10):
			if(i!=y):
				for n in range(1,10):
					clauses.append('-'+str(x)+str(y)+str(n)+" -"+str(x)+str(i)+str(n)+" 0")

# Checking columns
for x in range(1,10):
	for y in range(1,10):
		for i in range(1,10):
			if(i!=x):
				for n in range(1,10):
					clauses.append('-'+str(x)+str(y)+str(n)+" -"+str(i)+str(y)+str(n)+" 0")

#Checking single value
for x in range(1,10):
	for y in range(1,10):
		for i in range(1,10):
			for j in range(1,10):
				if(i!=j):
					clauses.append('-'+str(x)+str(y)+str(i)+" -"+str(x)+str(y)+str(j)+" 0")

# Checking squares
for a in range(0,3):
	for b in range(0,3):
		for x in range(1,4):
			for y in range(1,4):
				for i in range(1,4):
					for j in range(1,4):
						for n in range(1,10):
							if(not(i==x and j==y)):
								clauses.append('-'+str(i+3*a)+str(j+3*b)+str(n)+" -"+str(x+3*a)+str(y+3*b)+str(n)+" 0")

print("p cnf "+str(999)+" "+str(len(clauses)))
for clause in clauses:
	print(clause)