from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Tuple
import copy
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for the frontend
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


X = 'X'
O = 'O'
EMPTY = None

class Move(BaseModel):
    row: int
    column: int

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

board = initial_state()

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Xcnt = 0
    Ocnt = 0
    for row in board:
        for item in row:
            if item == X:
                Xcnt += 1
            elif item == O:
                Ocnt += 1
    if Xcnt > Ocnt:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == None:
                actions.add((i, j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_move = action
    if player_move not in actions(board):
        raise ValueError(f"You can't make this move")
    row, column = player_move
    new_board = copy.deepcopy(board)
    new_board[row][column] = player(board)

    return new_board

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0
    raise Exception("Error of utility")

@app.get("/ai")
def minimax():
    """
    Returns the optimal action for the current player on the board.
    """
    global board
    if terminal(board):
        return None
    
    def max_value(board):
        if terminal(board):
            return utility(board), None
        
        v = float('-inf')
        
        best_action = None

        for action in actions(board):

            min_v , _ = min_value(result(board, action))
            
            if min_v > v:
                v = min_v
                best_action = action

        return v, best_action

    def min_value(board):
        if terminal(board):
            return utility(board), None
        
        v = float('inf')
        
        best_action = None
        for action in actions(board):

            max_v, _ = max_value(result(board, action))

            if max_v < v:
                v = max_v
                best_action = action
        
        return v, best_action
    
    # if player(board) == X:
    #     _, best_move = max_value(board)

    # else:
    _, best_move = min_value(board)

    return {"move" : best_move}

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for rows in board:  # Checking rows
        x_row = True
        o_row = True
        
        for item in rows:
            if item != X:
                x_row = False
            if item != O:
                o_row = False
        if x_row:
            return X
        if o_row:
            return O
    for col in range(len(board[0])):  # Checking columns
        x_col = True
        o_col = True
        for row in range(len(board)):
            if board[row][col] != X:
                x_col = False
            if board[row][col] != O:
                o_col = False
        if x_col:
            return X
        if o_col:
            return O
        
    diagonal_1 = {board[0][0], board[1][1], board[2][2]}   # Checking diagonals
    diagonal_2 = {board[0][2], board[1][1], board[2][0]}
    
    if diagonal_1 == {X} or diagonal_2 == {X}:
        return X
    if diagonal_1 == {O} or diagonal_2 == {O}:
        return O
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if len(actions(board)) == 0:                        
        return True
    elif winner(board) != None:
        return True
    else: 
        return False


@app.get("/board")
def get_board():
    return {"board": board}

@app.post("/move")
def make_move(move:Move):
    global board
    
    new_board = result(board, (move.row, move.column))
    
    if new_board:
        board = new_board
        if terminal(board):
            return {"status": "Game Over", "board": board, "winner": winner(board)}
    return {"board": board, "player": player(board)}

@app.get("/reset")
def reset_board():
    global board
    board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    return {"status": "Board reset", "board": board}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
