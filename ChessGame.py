from ChessPieces import Pawn, Bishop, Knight, Rook, Queen, King

# Constants that represent board dimensions
MAX_RANK = 8
MAX_FILE = 8

# Dictionary of error messages, for use with move_is_invalid function
error_messages = {
    1: "Origin and destination square cannot be the same.",
    2: "Couldn't find selected piece. Ranks are a through h, files are 1 through 8.",
    3: "Couldn't find destination square. Ranks are a through h, files are 1 through 8.",
    4: "The piece selected to move is of the wrong color.",
    5: "Destination square is occupied.",
    6: "Move doesn't follow the movement rules for the selected piece. "
       "\nType \"rules\" if you wish to review the movement rules for each piece.",
    7: "Path is blocked.",
    8: "Pawns only move diagonally if they are capturing a piece.",
    9: "That move puts/leaves your king in check!",
    10: "Cannot castle, your king has previously moved.",
    11: "Cannot castle, you must castle with a rook, and no rook was found.",
    12: "Cannot castle, the rook you are trying to castle with has previously moved.",
    13: "Cannot castle, path is blocked.",
    14: "Cannot castle when your king is currently in check.",
    15: "Cannot castle, the square your king is crossing over is threatened by an opposing piece.",
    16: "Cannot castle, your king will be in check!"
}


def main():

    is_white_turn = True  # To keep track of whose turn it is
    turn_number = 0  # To keep track of the turn number
    move_count = 1  # Counts how many moves have elapsed (Needed in order to handle en passant captures correctly)
    threatening_piece = None  # To warn player if they are in check.
    # Set to none initially because there is no piece threatening the king yet

    # Instantiate the board
    # Instantiate all pieces. Both colors get eight pawns, two bishops, two knights, two rooks, one queen, and one king.
    board = [
        # White pieces
        Pawn(True, [0, 1]),
        Pawn(True, [1, 1]),
        Pawn(True, [2, 1]),
        Pawn(True, [3, 1]),
        Pawn(True, [4, 1]),
        Pawn(True, [5, 1]),
        Pawn(True, [6, 1]),
        Pawn(True, [7, 1]),

        Rook(True, [0, 0]),
        Rook(True, [7, 0]),

        Knight(True, [1, 0]),
        Knight(True, [6, 0]),

        Bishop(True, [2, 0]),
        Bishop(True, [5, 0]),

        Queen(True, [3, 0]),

        King(True, [4, 0]),

        # Black pieces
        Pawn(False, [0, 6]),
        Pawn(False, [1, 6]),
        Pawn(False, [2, 6]),
        Pawn(False, [3, 6]),
        Pawn(False, [4, 6]),
        Pawn(False, [5, 6]),
        Pawn(False, [6, 6]),
        Pawn(False, [7, 6]),

        Rook(False, [0, 7]),
        Rook(False, [7, 7]),

        Knight(False, [1, 7]),
        Knight(False, [6, 7]),

        Bishop(False, [2, 7]),
        Bishop(False, [5, 7]),

        Queen(False, [3, 7]),

        King(False, [4, 7]),
    ]

    # Print welcome message
    print_welcome_message()

    # Begin playing. Iterate until a winner has been determined
    while True:

        # If it is white's turn, one turn has passed. Increment turn counter
        if is_white_turn:
            turn_number += 1

        # Display board
        print_board(board)

        # If player is in check, print warning
        if threatening_piece is not None:
            print("CHECK!")

        # Print turn number
        print(f"Turn number {turn_number}. ", end='')

        # Get user input for move
        selected_piece, destination = get_move(board, is_white_turn)

        # Validate the move
        while err_code := move_is_invalid(board, selected_piece, destination, is_white_turn, move_count):

            # If it is invalid, print appropriate error message and re-prompt user for a new move
            print(f"Invalid move: {error_messages[err_code]}")
            selected_piece, destination = get_move(board, is_white_turn)

        # Execute the move
        execute_move(board, selected_piece, destination, move_count)

        # See if the player moved a pawn
        if isinstance(selected_piece, Pawn):

            # If so, check if it has reached the last file, and if it has, promote it
            promote_pawn(board, selected_piece)

        # Find the opposing king
        opposing_king = next((piece for piece in board if isinstance(piece, King)
                              and piece.is_white() != is_white_turn))

        # See if the opponent is in check so that they can be alerted next turn
        threatening_piece = piece_threatening_king(board, opposing_king, move_count)

        # Check for the end of the game
        if is_game_over(board, opposing_king, threatening_piece, move_count):

            # End the game if there is a winner/stalemate
            input("(Press Enter to exit) ")
            return

        # If there is no winner, the next player gets a turn.
        is_white_turn = not is_white_turn

        # Increment move counter (for en passant captures)
        move_count += 1


