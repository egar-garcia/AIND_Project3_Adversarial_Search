import random
import pickle
from collections import defaultdict, Counter
from isolation import Isolation

NUM_ROUNDS = 1000000
#NUM_ROUNDS = 50000 # This is to get within the limits of the review tool
DEPTH = 6
DATA_FILE = 'data.pickle'

def build_table(num_rounds=NUM_ROUNDS):
    """
    Creates the table of opening moves,
    returns a dictionary with the game state as the key and
    the best found move as value.
    """

    # Creates a dictionary for counting purposes,
    # it has a game state as a key, and the values are other dictionaries.
    # This inner dictionaries have actions (taken in a particular state) as keys
    # and total reward (#won-matches - #lost-matches) as values
    book = defaultdict(Counter)

    for _ in range(num_rounds):
        state = Isolation() # Initial state (a blank board)
        build_tree(state, book)

    return {k: max(v, key=v.get) for k, v in book.items()}


def build_tree(state, book, depth=DEPTH):
    """
    Recursive function to explore the game states up to a given depth,
    and create the respective entries in the opening book.
    """
    # If the depth is 0 (i.e. the maximum depth to explore has been reached)
    # then performing a simulation for the rest of the game
    if depth <= 0 or state.terminal_test():
        return -simulate(state)

    # Taking a random action from the current state
    action = random.choice(state.actions())
    
    # Recursively calling this function to explore actions in deeper levels
    # reward would be 1 if the next player wins or -1 if it loses (i.e. the current player wins)
    reward = build_tree(state.result(action), book, depth - 1)

    # Updating the total reward of the taken action,
    # the more wins the higher the total reward  
    book[state][action] += reward

    # Returns the negative of the reward,
    # in order to adjust the result to the caller's perspective (i.e the other player's) 
    return -reward


def simulate(state):
    """
    Performs a simulation of the rest of a game, by choosing random moves.
    """
    # The current player
    player_id = state.player()

    # Performing random moves till the game ends
    while not state.terminal_test():
        state = state.result(random.choice(state.actions()))

    # Returns 1 if the current player wins, or -1 if it loses
    return -1 if state.utility(player_id) < 0 else 1


# Creating the opening book (dictionary),
# and storing it into the specified pickle file 
opening_book = build_table()
with open(DATA_FILE, 'wb') as f:
    pickle.dump(opening_book, f)
