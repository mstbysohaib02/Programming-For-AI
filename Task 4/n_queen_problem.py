# Task 04
# Implementation of N queen problem (Dynamic)
def printBoard(chess,N) :
    for i in range(N):
        for j in range(N):
            print(chess[i][j],end=' ')
        print()

def isValid( chess, rows, cols, N) :	
	for i in range(rows):
		if chess[i][cols]==1:
			return False
	for i, j in zip(range(rows, -1, -1),range(cols, N, 1)):
		if chess[i][j]==1:
			return False
	for i, j in zip(range(rows, -1, -1),range(cols, -1, -1)):
		if chess[i][j]==1:
			return False
	return True
def recur_nqueen( chess, rows, N):
	if rows >= N:
		return True
	for i in range(N):
		if isValid(chess, rows, i, N) == True: 
			chess[rows][i] = 1
			if recur_nqueen(chess, rows + 1, N):
				return True
			chess[rows][i] = 0 
	return False

def NQueen(N):
    chess = [[0 for i in range(N+1)] for j in range(N+1)]
    if recur_nqueen(chess, 0, N) == 0:
        print("Solution not found !!")
        return
    printBoard(chess, N)
# for example
print("N Queen Problem :")
num = int(input("Enter the number of queens : "))
NQueen(num)