# Prints the welcome message. User hits enter to continue after reading.
def print_welcome_message():
    print("   ________                  ")
    print("  / ____/ /_  ___  __________ ")
    print(" / /   / __ \\/ _ \\/ ___/ ___/")
    print("/ /___/ / / /  __/__  |__  / ")
    print("\\____/_/ /_/\\___/____/____/")
    print("      -Coded by Andrew Dagger\n")
    print("APPEARANCE:\n")
    print("\tThis game was intended to be played in a dark theme. If your terminal window is \n\tlight "
          "themed, the colors are all opposite.\n")
    print("\tOn Windows, white pawns render as off-center, purple emojis. So, \n\tI have decided to replace them with "
          "diamonds. Get it together, Microsoft.\n")
    print("USAGE:\n")
    print("\tTo move a piece, type the square in which it is located, followed by the \n\tsquare you wish to move it"
          " to. For example, If white wants to move its \n\tpawn located at a2 up two squares "
          "to a4, they would type \"a2 a4\".\n")
    print("\tTo castle the king, move the king two spaces in the direction you wish to castle. \n\tThe rook will be "
          "moved automatically. For example, If white wants \n\tto castle on the queen (left) side, they would type"
          " \"e1 c1\". If it is a valid move, \n\tthe king will be moved to c1 and the leftmost rook to d1.\n")
    print("\tAt the beginning of your turn, you may type \"rules\" to \n\treview the movement rules for each piece, "
          "or \"usage\" to \n\tremind yourself how to move pieces.\n")
    input("Ready? press enter.")


# Prints the board and a list of pieces that are captured
def print_board(board):
    empty = None  # For checking if a piece is in a square

    # Iterate over every rank and file
    print()
    for file in range(MAX_FILE - 1, -1, -1):
        print(file + 1, end=' ')
        for rank in range(MAX_RANK):

            # Iterate over every piece
            for piece in board:

                # If a piece is at the given rank and file, print it
                empty = True
                if piece.get_position() == [rank, file] and not piece.is_captured():
                    print(f"{piece} ", end='')
                    empty = False
                    break

            # If square is empty, print a white/black square
            if empty:

                # Black squares are even
                if (file + rank) % 2 == 0:
                    print("\u25a1\u2003", end='')

                # White are odd
                else:
                    print("\u25a0\u2003", end='')
        print()

    # Print files
    # print("  \u200aᴬ\u200b\u200aᴮ\u2000 ᶜ \u2000ᴰ \u2000ᴱ \u2000ᶠ  ᴳ \u200a\u200aᴴ")  # for pycharm
    print("  a b c d e f g h")

    # Print captured pieces
    print("\nCaptured pieces: ")
    for piece in board:
        if piece.is_captured():
            print(f"{piece} ", end='')
    print("\n")


