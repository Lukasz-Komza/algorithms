'''
Written by Lukasz Komza for Artificial Intellgence 1 at the Bergen County Academies

8-puzzle.py contains implementations of DFS, BFS, Hill Climbing,
Greedy Best, and A* search algorithms to solve a sliding puzzle.

'''
from collections import deque
import heapq
INF = float('inf')

#### Part 1: Problem Representation #################################################
### 1a. Implement PuzzleBoard, which represents a configuration of an n-by-n sliding puzzle.

class PuzzleBoard :

    def __init__(self, tiles) :
        board = []
        for i in range(len(tiles)):
            board.append([])
            for j in range(len(tiles)):
                board[i].append(tiles[i][j])
                if(tiles[i][j]==0): # Finds the zero position while creating the puzzleboard
                    self.zero=[i,j]
            board[i] = tuple(board[i])
        self.board = tuple(board)

    def __str__(self) :
        str_list = []
        for row in range(self.get_size()):
            for col in range(self.get_size()):
                str_list.append("{:2d} ".format(self.get_tile_at(row,col)))
            str_list.append("\n")
        return "".join(str_list)

    def __eq__(self, other) :
        return (isinstance(other, PuzzleBoard)
                and (self.board == other.board))

    def __hash__(self) :
        return hash(self.board)

    def get_tile_at(self, row, col) :
        if(row>=0 and col>=0 and row<len(self.board) and col<len(self.board)):
            return self.board[row][col]
        return 0

    def get_size(self) :
        return len(self.board)

    def is_goal(self) :
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if(self.board[i][j] != len(self.board)*i+j):
                    return False
        return True

    def get_neighbors(self) :
        x,y=self.zero
        neighbors=[]
        t=[]
        for i in range(len(self.board)):
            t.append(list(self.board[i])) # Makes a new board that's mutable
        if(x>0):
            t[x][y] = t[x-1][y]
            t[x-1][y] = 0
            neighbors.append(PuzzleBoard(t))
            t[x-1][y] = t[x][y]
            t[x][y] = 0
        if(y>0):
            t[x][y] = t[x][y-1]
            t[x][y-1]=0
            neighbors.append(PuzzleBoard(t))
            t[x][y-1] = t[x][y]
            t[x][y] = 0
        if(x!=len(self.board)-1):
            t[x][y] = t[x+1][y]
            t[x+1][y] = 0
            neighbors.append(PuzzleBoard(t))
            t[x+1][y] = t[x][y]
            t[x][y] = 0
        if(y!=len(self.board)-1):
            t[x][y] = t[x][y+1]
            t[x][y+1]=0
            neighbors.append(PuzzleBoard(t))
            t[x][y+1] = t[x][y]
            t[x][y] = 0
        return neighbors

### 1b. Implement AbstractState, which serves as a general wrapper for PuzzleBoard. 

class AbstractState:

    def __init__(self, snapshot, parent, path_length) :
        self.snapshot = snapshot
        self.parent = parent
        self.path_length = path_length

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        return (isinstance(other, AbstractState)
                and (self.snapshot == other.snapshot))

    def __hash__(self):
        return hash(self.snapshot)

    def get_snapshot(self) :
        return self.snapshot

    def get_parent(self) :
        return self.parent

    def get_path_length(self) :
        return self.path_length

    def get_neighbors(self) :
        states = []
        boards = self.snapshot.get_neighbors()
        for board in boards:
            if(self.parent==None or board!=self.parent.snapshot):
                states.append(AbstractState(board, self, self.path_length+1))
        return states

#### Part 2: Uninformed Search #################################################
### 2a. Implement DFSPuzzleSolver, which performs Depth-First Search with backtracking to a limited depth.

class DFSPuzzleSolver:

    def __init__(self, initial_board, graph_search = True, max_depth = INF) :
        stack=[AbstractState(initial_board, None, 0)]
        self.solution = None
        self.enqueues = 1
        self.extends = 0
        extended = set()
        while(stack!=[]):
            current = stack.pop()
            if(current.path_length>max_depth):
                continue
            if(graph_search):
                if(current in extended):
                    continue
                else:
                    extended.add(current)
            self.extends += 1
            if(current.snapshot.is_goal()):
                self.solution = current
                break
            neighbors = current.get_neighbors()
            for state in neighbors:
                stack.append(state)
                self.enqueues+=1

    def num_moves(self) :
        if(self.solution==None):
            return None
        return self.solution.path_length

    def num_enqueues(self) :
        return self.enqueues

    def num_extends(self) :
        return self.extends

    def get_solution(self) :
        solve = []
        state = self.solution
        for i in range(state.path_length):
            solve.append(state)
            state = state.parent
        return solve

### 2b. Implement BFSPuzzleSolver, which performs Breadth-First Search 

class BFSPuzzleSolver:

    def __init__(self, initial_board, graph_search = True) :
        queue = deque([AbstractState(initial_board, None, 0)])
        self.solution = None
        self.enqueues = 1
        self.extends = 0
        extended = set()
        while(queue!=[]):
            current = queue.popleft()
            if(graph_search):
                if(current in extended):
                    continue
                else:
                    extended.add(current)
            self.extends += 1
            if(current.snapshot.is_goal()):
                self.solution = current
                break
            neighbors = current.get_neighbors()
            for state in neighbors:
                queue.append(state)
                self.enqueues+=1

    def num_moves(self) :
        if(self.solution==None):
            return None
        return self.solution.path_length

    def num_enqueues(self) :
        return self.enqueues

    def num_extends(self) :
        return self.extends

    def get_solution(self) :
        solve = []
        state = self.solution
        for i in range(state.path_length):
            solve.append(state)
            state = state.parent
        return solve

