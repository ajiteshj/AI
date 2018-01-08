#!/usr/bin/python
import sys

board = []
position = []
player = "X"
opponent = "O"
depth = 0

def evaluationFunction(currPosition):
	sum = 0
	for i in range(8):
		for j in range(8):
			if currPosition[i][j] == player:
				sum = sum + board[i][j]
			elif currPosition[i][j] != "*":
				sum = sum - board[i][j]
	return sum
	
def checkUp(row, col, nextPlayer):
	if row > 1 and position[row - 1][col] == nextPlayer or position[row - 1][col] == "*":
		return -1
	for i in reversed(range(0, row - 1)):
		if(position[i][col] == nextPlayer):
			return i
	return -1

def checkDown(row, col, nextPlayer):
	if row < 6 and position[row + 1][col] == nextPlayer or position[row + 1][col] == "*":
		return -1
	for i in reversed(range(row + 2, 8)):
		if(position[i][col] == nextPlayer):
			return i
	return -1

def checkLeft(row, col, nextPlayer):
	if col > 1 and position[row][col - 1] == nextPlayer or position[row][col - 1] == "*" :
		return -1
	for i in reversed(range(0, col - 1)):
		if(position[i][col] == nextPlayer):
			return i
	return -1

def checkRight(row, col, nextPlayer):
	if col < 6 and position[row][col + 1] == nextPlayer or position[row - 1][col] == "*":
		return -1
	for i in reversed(range(col + 2, 8)):
		if(position[i][col] == nextPlayer):
			return i
	return -1
	
def validPosition(row, col, nextPlayer):
	if checkUp(row, col, nextPlayer) != -1:
			return 1
	if checkLeft(row, col, nextPlayer) != -1:
			return 2
	if checkRight(row, col, nextPlayer) != -1:
			return 3
	if checkDown(row, col, nextPlayer) != -1:
			return 4
	return 0
	
def changeBoard(row, col, nextPlayer, val):
	if val == 1:
		for i in reversed(range(0, row)):
			if position[i][col] != nextPlayer:
				board[i][col] = nextPlayer
			else:
				return
	if val == 2:
		for i in reversed(range(0, col)):
			if position[row][i] != nextPlayer:
				board[row][i] = nextPlayer
			else:
				return
	if val == 3:
		for i in reversed(range(col + 1, 8)):
			if position[row][i] != nextPlayer:
				board[row][i] = nextPlayer
			else:
				return
	if val == 1:
		for i in reversed(range(row + 1, 8)):
			if position[i][col] != nextPlayer:
				board[i][col] = nextPlayer
			else:
				return
	
	
def playMaxGame(currBoard, currDepth):
	if(currDepth == int(depth)):
		return evaluationFunction(currBoard)
	bestEval = -100000
	bestRow = 0
	bestCol = 0
	for i in range(8):
		for j in range(8):
			val = validPosition(i, j, player)
			if val != 0:
				temp = changeBoard(i, j, player, val)
				tempEval = playMinGame(temp, currDepth + 1)
				if tempEval > bestEval:
					bestEval = tempEval
					bestRow = i
					bestCol = j
	return bestEval
				
def playMinGame(currBoard, currDepth):
	if(currDepth == int(depth)):
		return evaluationFunction(currBoard)
	bestEval = 100000
	bestRow = 0
	bestCol = 0
	for i in range(8):
		for j in range(8):
			val = validPosition(i, j, opponent)
			if val != 0:
				temp = changeBoard(i, j, opponent, val)
				tempEval = playMaxGame(temp, currDepth + 1)
				if tempEval < bestEval:
					bestEval = tempEval
					bestRow = i
					bestCol = j
	return bestEval

def initializeBoard():
		global board
		with open('board.txt', 'r') as f:
			for line in f:
				mat = []
				for s in line.split(' '):
					mat.append(int(s))
				board.append(mat)
		return
		
def readInput():
	global position
	global player
	global depth
	f = open("input.txt")
	player = f.readline()
	player = player.strip()
	depth = f.readline()
	depth = depth.strip()
	for line in f:
		line = line.strip()
		position.append(list(line))
	if player == "O":
		opponent = "X"
	return
		
def main():
	readInput()
	initializeBoard()
	playMaxGame(board, 0)
	return 0

if __name__ == '__main__':
	main()