# Prompts the user for a move and checks the format of the input. Ensures that two squares were selected, that
# they are within bounds, and that a piece was selected.
# Re-prompts user until they give valid input. Returns a reference to selected piece, and destination square coordinates
def get_move(board, is_white_turn):

    selected_piece = None  # To hold the piece chosen by the user

    # Get user input for move
    while True:

        # Prompt if it is white's turn
        if is_white_turn:
            move = input("White, enter move: ").strip().lower().split()

        # Prompt if it is black's turn:
        else:
            move = input("Black, enter move: ").strip().lower().split()

        # See if user is requesting help
        if move == ["rules"]:
            print_movement_rules()
            print_board(board)
            continue
        if move == ["usage"]:
            print_usage()
            print_board(board)
            continue

        # Ensure user selected two squares
        if len(move) != 2:
            print("Expected two squares to be selected. Type \"usage\" for more info.")
            continue

        # Ensure that the two selected squares have exactly two coordinates
        if len(move[0]) != 2 or len(move[1]) != 2:
            print("There should be 2 coordinates for each square, even though 3D chess is a cool idea.\n"
                  "Type \"usage\" for more info.")
            continue

        # Assign coordinates to origin and destination squares
        origin = [ord(move[0][0]) - 97, ord(move[0][1]) - 49]
        destination = [ord(move[1][0]) - 97, ord(move[1][1]) - 49]

        # Ensure that a piece was selected.
        for piece in board:
            if origin == piece.get_position() and not piece.is_captured():
                selected_piece = piece

        # If a piece wasn't selected, print error message and re-prompt
        if selected_piece is None:
            print(f"Invalid move: Expected to find a piece at {move[0]} but found an empty square.")
            continue

        # If input is in correct format, return the move
        return selected_piece, destination


# Prints information regarding the movement rules for each piece,
# as well as how castling and capturing en passant works.
def print_movement_rules():
    print("MOVEMENT RULES:\n")
    print("\tPawns (\u2659) generally move one space vertically towards the opponents side, \n\twith some exceptions: "
          "Pawns cannot capture moving vertically, but they \n\tcan move one space forwards diagonally to capture a "
          "piece. They have the \n\toption to move two spaces vertically only on their first turn.\n")
    print("\tRooks (\u2656) can move vertically or horizontally any number of spaces. "
          "\n\tThey may also castle with the king if neither piece has moved yet.\n")
    print("\tBishops (\u2657) can move diagonally any amount of spaces.\n")
    print("\tKnights (\u2658) move in an \'L\' shaped pattern. More specifically, they can \n\tmove either up/down one"
          " and left/right two, or up/down two and right/left one. \n\tAlso, knights can hop over "
          "pieces, meaning their path is never blocked.\n")
    print("\tQueens (\u2655) can vertically, horizontally, or diagonally any number of spaces.\n")
    print("\tKings (\u2654) can move one space in any direction. They may also castle with any rook if \n\tneither"
          " piece has moved yet. If an opposing player \n\tis one move away from capturing your king, that means"
          " your king is in \"check\". \n\tYou must remove the check on your next turn (by moving the king out of "
          "\n\tthe way or capturing/blocking the threatening piece), and any move that \n\tdoesn't do "
          "so is considered illegal. Also, any move \n\tthat puts your own king in check is illegal as well.\n")
    print("SPECIAL MOVES:\n")
    print("\tEn passant rule: When a pawn moves two spaces on its first turn, it is vulnerable \n\tto being captured"
          " en passant. This special type of capture occurs \n\tif an opposing player moves their pawn diagonally"
          " one space BEHIND the player's \n\tpawn, as if it had only moved one square. En passant captures must meet"
          " the following criteria: \n\n\t1.) A pawn can only be captured en passant if it has moved two squares on its"
          " first turn. \n\t2.) The opponent can only use a pawn to perform an en passant capture. \n\t3.) The opponent"
          " must perform the en passant capture on the turn immediately after \n\twhite's pawn moved, and no later."
          " \n\t4.) The opponent must move their pawn diagonally one space behind the pawn to capture it. \n\n\tHere "
          "is an example on how an en passant could be performed: \n\n\t1.) White moves its pawn at a2 to a4. \n\t2.) "
          "Black has a pawn on b4. On the turn immediately after white \n\tmoved its pawn, black moves its pawn to a3. "
          "\n\t3.) White's pawn has been captured en passant.\n")
    print("\tCastling: A king and a rook can castle if neither have moved yet. To castle, \n\tthe king moves two"
          " spaces towards the rook it is castling with, \n\tand the rook moves to the square behind the king. "
          "Castling must follow these rules: \n\n\t1.) It must be the first time either piece has been moved. \n\t2). "
          "The path between the king and the rook cannot be obstructed. \n\t3.) You cannot castle out of, through, or "
          "into check. \n\tFor example, say your king is castling from e1 to c1. For the castle to work, \n\tyour king "
          "cannot currently be in check, and squares d1 and c1 \n\tmust not be threatened by an opponent's piece."
          " \n\n\tHere is an example on how a castle can be performed: \n\n\t1.) White wants to castle its king at e1 "
          "with its rook at a1. \n\t2.) No piece is in between the king and the rook. \n\tThe king is not moving out "
          "of, through, or into check. \n\t3.) White moves its king two spaces to c1, and the rook \n\tto the "
          "space behind where the king moved (d1).\n")


