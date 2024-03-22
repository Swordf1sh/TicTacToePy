from enum import Enum
from random import choice


# Enum class for the players in the game
class PlayerSign(Enum):
    ONE = 'X'  # Player one is represented by 'X'
    TWO = 'O'  # Player two is represented by 'O'


class PlayerType(Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    USER = 'user'


class Player:
    def __init__(self, player_sign: PlayerSign, player_type: PlayerType):
        self.player_sign = player_sign
        self.player_type = player_type
        self.value = player_sign.value

    @property
    def is_easy(self):
        return self.player_type is PlayerType.EASY

    @property
    def is_medium(self):
        return self.player_type is PlayerType.MEDIUM

    @property
    def is_hard(self):
        return self.player_type is PlayerType.HARD

    @property
    def is_user(self):
        return self.player_type is PlayerType.USER


# Class for the Tic Tac Toe game
class TicTacToe:

    # Constructor for the TicTacToe class
    def __init__(self, player_one_type: PlayerType, player_two_type: PlayerType):
        """
        Constructor for the TicTacToe class.
        :param player_one_type:
        :param player_two_type:
        """

        self.player_one = Player(player_sign=PlayerSign.ONE, player_type=player_one_type)
        self.player_two = Player(player_sign=PlayerSign.TWO, player_type=player_two_type)

        # Create the game board
        pattern = '_________'
        self.board = [[c.replace('_', ' ') for c in pattern[_i:_i + 3]] for _i in range(0, 9, 3)]

        self.player = self.player_one

    @property
    def player_opponent(self):
        return self.player_one if self.player == self.player_two else self.player_two

    def get_random_empty_cell(self):
        """
        Returns the coordinates of a random empty cell on the board.
        """
        all_empty_cells = [(j + 1, i + 1) for i in range(3) for j in range(3) if self.board[j][i] == ' ']
        return choice(all_empty_cells)

    # Method to switch the current player
    def next_player(self):
        """
        Switches the current player.
        """
        self.player = self.player_one if self.player == self.player_two else self.player_two

    # Method to place a move on the board
    def _place_move(self, x: int, y: int) -> bool:
        """
        Places a move on the board.

        :param x: The x-coordinate of the move.
        :param y: The y-coordinate of the move.
        """
        if self.board[x - 1][y - 1] != ' ':
            print('This cell is occupied! Choose another one!')
            return False
        self.board[x - 1][y - 1] = self.player.value
        return True

    # Method to check if a player has won the game
    def check_win(self, minmax=False) -> bool or (bool, Player):
        """
        Checks if a player has won the game.
        """
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                if not minmax:
                    print(f'{self.player.value} wins')
                return True if not minmax else True, 10 if self.player.value == row[0] else -10

        # Check columns
        for _i in range(3):
            if self.board[0][_i] == self.board[1][_i] == self.board[2][_i] != ' ':
                if not minmax:
                    print(f'{self.player.value} wins')
                return True if not minmax else True, 10 if self.player.value == self.board[0][_i] else -10

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ' or \
                self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            if not minmax:
                print(f'{self.player.value} wins')
            return True if not minmax else True, 10 if self.player.value == self.board[1][1] else -10

        # Check for a draw
        if all(c != ' ' for row in self.board for c in row):
            if not minmax:
                print('Draw')
            return True if not minmax else True, 0

        return False

    # Method to handle a player's move
    def ask_for_coordinates(self) -> bool:
        """
        Handles a player's move.
        """
        try:
            _coordinates = list(map(int, input('Enter the coordinates: ').split()))
        except ValueError:
            print('You should enter numbers!')
            return False

        if len(_coordinates) != 2 or not all(1 <= c <= 3 for c in _coordinates):
            print('Coordinates should be from 1 to 3!')
            return False

        if not self._place_move(*_coordinates):
            return False
        self.draw_board()
        return True

    def make_easy_move(self):
        """
        Makes a random move on the board.
        """
        print(f'Making move level "easy"')
        _x, _y = self.get_random_empty_cell()
        self._place_move(_x, _y)
        self.draw_board()

    def make_medium_move(self):
        print(f'Making move level "medium"')

        # check if it can win in the next move
        can_win, x, y = self._predict_medium_move(self.player)
        can_lose, x, y = self._predict_medium_move(self.player_one if self.player == self.player_two else self.player_two)
        if can_win:
            self._place_move(x, y)
        # check if the opponent can win in the next move

        elif can_lose:
            self._place_move(x, y)

        else:
            # if it can't win in the next move, it moves randomly
            _x, _y = self.get_random_empty_cell()
            self._place_move(_x, _y)
        self.draw_board()

    def make_hard_move(self):
        """
        Makes a move on the board using the minimax algorithm.
        :return:
        """
        print(f'Making move level "hard"')
        x, y = self._predict_hard_move()
        self._place_move(x + 1, y + 1)
        self.draw_board()

    def _predict_medium_move(self, player: Player) -> (bool, int, int):
        """
        Predicts the best move for the current player.
        :param player:
        :return:
        """
        winning_combinations = [[(i, j) for j in range(3)] for i in range(3)] \
                               + [[(j, i) for j in range(3)] for i in range(3)] \
                               + [[(i, i) for i in range(3)], [(i, 2 - i) for i in range(3)]]

        for combination in winning_combinations:
            values = [self.board[x][y] for x, y in combination]
            if values.count(player.value) == 2 and ' ' in values:
                return True, combination[values.index(' ')][0] + 1, combination[values.index(' ')][1] + 1

        return False, 0, 0

    def _predict_hard_move(self) -> (int, int):
        """
        Predicts the best move for the current player.
        :return:
        """
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.player.value
                    score = self._minimax(False, 0)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def _minimax(self, is_maximizing: bool, depth: int):
        """
        Minimax algorithm with alpha-beta pruning.
        :param is_maximizing:
        :param depth:
        :return:
        """
        game_result = self.check_win(minmax=True)
        if game_result:
            return game_result[1]

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.player.value
                        score = self._minimax(False, depth + 1)
                        self.board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.player_opponent.value
                        score = self._minimax(True, depth + 1)
                        self.board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    # Method to draw the game board
    def draw_board(self):
        """
        Draws the game board.
        """
        print('---------')
        for row in self.board:
            print('| ' + ' '.join(row) + ' |')
        print('---------')


def start_game(player_one: PlayerType, player_two: PlayerType):
    # Start of the game
    game = TicTacToe(player_one, player_two)
    game.draw_board()
    while True:
        if game.player.is_easy:
            game.make_easy_move()
        elif game.player.is_medium:
            game.make_medium_move()
        elif game.player.is_hard:
            game.make_hard_move()
        else:
            if not game.ask_for_coordinates():
                continue

        if game.check_win():
            break
        game.next_player()


def check_command(command) -> (bool, PlayerType, PlayerType):
    # check if split command len is 3
    if len(command.split()) != 3:
        return False
    # check if first word is 'start' and second and third word is 'easy' or 'user'
    _player_types = [t.value for t in PlayerType]
    if command.split()[0] != 'start' or command.split()[1] not in _player_types or command.split()[2] not in _player_types:
        return False
    return True, PlayerType(command.split()[1]), PlayerType(command.split()[2])


def menu():
    while True:
        command = input('Input command: ')
        if command == 'exit':
            break
        elif params := check_command(command):
            if params[0]:
                start_game(*params[1:])
        else:
            print('Bad parameters!')


if '__main__' == __name__:
    menu()
