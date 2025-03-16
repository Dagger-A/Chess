# Superclass for all pieces. Every piece has a color (white or black), starting position, captured status, and a boolean
# to determine if the piece has been moved.
# Also contains setter and getter for position, getter for is_white and is_captured, and 2
# setters to mark a piece as captured/uncaptured.
class Piece:
    def __init__(self, is_white, position):
        self._is_white = is_white
        self._is_captured = False
        self._position = position

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position

    def is_white(self):
        return self._is_white

    def capture(self):
        self._is_captured = True

    def un_capture(self):
        self._is_captured = False

    def is_captured(self):
        return self._is_captured


# Subclasses for each piece with two methods:

# 1.) An is_legal_move method, which accepts an array containing the coordinates
# of the destination square. It determines if the move fits within the general
# movement rules for that piece by comparing it to the origin square (i.e. A rook can move vertically or horizontally
# in any direction). is_legal_move does NOT check if a move is out of bounds, if a piece of the same color is in the
# way, if the origin and destination square are the same,
# or if the king will move into checkmate. That is done in the ChessGame module.

# 2.) A __str__ method containing the unicode character of that chess piece. For use with the print_board function in
# the ChessGame module. There are two return values, one for each color.

# Definition for pawn includes two extra data attributes.
# First, a boolean called has_moved which keeps track of if the pawn has moved yet. A setter and getter method
# are included to help return the pawn to its original state after testing a move.
# Second, an int called move_when_capturable_en_passant. Pawns can be captured en passant on the immediate next turn if
# they move 2 forward on their first turn. This variable stores the turn number in which that capture can occur
# (which will be set in the ChessGame module). Initially set to 0, if the pawn doesn't move forward 2 on its first move,
# it should never change from 0. A setter and getter is included for move_when_capturable_en_passant.
class Pawn(Piece):
    def __init__(self, is_white, position):
        Piece.__init__(self, is_white, position)
        self.__has_moved = False
        self.__move_when_capturable_en_passant = 0

    def has_previously_moved(self):
        return self.__has_moved
    
    def set_has_moved(self, has_moved):
        self.__has_moved = has_moved

    def get_move_when_capturable_en_passant(self):
        return self.__move_when_capturable_en_passant

    def set_move_when_capturable_en_passant(self, turn):
        self.__move_when_capturable_en_passant = turn

    # Checks to see if the given move is legal for a pawn.
    # A pawn may only move upwards (if white) or downwards (if black) one space per turn, with two exceptions.
    # 1) Pawns can move two spaces for its first move. 2) Pawns may move diagonally to capture
    # a piece (cannot capture vertically)
    def is_legal_move(self, move):

        # Pawns can move two spaces for its first move.
        if not self.__has_moved:

            # A white pawn may only move upwards.
            if self._is_white:
                if move[0] == self._position[0] and move[1] == self._position[1] + 2:
                    # Move is valid, return true. Change first move flag to false
                    return True

            # A black pawn may only move downwards.
            else:
                if move[0] == self._position[0] and move[1] == self._position[1] - 2:
                    # Move is valid, return true. Change first move flag to false
                    return True

        # Pawns can only move one space forward after its first turn, unless it is capturing. Then, it
        # moves one space diagonally. Whether it is capturing a piece or not is determined in the ChessGame module,
        # so for now, both possibilities return true (one forward, or one diagonal)
        # A white pawn may only move upwards.
        if self._is_white:
            if move[0] in [self._position[0] - 1, self._position[0],
                           self._position[0] + 1] and move[1] == self._position[1] + 1:
                # Move is valid
                return True

            # Move is invalid
            return False

        # A black pawn may only move downwards.
        else:
            if move[0] in [self._position[0] - 1, self._position[0],
                           self._position[0] + 1] and move[1] == self._position[1] - 1:
                # Move is valid
                return True

            # Move is invalid
            return False

    def __str__(self):
        if self._is_white:
            # return "\u265f"  # Command prompt renders the black pawn emoji improperly
            return "\u29eb"
        return "\u2659"