# Prints information regarding how to give proper input.
def print_usage():
    print("\nUSAGE:\n")
    print("\tTo move a piece, type the square in which it is located, followed by the \n\tsquare you wish to move it"
          " to. For example, If white wants to move its \n\tpawn located at a2 up two squares "
          "to a4, they would type \"a2 a4\".\n")
    print("\tTo castle the king, move the king two spaces in the direction you wish to castle. \n\tThe rook will be "
          "moved automatically. For example, If white wants \n\tto castle on the queen (left) side, they would type"
          " \"e1 c1\". If it is a valid move, \n\tthe king will be moved to c1 and the leftmost rook to d1.\n")


# This function checks to see if the proposed move is invalid. If it is invalid, an int representing an error code is
# returned (to be used with error_messages dictionary), otherwise 0 is returned. The specific checks are as follows:
# A piece of the right color was selected, the destination and origin squares are not the same,
# destination square is not occupied by a piece of the same color, the move follows the movement rules for the selected
# piece, the path from the origin to the destination is unblocked, pawns moving diagonally are capturing a piece
# (including en passant captures), and the move doesn't put/leave the player's king in check.
def move_is_invalid(board, piece, destination, is_white_turn, move_count):

    origin = piece.get_position()   # To hold origin square

    # Ensure that origin and destination are different
    if origin == destination:
        return 1

    # Ensure both squares selected by user are in bounds (all ranks are a-h and files are 1-8)
    if origin[0] not in range(MAX_RANK) or origin[1] not in range(MAX_FILE):
        return 2
    if destination[0] not in range(MAX_RANK) or destination[1] not in range(MAX_FILE):
        return 3

    # Ensure that a piece of the right color was selected.
    if piece.is_white() != is_white_turn:
        return 4

    # Ensure that the destination does not contain a piece of the same color
    for chess_piece in board:
        if (destination == chess_piece.get_position() and chess_piece.is_white() == is_white_turn
                and not chess_piece.is_captured()):
            return 5

    # Check if user is attempting to castle
    if isinstance(piece, King) and abs(origin[0] - destination[0]) == 2 and origin[1] == destination[1]:

        # If they are, a special set of checks with their own error codes will execute and bypass the rest of the checks
        return castle_is_invalid(board, piece, destination, move_count)

    # Determine if destination is reachable based off of predefined movement rules for the piece.
    # Read ChessPieces module for more info
    if not piece.is_legal_move(destination):
        return 6

    # Ensure that the path to the destination is unblocked
    if not path_unblocked(board, piece, destination):
        return 7

    # Ensure that all diagonally moving pawns are capturing properly (checks for en passant captures as well)
    if (isinstance(piece, Pawn) and origin[0] != destination[0]
            and not pawn_captures_properly(board, piece, destination, move_count)):
        return 8

    # Ensure that the proposed move does not leave the player's king in check
    if move_leaves_king_in_check(board, piece, destination, move_count):
        return 9

    # If the move passes all checks, it is valid
    else:
        return 0


