from a1_state import State
class Agent:
    '''An Agent class that models a player capable of making strategic decisions in the Hinger game.'''
    def __init__(self, name: str = "A9", modes: list[str] = ['minimax']):
        '''
        prams:
            name: str - The name of the agent.
            modes: list[str] - A list of modes the agent can operate in, such as 'minimax', 
            'expectimax', 'alpha-beta', or 'mcts'.
        '''
        self.name = name
        self.modes = modes if modes else ['minimax'] # [minimax, expectimax, alpha-beta, mcts]

    def __str__(self):
        '''Return a string representation of the Agent instance.'''
        return f"Agent(name={self.name}, modes={self.modes})"

    def next_move(self, state, mode: str = 'minimax'):
        '''Determine the next move based on the current state.'''
        if mode == 'minimax':
            best_score = float('-inf')
            best_move = None

            for move in state.successors():
                new_state = move
                score = self.minimax(new_state, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_move
        else:
            raise NotImplementedError("This mode is not implemented yet.")

    def minimax(self, state: State, is_maximizing: bool = True, depth: int = 0):
        '''Implement the minimax algorithm to determine the best move.'''
        raise NotImplementedError("Minimax algorithm not implemented yet.")

def tester():
    '''Test the Agent class functionality.'''
    agent = Agent(name="TestAgent", modes=['minimax', 'expectimax'])
    print(agent)
    try:
        agent.next_move(None)
    except NotImplementedError as e:
        print(f"Caught expected exception: {e}")

if __name__ == "__main__":
    tester()
  