class Bishop(Piece):
    def __init__(self, is_white, position):
        Piece.__init__(self, is_white, position)

    # Bishops may move any amount of squares diagonally
    def is_legal_move(self, move):

        # Determine if the bishop is moving diagonally
        if abs(self._position[0] - move[0]) == abs(self._position[1] - move[1]):
            return True

        # If the bishop isn't moving diagonally, move is illegal
        else:
            return False

    def __str__(self):
        if self._is_white:
            return "\u265d"
        return "\u2657"


class Knight(Piece):
    def __init__(self, is_white, position):
        Piece.__init__(self, is_white, position)

    # Knights can only move to one of eight relative locations: up 1 and right 2, up 2 and right 1, down 1 and right 2,
    # down 2 and right 1, up 1 and left 2, up 2 and left 1, down 1 and left 2, or down 2 and left 1.
    def is_legal_move(self, move):

        # Determine if the knight is moving to one of the eight relative locations
        if [abs(self._position[0] - move[0]), abs(self._position[1] - move[1])] in [[2, 1], [1, 2]]:
            return True

        # If it did not move properly, return false
        else:
            return False

    def __str__(self):
        if self._is_white:
            return "\u265e"
        return "\u2658"


# Rook definition includes has_moved boolean to handle cases in which the user wants to castle.
# Also includes setter and getter for has_moved.
class Rook(Piece):
    def __init__(self, is_white, position):
        Piece.__init__(self, is_white, position)
        self.__has_moved = False

    def has_previously_moved(self):
        return self.__has_moved

    def set_has_moved(self, has_moved):
        self.__has_moved = has_moved

    # Rooks can move any amount of spaces horizontally or vertically
    def is_legal_move(self, move):

        # Determine if the rook is moving horizontally
        if self._position[1] == move[1]:
            return True

        # Determine if the rook is moving vertically
        elif self._position[0] == move[0]:
            return True

        # If the rook isn't moving horizontally or vertically, move is illegal
        else:
            return False

    def __str__(self):
        if self._is_white:
            return "\u265c"
        return "\u2656"


class Queen(Piece):
    def __init__(self, is_white, position):
        Piece.__init__(self, is_white, position)

    # The queen can move any amount of squares in any direction (vertical, horizontal, diagonal).
    def is_legal_move(self, move):

        # Determine if the queen is moving horizontally
        if self._position[1] == move[1]:
            return True

        # Determine if the queen is moving vertically
        elif self._position[0] == move[0]:
            return True

        # Determine if the queen is moving diagonally
        elif abs(self._position[0] - move[0]) == abs(self._position[1] - move[1]):
            return True

        # If the queen isn't moving horizontally, vertically, or diagonally, move is illegal
        else:
            return False

    def __str__(self):
        if self._is_white:
            return "\u265b"
        return "\u2655"


# King definition includes has_moved boolean to handle cases in which the user wants to castle.
# Also includes setter and getter for has_moved.
class King(Piece):
    def __init__(self, is_white, position):
        Piece.__init__(self, is_white, position)
        self.__has_moved = False

    def has_previously_moved(self):
        return self.__has_moved

    def set_has_moved(self, has_moved):
        self.__has_moved = has_moved

    # The king can move one space in any direction. If it is castling,
    # it may move two spaces horizontally (only valid on its first move).
    def is_legal_move(self, move):

        # King may move two horizontally on first move to castle. (Has_moved is not checked for here. This is
        # because if the player wants to castle, there is a special function (castle_is_invalid) that will check for
        # has_moved and will print a unique error message. If is_legal_move returns false, the move_is-invalid function
        # will print a generic error message and castle_is_invalid will never be called.)
        if abs(move[0] - self._position[0]) == 2 and move[1] == self._position[1]:
            return True

        # Iterate over every square surrounding the king (this includes the origin square, but the ChessPieces module
        # will ensure that the origin and destination square aren't the same)
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:

                # If the move is next to the origin square, move is legal
                if [self._position[0] - move[0], self._position[1] - move[1]] == [x, y]:
                    return True

            # If it isn't, move is illegal
        return False

    def __str__(self):
        if self._is_white:
            return "\u265a"
        return "\u2654"