# Accepts a king object moving two squares horizontally. Determines if the user can castle by ensuring that there is a 
# rook the king can castle with, neither the king nor the rook its castling with have moved yet, that the king is not 
# moving out of, through, or into check, and that no piece is in the way. If the move is valid, returns the king and 
# rook objects that are castling. If not, returns an error code (to be used with error_messages dictionary).
def castle_is_invalid(board, king, destination, move_count):

    origin = king.get_position()  # To help with seeing if king is currently in, moving through, or into check

    # Ensure the king has not moved yet
    if king.has_previously_moved():
        return 10

    # Find the rook the king is castling with.
    rook = None                             # To hold the rook the king is castling with
    rank = 0 if destination[0] == 2 else 7  # If the king is moving left, the rook's file should be 0,
                                            # but if the king is moving right, the rook's file should be 7
    file = 0 if king.is_white() else 7      # The rook should be on the same file as the king.
    
    # Look for the rook (must be same color and be uncaptured)
    for piece in board:
        if (piece.get_position() == [rank, file] and piece.is_white() == king.is_white() 
                and not piece.is_captured() and isinstance(piece, Rook)):
            rook = piece
            break
    
    # Ensure a rook was found
    if rook is None:
        return 11
    
    # Ensure the rook hasn't moved yet
    if rook.has_previously_moved():
        return 12
    
    # Ensure there is no piece in between the rook and the king
    if not path_unblocked(board, rook, king.get_position()):
        return 13
    
    # Ensure the king is not currently in check
    if piece_threatening_king(board, king, move_count) is not None:
        return 14

    # Move the king one over, and see if it will be in check
    king.set_position(get_path(king, destination)[0])
    if piece_threatening_king(board, king, move_count) is not None:

        # Move king back to where it was and return error code
        king.set_position(origin)
        return 15
    
    # Move the king two over, and see if it will be in check
    king.set_position(destination)
    if piece_threatening_king(board, king, move_count) is not None:

        # Move king back to where it was and return error code
        king.set_position(origin)
        return 16

    # Move king back to where it was, return 0 to indicate valid move
    king.set_position(origin)
    return 0
    

# Validates that no pieces are blocking the proposed move
def path_unblocked(board, piece, destination):

    # Get piece origin
    origin = piece.get_position()

    # For every other piece, create an array of all squares that it will traverse, not including destination
    path = get_path(piece, destination)

    # Check that the path is free of pieces, and if it isn't, move is invalid
    for square in path:
        for chess_piece in board:
            if chess_piece.get_position() == square and not chess_piece.is_captured():
                return False

    # If a pawn is moving forwards, check the destination square for any pieces (pawns can't capture moving forwards).
    # If a piece of any color is in the way, return False. If not, return True.
    # NOTE: If a pawn is moving diagonally and a piece of the same color is at the destination, the
    # pawn_captures_properly function will handle it
    if isinstance(piece, Pawn) and origin[0] == destination[0]:
        for chess_piece in board:
            if chess_piece.get_position() == destination:
                return False

    # If move passes every check, move is valid
    return True


# Function accepts a chess piece object and its intended destination. Returns a list containing the coordinates of
# every square that it will cross to reach the destination, not including the destination square (because the get_move
# and path_unblocked functions already checks to see if the destination square is occupied).
def get_path(piece, destination):

    # Knights do not technically have a path since they hop over pieces, so return an empty list
    if isinstance(piece, Knight):
        return []

    # Get piece origin
    origin = piece.get_position()

    # Create an array of all squares that the given piece will traverse, not including destination
    path = []

    # Determine the change in the rank value (aka check for left or right movement)
    delta_x = 0

    # Check if it is moving right, and if so, change in rank is 1
    if origin[0] < destination[0]:
        delta_x = 1

    # Check if it is moving left, and if so, change in rank is -1. If none of the above is true,
    # there is no change in rank
    if origin[0] > destination[0]:
        delta_x = -1

    # Determine the change in the file value (aka check for upwards or downwards movement)
    delta_y = 0

    # Check if it is moving up, and if so, change in file is 1
    if origin[1] < destination[1]:
        delta_y = 1

    # Check if it is moving left, and if so, change in file is -1. If none of the above is true,
    # there is no change in file
    if origin[1] > destination[1]:
        delta_y = -1

    # Start at the adjacent square. If it isn't the destination square, add it to the path. Move to
    # next square and repeat the process until you reach the destination
    cursor = [origin[0] + delta_x, origin[1] + delta_y]
    while cursor != destination:
        path.append(cursor)
        cursor = [cursor[0] + delta_x, cursor[1] + delta_y]

    # Return the path
    return path


