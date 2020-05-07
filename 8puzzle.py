from random import randrange

class EightPuzzle:
    def __init__(self):
        self.grid = [randrange(8), randrange(8), randrange(8), randrange(8), randrange(8), randrange(8), randrange(8), randrange(8)]

    @staticmethod
    def isGoal(grid):
        attacks = EightPuzzle.numberOfAttacks(grid)
        if attacks == 0:
            return True
        else:
            return False

    @staticmethod
    def numberOfAttacks(grid):
        attacks = 0
        for i in range(0, 8):
            row = grid[i]
            for j in range(0, 8):
                if not j == i:
                    if grid[j] == row:
                        #check sideways
                        attacks += 1
                    if grid[j] == abs(j-i) + row:
                        #check diagonals above
                        attacks += 1
                    if grid[j] == row - abs(j-i):
                        #check diagonals below
                        attacks += 1
        return attacks

    @staticmethod
    def successors(grid):
        successors = []
        for i in range(0, 8):
            for move in [-1, 1]:
                newGrid = grid.copy()
                newGrid[i] += move
                if newGrid[i] >= 0 and newGrid[i] < 8:
                    node = Node(newGrid, EightPuzzle.numberOfAttacks(newGrid))
                    successors.append(node)
        successors.append(Node(grid, EightPuzzle.numberOfAttacks(grid)))
        return successors

from queue import PriorityQueue
import math

class Node:
    def __init__(self, grid, h):
        self.grid = grid
        self.h = h
    
    def __lt__(self, other):
        return self.h < other.h

class AI:
    @staticmethod
    def hillClimbing(puzzle):
        current = Node(puzzle.grid, puzzle.numberOfAttacks(puzzle.grid))
        loops = 0
        while True:
            loops += 1
            successors = puzzle.successors(current.grid)
            q = PriorityQueue()
            list(map(q.put, successors))
            bestNeighbor = q.get()
            if bestNeighbor.h >= current.h:
                return (current.grid, puzzle.numberOfAttacks(current.grid), puzzle.isGoal(current.grid), loops)
            else:
                current = bestNeighbor
                
    @staticmethod
    def stochasticHillClimbing(puzzle):
        current = Node(puzzle.grid, puzzle.numberOfAttacks(puzzle.grid))
        loops = 0
        while True:
            loops += 1
            successors = puzzle.successors(current.grid)
            randomIndex = randrange(len(successors))
            randNeighbor = successors[randomIndex]
            if puzzle.isGoal(randNeighbor.grid):
                return (randNeighbor.grid, loops)
            else:
                current = randNeighbor
    
    @staticmethod
    def randomRestartHillClimbing(puzzle):
        current = Node(puzzle.grid, puzzle.numberOfAttacks(puzzle.grid))
        loops = 0
        while True:
            loops += 1
            successors = puzzle.successors(current.grid)
            q = PriorityQueue()
            list(map(q.put, successors))
            bestNeighbor = q.get()
            if puzzle.isGoal(bestNeighbor.grid):
                return (bestNeighbor.grid, loops)
            else:
                current = bestNeighbor
                if randrange(1000) < 1:
                    #random new board
                    puzzle = EightPuzzle()
                    current = Node(puzzle.grid, puzzle.numberOfAttacks(puzzle.grid))

    @staticmethod
    def simulatedAnnealing(puzzle, schedule):
        current = Node(puzzle.grid, puzzle.numberOfAttacks(puzzle.grid))
        loops = 0
        for t in range(0, 1000):
            T = schedule(t)
            if T == 0:
                return (current.grid, loops, puzzle.isGoal(current.grid))
            loops += 1
            successors = puzzle.successors(current.grid)
            randomIndex = randrange(len(successors))
            randNeighbor = successors[randomIndex]
            if puzzle.isGoal(randNeighbor.grid):
                return (randNeighbor.grid, loops, True)
            else:
                delta = current.h - randNeighbor.h
                denom = math.exp(delta / T)
                if delta > 0 or (denom > 0.000000000001 and randrange(round(1 / denom)) < 1):
                    current = randNeighbor
        return (current.grid, current.h, loops, puzzle.isGoal(current.grid))
    
    @staticmethod
    def exp_schedule(k=20, lam=0.002, limit=10000):
        "One possible schedule function for simulated annealing"
        return lambda t: k * math.exp(-lam * t) if (t < limit) else 0

ai = AI()
puzzle = EightPuzzle()
# print(ai.hillClimbing(puzzle))               
# print(ai.stochasticHillClimbing(puzzle))  
# print(ai.randomRestartHillClimbing(puzzle))                 
print(ai.simulatedAnnealing(puzzle, AI.exp_schedule()))