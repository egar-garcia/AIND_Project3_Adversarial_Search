import pickle
import queue
from isolation import Isolation, DebugState

# Loading the opening book form a pickle file
with open("data.pickle", "rb") as f:
    book = pickle.load(f)

# Creating the initial state (a blank board)
initial_statate = Isolation()

# Displaying the initial move taken by the first player
first_move_state = initial_statate.result(book[initial_statate])
print('OPENING MOVE FOR PLAYER 1')
print(DebugState().from_state(first_move_state))

# Displaying the reply taken by the second player
response_move_state = first_move_state.result(book[first_move_state])
print('BEST REPLY BY PLAYER 2')
print(DebugState().from_state(response_move_state))