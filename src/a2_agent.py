from a1_state import State

"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes an agent class for Task 2

@author: {B26} (100464375, 100457714, 100500854, and 100501057)
@date:   26/11/2026

"""


class Agent:
    '''An Agent class that models a player capable of making strategic decisions in the Hinger game.'''
    def __init__(self, name: str = "A9", modes: list[str] = None, max_depth: int = 4):
        '''
        params:
            name: str - The name of the agent.
            modes: list[str] - A list of modes the agent can operate in, such as 'minimax', 
            'alpha-beta', or 'mcts'.
        '''
        self.name = name
        self.modes = modes if modes else ['minimax', 'alphabeta'] # [minimax, alpha-beta, mcts]
        self.max_depth = max(1, int(max_depth))

    def __str__(self):
        '''Return a string representation of the Agent instance.'''
        return f"Agent(name={self.name}, modes={self.modes})"

    def legal_moves(self, state: State):
        """Return all legal moves as letters A-Y."""
        moves = []
        for row, col, counters in state.cells():
            if counters > 0:
                letter = chr(ord('A') + row * 5 + col)
                moves.append(letter)
        return moves

    def evaluate_move(self, state: State, letter: str) -> int:
        '''Evaluate the potential score of a move based on its position and neighboring cells.'''
        index = ord(letter) - ord('A')
        row, col = divmod(index, 5)
        cost = sum(
            1 for r, c in state.neighbours((row, col))
            if state.grid[r][c] > 0
        )
        bonus = 100 if state.isHinger(row, col) else 0
        return bonus - cost

    def next_move(self, state, mode: str = 'minimax') -> str | None:
        '''
        Determine the next move based on the current state.\n
        Returns None when no counters remain.\n
        Search values are score differences from the viewpoint of the player
        whose turn it is.
        '''
        if state is None:
            raise TypeError("state must be a State object, not None")

        if mode not in self.modes:
            raise ValueError(
                f"Invalid mode {mode}; this agent accepts {self.modes}"
            )

        moves = self.legal_moves(state)
        if not moves:
            return None  # No valid moves available
        # Order moves to improve search efficiency
        moves.sort(key=lambda move: self.evaluate_move(state, move), reverse=True)

        total_counters = sum(counters for _, _, counters in state.cells())
        depth = min(self.max_depth, total_counters)  # Limit depth to avoid excessive computation

        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for move in moves:
            reward = self.evaluate_move(state, move)
            new_state = state.clone()
            new_state.move(move)

            if mode == 'minimax':
                score = reward + self.minimax(new_state, False, depth - 1)
            elif mode == 'alphabeta':
                raise NotImplementedError("Alphabeta mode is not implemented yet.")
            elif mode == 'mcts':
                raise NotImplementedError("MCTS mode is not implemented yet.")
            else:
                raise ValueError(f"Invalid mode {mode}; this agent supports {self.modes}")

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, state: State, is_maximizing: bool = True, depth: int | None = None) -> float:
        '''Return the minimax value of the current player's position.'''
        # raise NotImplementedError("Minimax algorithm not implemented yet.")
        if depth is None:
            depth = self.max_depth

        if depth <= 0 or state.is_terminal():
            return 0

        best_value = float('-inf') if is_maximizing else float('inf')
        moves = self.legal_moves(state)
        moves.sort(
            key=lambda move: self.evaluate_move(state, move),
            reverse=is_maximizing
        )

        for move in moves:
            # Calculate immediate reward (bonus - cost)
            reward = self.evaluate_move(state, move)

            # Create a new state to pass without modifying the original
            new_state = state.clone()
            new_state.move(move)

            # Evaluate the opponent's position
            future_value = self.minimax( new_state, not is_maximizing, depth - 1)

            # Include the reward from the current move
            if is_maximizing:
                value = reward + future_value
                best_value = max(best_value, value)
            else:
                value = -reward + future_value
                best_value = min(best_value, value)            
        return best_value

    def alphabeta(self, state: State, is_maximizing: bool = True, alpha: float = float('-inf'), beta: float = float('inf'), depth: int | None = None) -> float:
        raise NotImplementedError("Alphabeta algorithm not implemented yet.")


def tester():
    '''Test the Agent class functionality.'''
    sample_grid = [
        [1, 1, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1],
    ]
    agent = Agent(name="TestAgent", modes=['minimax', 'alphabeta'], max_depth=3)
    state = State(sample_grid)
    print(agent)
    print("Initial board:")
    print(state)

    try:
        # The agent returns a single legal move and does not alter the input.
        original_grid = state.clone().grid

        #move_minimax = agent.next_move(state, "minimax") test
        minimax_next_move = agent.next_move(state, "minimax")
        assert minimax_next_move in agent.legal_moves(state)
        assert state.grid == original_grid
        print("Minimax move:", minimax_next_move)

        #move_alphabeta = agent.next_move(state, "alphabeta") test
        """
        alphabeta_next_move = agent.next_move(state, "alphabeta")
        assert alphabeta_next_move in agent.legal_moves(state)
        assert state.grid == original_grid
        print("Alpha-beta move:", alphabeta_next_move)
        """

        # On a completely empty board algorithm should return None.
        assert agent.next_move(State([[0] * 5 for _ in range(5)])) is None

        print("All Task 2 tests passed.")
    except NotImplementedError as e:
        print(f"Caught expected exception: {e}")

if __name__ == "__main__":
    tester()
  