# Assumes given pawn moves 1 diagonally. Confirms that a capture is taking place. If the destination square contains a
# piece of opposite color, return True. If it is empty, check to see if an en passant capture is taking place.
# If it is, return true, and if not, return false.
def pawn_captures_properly(board, pawn, destination, move_count):
    origin = pawn.get_position()  # To hold the square in which the pawn is moving from

    # Ensure destination contains piece of opposite color, and if it does, return True
    for chess_piece in board:
        if chess_piece.get_position() == destination and chess_piece.is_white() != pawn.is_white():
            return True

    # If it doesn't, we can assume based on the previous checks that the square is empty. In this case, an en passant
    # capture might be taking place. Find the square in which the capture will take place (has the same rank as the
    # destination square and  the same file as the origin square), check if it contains a pawn, and check if it moved
    # two on the previous turn (making it capturable en passant). If all checks pass, a valid en passant capture is
    # taking place. return True.
    for chess_piece in board:
        if chess_piece.get_position() == [destination[0], origin[1]] and isinstance(chess_piece, Pawn):
            if chess_piece.get_move_when_capturable_en_passant() == move_count:
                return True

    # If the pawn is moving diagonally but not capturing a piece, move is invalid
    return False


# Temporarily executes the proposed move to see if it leaves the players king in check.
# If it does, returns True. If not, False.
def move_leaves_king_in_check(board, piece, destination, move_count):

    original_position = piece.get_position()  # To keep track of where piece was
    check = False  # To store the result of the function (allows for cleanup)
    reset_first_move = False  # To switch the has_moved variable back to its original state
    king = next((chess_piece for chess_piece in board if isinstance(chess_piece, King)  # Finds the player's king
                 and piece.is_white() == chess_piece.is_white()))

    # Kings, Rooks and Pawns have a has_moved variable, and by temporarily executing the move, has_moved may be
    # switched from False to True. This needs to be reset back to False when undoing the move.
    if ((isinstance(piece, King) or isinstance(piece, Rook) or isinstance(piece, Pawn))
            and not piece.has_previously_moved()):
        reset_first_move = True

    # Temporarily execute the move, and make note of the captured piece (if any) so it can be undone
    temporarily_captured_piece = execute_move(board, piece, destination, move_count)

    # Check if the move leaves the current players king in check
    if piece_threatening_king(board, king, move_count) is not None:

        # If it does, move is invalid.
        check = True

    # Return the board to its previous state by returning piece to its original destination, un-capturing any piece that
    # was captured, resetting en passant variable, and marking has_moved as true if the piece hasn't moved yet
    piece.set_position(original_position)
    if temporarily_captured_piece is not None:
        temporarily_captured_piece.un_capture()
    if isinstance(piece, Pawn) and piece.get_move_when_capturable_en_passant() == move_count:
        piece.set_move_when_capturable_en_passant(0)
    if reset_first_move:
        piece.set_has_moved(False)

    # Return the result of the check
    return check