### 2c. Go back and add optional "graph-search" to both DFSPuzzleSolver and BFSSolver; if the graph_search 
### parameter is set to True, the algorithm should avoid re-exploring states. 

#### Part 3: Informed Search #################################################
### 3a. First, implement these two heuristic functions. 

def hamming(board):
    h=0
    for i in range(len(board.board)):
        for j in range(len(board.board)):
            if(board.board[i][j]!=len(board.board)*i+j): # Checks if its the expected value
                h+=1
    return h

def manhattan(board):
    m=0
    l=len(board.board)
    for i in range(l):
        for j in range(l):
            if(board.board[i][j]!=0):
                m+=abs(i-int(board.board[i][j]/l))+abs(j-board.board[i][j]%l) # Subtracts the expected positions from the actual positions
    return m
    
### 3b. Implement HllClimbingPuzzleSolver, which perform Hill-Climbing search
### with backtracking to a limited depth.

class HillClimbingPuzzleSolver:

    def __init__(self, initial_board, graph_search = False, heuristic_fn = manhattan, max_depth = INF) :
        stack=[AbstractState(initial_board, None, 0)]
        self.solution = None
        self.enqueues = 1
        self.extends = 0
        extended = set()
        while(stack!=[]):
            current = stack.pop()
            if(current.path_length>max_depth):
                continue
            if(graph_search):
                if(current in extended):
                    continue
                else:
                    extended.add(current)
            self.extends += 1
            if(current.snapshot.is_goal()):
                self.solution = current
                break
            t = current.get_neighbors()
            neighbors = []
            for state in t:
                neighbors.append([heuristic_fn(state.snapshot),state])
            neighbors.sort(reverse=True)
            for s in neighbors:
                stack.append(s[1])
                self.enqueues+=1

    def num_moves(self) :
        if(self.solution==None):
            return None
        return self.solution.path_length

    def num_enqueues(self) :
        return self.enqueues

    def num_extends(self) :
        return self.extends

    def get_solution(self) :
        solve = []
        state = self.solution
        for i in range(state.path_length):
            solve.append(state)
            state = state.parent
        return solve

### 3c. Implement GreedyBestPuzzleSolver, which perform Greedy Best-first search
### using a given heuristic.

class GreedyBestPuzzleSolver:

    def __init__(self, initial_board, graph_search = False, heuristic_fn = manhattan) :
        h=[]
        heapq.heappush(h, [heuristic_fn(initial_board), AbstractState(initial_board, None, 0)])
        self.solution = None
        self.enqueues = 1
        self.extends = 0
        extended = set()
        while(h!=[]):
            current = heapq.heappop(h)
            if(graph_search):
                if(current[1] in extended):
                    continue
                else:
                    extended.add(current[1])
            self.extends += 1
            if(current[1].snapshot.is_goal()):
                self.solution = current[1]
                break
            t = current[1].get_neighbors()
            neighbors = []
            for state in t:
                neighbors.append([heuristic_fn(state.snapshot),state])
            for state in neighbors:
                heapq.heappush(h, state)
                self.enqueues+=1

    def num_moves(self) :
        if(self.solution==None):
            return None
        return self.solution.path_length

    def num_enqueues(self) :
        return self.enqueues

    def num_extends(self) :
        return self.extends

    def get_solution(self) :
        solve = []
        state = self.solution
        for i in range(state.path_length):
            solve.append(state)
            state = state.parent
        return solve

### Part 4: Optimal Search ###################################################

def zero_heuristic(board):
    return 0

### 4a. Implement AStarPuzzleSolver, which perform A* Search
### using a given heuristic.

class AStarPuzzleSolver:

    def __init__(self, initial_board, graph_search = False, heuristic_fn = manhattan) :
        h=[]
        heapq.heappush(h, [heuristic_fn(initial_board), AbstractState(initial_board, None, 0)])
        self.solution = None
        self.enqueues = 1
        self.extends = 0
        extended = set()
        while(h!=[]): #PROBLEM 37 PROVES MANHATTAN IS FUUUUUCCCCCCKKKKKKEEEEEDDDDDD
            current = heapq.heappop(h)
            if(graph_search):
                if(current[1] in extended):
                    continue
                else:
                    extended.add(current[1])
            self.extends += 1
            if(current[1].snapshot.is_goal()):
                self.solution = current[1]
                break
            neighbors = current[1].get_neighbors()
            for state in neighbors:
                heapq.heappush(h, [heuristic_fn(state.snapshot)+state.path_length,state])
                self.enqueues+=1

    def num_moves(self) :
        if(self.solution==None):
            return None
        return self.solution.path_length

    def num_enqueues(self) :
        return self.enqueues

    def num_extends(self) :
        return self.extends

    def get_solution(self) :
        solve = []
        state = self.solution
        for i in range(state.path_length):
            solve.append(state)
            state = state.parent
        return solve