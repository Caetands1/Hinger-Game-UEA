class Agent:
    '''An Agent class that models a player capable of making strategic decisions in the Hinger game.'''
    def __init__(self, name: str = "A9", modes: list[str] = ['minimax']):
        self.name = name
        self.modes = modes if modes else ['minimax'] # [minimax, expectimax, alpha-beta, mcts]

    def __str__(self):
        '''Return a string representation of the Agent instance.'''
        return f"Agent(name={self.name}, modes={self.modes})"

    def next_move(self, state, mode: str = 'minimax'):
        '''Determine the next move based on the current state.'''
        raise NotImplementedError("This method should be overridden by subclasses.")

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
  
