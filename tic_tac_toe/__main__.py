import collections
import typing


def main():
    board = Board()
    print(board)

    while True:
        i = int(input('>'))

        if board[i] in ['x', 'o']:
            continue
        board[i] = 'x'

        if winner := judge(board):
            print(f'{winner} wins')
            exit(0)

        minimax_player(board)

        print(board)
        print()

        if winner := judge(board):
            print(f'{winner} wins')
            exit(0)


# Subclassing list has a problem with copy method.
class Board(collections.UserList[str]):

    def __init__(self):
        super().__init__()
        self.clear()

    def __str__(self) -> str:
        return '\n'.join(
            ['|'.join(self[i:i + 3]) for i in range(0, len(self), 3)])

    def clear(self):
        self.data = [str(i) for i in range(9)]


def minimax_player(board: Board):
    score, move = minimax(board, 'o', 0)
    board[move] = 'o'


def minimax(board: Board, turn: str, depth: int) -> tuple[int, int]:
    scores = []
    for i in range(9):
        test_board = board.copy()
        if board[i] not in ['x', 'o']:
            test_board[i] = turn
            if winner := judge(test_board):
                if winner == 'x':  # lose
                    return -10 - depth, i
                elif winner == 'o':  # win
                    return 10 - depth, i
                else:
                    return 0 - depth, i
            scores.append(minimax(test_board, switch_turn(turn), depth + 1))

    # randomize
    if turn == 'x':
        return max(scores)
    else:
        return min(scores)


def judge(board: Board) -> typing.Optional[str]:
    if all([i in ['x', 'o'] for i in board]):
        return 'draw'

    for i in ['o', 'x']:
        if judge_player(board, i):
            return i

    return None


def judge_player(board: Board, player: str) -> bool:

    def judge_line(line: Board) -> bool:
        return all([i == player for i in line])

    col = any([judge_line(board[i:i + 3]) for i in range(0, 9, 3)])
    row = any([judge_line(board[i::3]) for i in range(3)])
    diagonal = judge_line(board[2:7:2]) or judge_line(board[::4])

    return col or row or diagonal


def switch_turn(turn: str) -> str:
    return 'o' if turn == 'x' else 'x'


if __name__ == '__main__':
    main()
