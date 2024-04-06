INF = float('infinity')
[X, O, EMPTY] = ['x', 'o', '-']


class Board:
    def __init__(self, starting_player, human, ai):
        """
        Creates an empty board with the starting player
        :param starting_player: The player to move first ('x' or 'o')
        """
        self.board: list[list[str]] = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]
        self.current_player = starting_player

        self.human = human
        self.ai = ai

    def __str__(self):
        output = ''
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                cell = self.board[i][j]
                output += cell
            output += f' | {i * 3 + 1}{i * 3 + 2}{i * 3 + 3}\n'
        # [:-1] to remove trailing newline
        return output[:-1]

    def empty_cells(self) -> list[list[int, int]]:
        """
        Return coordinates for all EMPTY columns
        :return: A list of empty cell coordinates (e.g. [[0,2], [2,1]])
        """
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == EMPTY:
                    moves.append([row, col])
        return moves

    def winner(self) -> str | None:
        """
        Checks the board for winning states and returns the winning player, if any
        :return: self.human or self.ai depending on who won, None if tie
        """
        b = self.board
        win_states = [
            # Horizontal
            [b[0][0], b[0][1], b[0][2]],
            [b[1][0], b[1][1], b[1][2]],
            [b[2][0], b[2][1], b[2][2]],
            # Vertical
            [b[0][0], b[1][0], b[2][0]],
            [b[0][1], b[1][1], b[2][1]],
            [b[0][2], b[1][2], b[2][2]],
            # Diagonal
            [b[0][0], b[1][1], b[2][2]],
            [b[2][0], b[1][1], b[0][2]]
        ]

        if [self.ai, self.ai, self.ai] in win_states:
            return self.ai
        elif [self.human, self.human, self.human] in win_states:
            return self.human
        else:
            return None

    def is_game_over(self) -> bool:
        """
        The game is over if no more moves can be made or the game has a winner
        :return: True if no more empty cells, or has winner
        """
        return len(self.empty_cells()) == 0 or self.winner() is not None

    def end_turn(self) -> None:
        """
        Swaps the current player
        """
        if self.current_player == self.human:
            self.current_player = self.ai
        else:
            self.current_player = self.human

    def apply(self, move: list[int, int]) -> None:
        """
        Sets a specified cell to be the current player
        :param move:
        :return:
        """
        row, col = move
        self.board[row][col] = self.current_player
        self.end_turn()

    def undo(self, move: list[int, int]) -> None:
        """
        Reverts cell to empty (EMPTY).
        :param move: The cell position to revert
        """
        row, col = move
        self.board[row][col] = EMPTY
        self.end_turn()


def evaluate(board: Board) -> int:
    winner = board.winner()
    if not winner:
        return 0
    elif winner is board.ai:
        return 1
    else:
        return -1


def minimax(board: Board, depth: int, is_ai: bool) -> int:
    # Base case: heuristic evaluation
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if is_ai:
        best_score = -INF
        for move in board.empty_cells():
            board.apply(move)
            score = minimax(board, depth - 1, board.current_player == board.ai)
            board.undo(move)
            best_score = max(score, best_score)
    else:
        best_score = INF
        for move in board.empty_cells():
            board.apply(move)
            score = minimax(board, depth - 1, board.current_player == board.ai)
            board.undo(move)
            best_score = min(score, best_score)

    return best_score


def think(board: Board, difficulty=9):
    best_score = -INF
    best_move = None
    for move in board.empty_cells():
        board.apply(move)
        score = minimax(board, difficulty, board.current_player == board.ai)
        board.undo(move)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def main() -> None:
    player = ''
    ai = ''
    first = ''
    board = None

    # Player select
    while True:
        player = input('Play as X or O? [x/o] ').lower()
        if player == X:
            ai = O
            break
        elif player == O:
            ai = X
            break

    print(f'Playing as {player.upper()} against {ai.upper()}')

    # Starting player
    while True:
        is_player_first = input(f'Go first as {player.upper()}? [y/n] ').lower()
        if is_player_first == 'y':
            first = player
            break
        elif is_player_first == 'n':
            first = ai
            break

    board = Board(first, player, ai)

    # Main game loop
    while not board.is_game_over():

        print(board)

        if board.current_player == player:
            move = input('Make a move [1..9]: ')

            if not move.isdigit():
                print('Usage:\n\t"<row>,<column>"')
                print('Example:\n\t3,3 for bottom-right column')
                continue

            row = (int(move) - 1) // 3
            col = (int(move) - 1) % 3

            if [row, col] not in board.empty_cells():
                print('Illegal move!')
                continue

            board.apply([row, col])

        elif board.current_player == ai:

            print('AI is thinking...')

            best_move = think(board)
            board.apply(best_move)

        else:
            raise RuntimeError(f'Current player is {board.current_player} but expected {player} or {ai}.')

    # Endgame
    if board.winner():
        print(f'Player {board.winner().upper()} won the game!')
    else:
        print('The game was a tie!')


if __name__ == '__main__':
    while True:
        main()
        if input('Play again? [Y/n] ') == 'n':
            break