# Executes the given move. Captures any piece at the destination square, and moves the piece there. Handles pawn
# captures, including en passant captures. If a pawn moves 2 forward on its first move, makes a note of the turn in
# which it is capturable en passant. Returns a reference to the piece captured so that the move_leaves_king_in_check
# function can undo the move (if a capture took place, else it returns None).
def execute_move(board, piece, destination, move_count):

    origin = piece.get_position()   # To hold the square in which the piece is moving from
    captured_piece = None   # To hold piece that is captured, if any

    # Check to see if user is castling (if they are moving king two spaces horizontally)
    if isinstance(piece, King) and abs(origin[0] - destination[0]) == 2:
        execute_castle(board, piece, destination)

        # Nothing else needs to happen. Return None since no pieces can be captured in a castle.
        return None

    # Check if a piece is being captured, and if it is, capture it
    for chess_piece in board:
        if chess_piece.get_position() == destination and not chess_piece.is_captured():
            captured_piece = chess_piece
            captured_piece.capture()
            break

    # Special cases for pawns:
    if isinstance(piece, Pawn):

        # Make sure has_moved is set to true
        piece.set_has_moved(True)

        # If a pawn is moving diagonally but there is no piece at the destination square,
        # an en passant capture is taking place.
        if origin[0] != destination[0] and captured_piece is None:

            # Find the pawn that is being captured en passant, and capture it
            for chess_piece in board:
                if chess_piece.get_position() == [destination[0], origin[1]]:
                    captured_piece = chess_piece
                    captured_piece.capture()
                    break

        # If a pawn is moving two squares, that makes it valid for en passant capture on the very next turn only.
        if destination[1] in [origin[1] + 2, origin[1] - 2]:
            piece.set_move_when_capturable_en_passant(move_count + 1)

    # Change has_moved to True for rooks and kings so they can't castle
    if isinstance(piece, King) or isinstance(piece, Rook):
        piece.set_has_moved(True)

    # Move piece
    piece.set_position(destination)

    # Return the piece that was captured (if any) so that the move_leaves_king_in_check
    return captured_piece


# Finds the rook the king is castling with, and performs the castle. Sets has_moved to True for both pieces.
# Assumes move is valid (already checked for in castle_is_valid function)
def execute_castle(board, king, destination):
    
    # Find the rook the king is castling with.
    rook = None  # To hold the rook the king is castling with
    rank = 0 if destination[0] == 2 else 7  # If the king is moving left, the rook's file should be 0,
    # but if the king is moving right, the rook's file should be 7
    file = 0 if king.is_white() else 7  # The rook should be on the same file as the king.

    # Look for the rook (must be same color and be uncaptured)
    for piece in board:
        if (piece.get_position() == [rank, file] and piece.is_white() == king.is_white()
                and not piece.is_captured() and isinstance(piece, Rook)):
            rook = piece
            break
            
    # Move rook to square king is crossing
    rook.set_position(get_path(king, destination)[0])
    
    # Move king to destination
    king.set_position(destination)
    
    # Both pieces have now moved.
    king.set_has_moved(True)
    rook.set_has_moved(True)


# Determines if the king of the current player is in check. Accepts king's position and returns a reference to the
# first piece found that is threatening the king. If no piece is threatening the king, returns None
def piece_threatening_king(board, king, move_count):

    # Iterate over every piece
    for chess_piece in board:

        # Determine if any moves from opposite color can capture king, and if so, return the threatening piece
        if (not move_is_invalid(board, chess_piece, king.get_position(), not king.is_white(), move_count)
                and not chess_piece.is_captured()):
            return chess_piece

    # If no piece is threatening the king, return None
    return None


# Function takes a reference to a pawn object. If the pawn has reached the end of the board, returns a reference to a
# new piece object with the same origin (thereby promoting it). If not, returns the pawn passed as an argument.
# User chooses the type of piece they wish to promote the pawn to (cannot be a pawn).
def promote_pawn(board, pawn):

    is_white = pawn.is_white()  # Holds color of pawn
    position = pawn.get_position()    # Holds current position of pawn

    # Ensure that the pawn has reached the end
    if (is_white and position[1] != MAX_FILE - 1) or (not is_white and position[1] != 0):

        # If it has not, pawn cannot be promoted. Return the pawn object
        return pawn

    # Remove the pawn to make room for the new piece
    board.remove(pawn)

    # Prompt user for the type of piece they wish to promote their pawn to
    print("Time to promote your pawn!")

    while True:
        selected_type = input("Enter the type of piece you wish to promote your "
                              "pawn to (Queen, Rook, Knight, or Bishop): ").strip().lower()

        # Find the type of piece the user selected and create a new one of that kind.
        # Loop until the user gives valid input
        match selected_type:
            case "queen":
                board.append(Queen(is_white, position))
                return
            case "rook":
                board.append(Rook(is_white, position))
                return
            case "knight":
                board.append(Knight(is_white, position))
                return
            case "bishop":
                board.append(Bishop(is_white, position))
                return
            case _:
                print("Invalid input, try again.")


