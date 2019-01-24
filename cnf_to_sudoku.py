'''
Written by Lukasz Komza for Artificial Intellgence 1 at the Bergen County Academies

cnf_to_sudoku.py prints a solved suodku puzzle for a corresponding  CNF expression.

'''
sudoku_board=[]
for i in range(9):
	sudoku_board.append([])
	for j in range(9):
		sudoku_board[i].append(0)
working=True
while(working):
	line = input()
	if(line[0]=='c' or line[0]=='s'):
		continue
	line = line.split()
	for thing in line:
		if(thing=="0"):
			working=False
			break
		if(thing!='v'):
			if((int)(thing)>0):
				sudoku_board[(int)(thing[0])-1][(int)(thing[1])-1]=((int)(thing[2]))
for line in sudoku_board:
	print(line)