import random
from sample_players import DataPlayer


class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # DONE: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)

        # Choosing a random move just to have a move in case of timeout         
        self.queue.put(random.choice(state.actions()))

        # If depth is 6 or less using an Opening Book,
        # otherwise using Iterative Deepening with Minimax and Alpha-Beta Pruning 
        if state.ply_count < 6 and state in self.data:
            self.queue.put(self.data[state])
        else:
            self.iterative_deepening(state)


    def iterative_deepening(self, state):
        depth = 1
        while True:
            self.queue.put(self.alpha_beta_search(state, depth))
            depth += 1


    def alpha_beta_search(self, state, depth):
        """
        Implementation of Minimax with Alpha-Beta pruning
        """
        alpha = float("-inf")
        beta = float("inf")
        best_score = None
        best_move = None

        for action in state.actions():
            value = self.min_value(state.result(action), depth - 1, alpha, beta)
            alpha = max(alpha, value)
            if best_score is None or value > best_score:
                best_score = value
                best_move = action

        return best_move


    def min_value(self, state, depth, alpha, beta):
        """
        Implementation of the min-value function as part of Minimax search
        """
        if state.terminal_test(): return state.utility(self.player_id)

        if depth <= 0: return self.score(state)

        value = float("inf")
        for action in state.actions():
            value = min(value, self.max_value(state.result(action), depth - 1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value


    def max_value(self, state, depth, alpha, beta):
        """
        Implementation of the max-value function as part of Minimax search
        """
        if state.terminal_test(): return state.utility(self.player_id)

        if depth <= 0: return self.score(state)

        value = float("-inf")
        for action in state.actions():
            value = max(value, self.min_value(state.result(action), depth - 1, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value


    def score(self, state):
        # Using the #my_moves - #opponent_moves heuristic
        return self.my_moves_vs_opponent_moves_heuristic(state)


    def my_moves_vs_opponent_moves_heuristic(self, state):
        """
        Implementation of the #my_moves - #opponent_moves heuristic
        """
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