# Determines if the end of the game has been reached.
# The game ends in stalemate if the king cannot move out of its current position, isn't in check, and is the last piece.
# The game ends in victory for a player if the opponent's king is in check and cannot get out of it by either moving the
# king, capturing the threatening piece, or blocking off the threatening piece. If the game ends, the results are
# printed to the user and the function returns True. If the game isn't over, returns False.
def is_game_over(board, king, threatening_piece, move_count):

    king_position = king.get_position()     # To hold position of king

    king_cannot_move = True            # See if there is any valid move left for the king
    king_is_last_piece = False          # See if the king is the last un-captured piece of its color
    in_check = False                    # See if the king is in check
    capturing_removes_check = False     # See if capturing the threatening piece (if possible) removes the check
    blocking_removes_check = False      # See if blocking the threatening piece's path (if possible) removes the check

    # Determine if there are any squares surrounding the king to which it could legally move to
    # Iterate over every surrounding square
    for rank in [-1, 0, 1]:
        for file in [-1, 0, 1]:

            # Check if the king can move
            if not move_is_invalid(board, king, [king_position[0] + rank, king_position[1] + file], king.is_white(),
                                   move_count):

                # If there is any legal move for the king left, set king_cannot_move to True
                king_cannot_move = False

    # If the king cannot move, see if it is currently in check
    if threatening_piece is not None:
        in_check = True

        # If king is in check, see if capturing the threatening piece removes the check
        for chess_piece in board:
            error = move_is_invalid(board, chess_piece, threatening_piece.get_position(), king.is_white(), move_count)
            if not error:

                # If it can, change capturing_removes_check to True, and break
                capturing_removes_check = True
                break

        # See if blocking the path of the threatening piece removes the check
        # Get the path of the threatening piece to the king
        path = get_path(threatening_piece, king_position)

        # See if any piece can move into the path and remove the check
        for square in path:
            for chess_piece in board:
                if not move_is_invalid(board, chess_piece, square, king.is_white(), move_count):

                    # If it can, change blocking_removes_check to True, and break
                    blocking_removes_check = True
                    break
                    # NOTE: Even if the threatening piece can be cut off or captured, doing so may lead to another piece
                    # putting the king in check, or maybe there are multiple pieces threatening the king.
                    # These possibilities are indirectly checked for here.

    # Determine if the king is last piece on the board of its color
    pieces_of_king_color = 0  # To hold amount of pieces that are the color of the given king (including king)

    # Count pieces of same color as king
    for piece in board:
        if piece.is_white() == king.is_white():
            pieces_of_king_color += 1

    # If king is last remaining, king_is_last_piece = True
    if pieces_of_king_color == 1:
        king_is_last_piece = True

    # If the king is not in check, cannot move, and is the last piece, game ends in a stalemate.
    # Print board one last time, print ending message, return True
    if not in_check and king_cannot_move and king_is_last_piece:
        print_board(board)
        print("GAME OVER! Oh no, looks like we have a stalemate! Nobody wins.")
        return True

    # If the king is in check and no move can remove the check, game ends in victory for opponent.
    # Print board one last time, print victory message, and return True
    if in_check and king_cannot_move and not capturing_removes_check and not blocking_removes_check:
        print_board(board)
        winner = "Black" if king.is_white() else "White"
        print(f"CHECKMATE!!! {winner} has won the game, congratulations!")
        return True

    # Keep playing
    return False


if __name__ == "__main__":
    main()
