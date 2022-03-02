# Author: Chandan Sohi
# GitHub username: sohic
# Date: 3/1/2022
# Description: Portfolio Project - BattleShip Game

class ShipGame:
    """This class represents a Battle Ship Game between two players.  There 11 total methods and are as below:
        1.  __init__ - initializes all the data members
        2.  place_ship - used to place the player ship on the respective board
        3.  get_current_state - returns the current state of the game
        4.  get_num_ships_remaining - returns number of ships remaining for a given player
        4.  _get_row_index - returns numerical row index for given row letter
        5.  _get_row_letter - returns the letter for given row index
        6.  _valid_location - checks to see if given location exist on game board
        7.  _check_squares - checks if the grid squares where a ship is being placed are empty
        8.  _mark_ships - marks grid squares to have a ship present, ship total is adjusted, and all grid locations
        covered by the ship are recorded
        9.  _add_ship_to_player_total - increases player ship total by 1
        10. _remove_ship_from_player_total - decreases player ship total by 1
        11. fire_torpedo - check to see if fire torpedo hits a ship and adjust ship and grid location accordingly"""

    def __init__(self):
        """Method __init__ initializes all data members within the class.  All members are private.  There is a data
        member for the state of the game (_state), for player turn (_turn), for player 1 board (_board_1), for player
        2 board (_board_2), for ship totals for the two players (_ship_total_1 and _ship_total_2), and for locations for
        the two players where the ships are placed (_ships_loc_1 and _ships_loc_2).  This method takes no parameters."""

        self._state = "UNFINISHED"
        self._turn = "FIRST"
        self._board_1 = [["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""]]
        self._board_2 = [["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""],
                         ["", "", "", "", "", "", "", "", "", ""]]
        self._ships_total_1 = 0
        self._ships_total_2 = 0
        self._ships_loc_1 = []
        self._ships_loc_2 = []

    def place_ship(self, player, squares, start, orientation):
        """method place_ship takes the following as parameters:  player, number of squares, starting position, and
        orientation.  The method runs a number of checks to see if the move is valid.  If the move is not valid the
        method returns False, else if the move is valid, the method returns True.

        This method calls the following methods:
            1.  _valid_location - to check if the start location is valid location on the board and get row and column
            if the location is valid.
            2.  _get_row_index - to get the index number for the game board corresponding with the row letter
            3.  _check_squares - to check if a ship is already present on the grid locations intended for the ship to be
            placed upon.
            4.  _mark_ships - to place ship on grid locations indicated"""

        # check if the ship length is valid
        if int(squares) < 2:
            return False
        length = int(squares)

        # check if start location is valid
        if self._valid_location(start) is False:
            return False

        # get row letter and column number from method _valid_location
        row, col = self._valid_location(start)
        # get row index number from method _get_row_index
        row_index = self._get_row_index(row)
        # calculate column index
        col_index = col - 1

        # check if the orientation parameter is either "C" or "R"
        if orientation.upper() not in "CR":
            return False

        orientation = orientation.upper()

        # check if move will finish within valid grid
        if orientation == "R" and col_index + length - 1 > 9:
            return False
        if orientation == "C" and row_index + length - 1 > 9:
            return False

        # check for valid player name (either first or second)
        if player.upper() != "FIRST":
            if player.upper() != "SECOND":
                return False

        player = player.upper()

        # check if a ship already exists on destination squares
        if self._check_squares(player, orientation, length, row_index, col_index) is False:
            return False
        # mark ships on game board by calling method _mark_ships
        self._mark_ships(player, orientation, length, row_index, col_index)
        return True

    def get_current_state(self):
        """Method get_current_state takes no parameters and returns the current state of the game."""
        return self._state

    def get_num_ships_remaining(self, player):
        """Method get_num_ships_remaining takes a player as a parameter and returns the number of ships remaining for
        that player."""
        if player.upper() == "FIRST":
            return self._ships_total_1
        if player.upper() == "SECOND":
            return self._ships_total_2
        return

    def _get_row_index(self, location):
        """Method _get_row_index returns the index number corresponding to the letter for row (which needs to be between
        A and J) if the game state is "UNFINISHED" else it returns False"""
        if self._state != "UNFINISHED":  # check game state
            return False

        letters = "ABCDEFGHIJ"
        for index in range(0, 10):
            if letters[index] == location[0].upper():
                return index
        return False

    def _get_row_letter(self, row_index):
        """Method _get_row_letter returns the letter corresponding to the index number for row (which needs to be
        between 0 and 9) if the game state is "UNFINISHED" else it returns False"""

        if self._state != "UNFINISHED":  # check game state
            return False

        letters = "ABCDEFGHIJ"
        for index in range(0, 10):
            if index == int(row_index):
                return letters[index]
        return False

    def _valid_location(self, location):
        """Method _valid_location takes a location on the board and checks if it is valid.  It determines if the row
        letter is between A and J and if the integer portion is between 1 and 10.  The method also checks the state of
        the game and returns FALSE if it is not "UNFINISHED".  For valid locations, the function returns a list of the
        row letter and column integer ([row, col])."""

        if self._state != "UNFINISHED":
            return False

        row = location[:1].upper()
        col = int(location[1:])

        # check to see if row letter is between A and J
        if row.upper() not in "ABCDEFGHIJ":  # check row
            return False
        # check to see if column number is between 1 and 10
        if col not in range(1, 11):  # check column
            return False

        return [row, col]  # returns row and column if valid

    def _check_squares(self, player, orientation, length, row_index, col_index):
        """Method _check_square check to see if any squares where a ship is being placed is already occupied.  The
        method takes the player, orientation, length, row_index, and col_index as parameters.  The method returns True
        if all the squares are previously empty, else it returns False."""

        # determine which board to look at
        if player == "FIRST":
            board = self._board_1
        else:
            board = self._board_2

        # for ships placed in row wise orientation
        if orientation == "R":
            for index in range(0, length):
                if board[row_index][col_index + index] == "X":
                    return False

        # for ships placed in column wise orientation
        if orientation == "C":
            for index in range(0, length):
                if board[row_index + index][col_index] == "X":
                    return False
        return True

    def _mark_ships(self, player, orientation, length, row_index, col_index):
        """Method _mark_ships places the ships on the board by placing an "X" on appropriate squares on the board.  The
        method takes the player, orientation, length, row_index, and col_index as parameters.  The method also adds all
        marked squares to the appropriate ship_loc list as well as add 1 to the total number of ships for the player.

        This method calls the following methods:
            1.  _get_row_letter - to get the letter for row corresponding to the index number
            2.  _add_ship_to_player_total - to add ship to the player total"""

        # check which board and ship_loc list to look at
        if player == "FIRST":
            board = self._board_1
            ship_loc = self._ships_loc_1
        else:
            board = self._board_2
            ship_loc = self._ships_loc_2

        # if the ship is in row wise orientation
        if orientation == "R":
            ship = []  # initializing
            for index in range(0, length):
                board[row_index][col_index + index] = "X"
                spot = self._get_row_letter(row_index) + str(col_index + index + 1)
                ship.append(spot)
            self._add_ship_to_player_total(player)  # call method to add ship to player total
            ship_loc.append(ship)  # append ship_loc list which keeps track of all marked squares on the board

        # if the ship is in column wise orientation
        if orientation == "C":
            ship = []   # initialize
            for index in range(0, length):
                board[row_index + index][col_index] = "X"
                spot = self._get_row_letter(row_index + index) + str(col_index + 1)
                ship.append(spot)
            self._add_ship_to_player_total(player)  # call method to add ship to player total
            ship_loc.append(ship)  # append ship_loc list which keeps track of all marked square on the board
            return True
        return

    def _add_ship_to_player_total(self, player):
        """Method _add_ship_to_player_total increments the players' ship total by 1.  The only parameter passed to the
        method is the player."""

        if player == "FIRST":
            self._ships_total_1 += 1
        if player == "SECOND":
            self._ships_total_2 += 1
        return

    def _remove_ship_from_player_total(self, player):
        """Method _remove_ship_from_player_total reduces the player's ship total by 1.  The only parameter passed to the
        method is the player."""

        if player.upper() == "FIRST":
            self._ships_total_2 -= 1
        if player.upper() == "SECOND":
            self._ships_total_1 -= 1
        return

    def fire_torpedo(self, player, square):
        """Method fire_torpedo takes a player and grid location as parameters.  The method checks the player to see if
        it is that player's turn, returns False if it isn't.  Then the method checks to see if the grid location is
        valid, returns False if it isn't.  If valid, check's the grid location on the opposing player's board to see if
        a ship is placed there, if not it returns False.  If the ship exists at that location, it removes that grid
        location from the opposing player's ship_loc list.  Then checks the ship_loc list sub-list (which represent
        ships) to see if any of them are length 0, which indicates that the entire ship has been sunk.  If so, the ship
        is removed from the list and the count for the number of ships is reduced appropriately.

        This method calls the following methods:
            1.  _valid_location - to see if the fired upon location is valid and on the board
            2.  _get_row_index - to get the index number corresponding to the row letter
            3.  _remove_ship_from_player_total - to remove ship from player total"""

        # check player turn
        if self._turn != player.upper():
            return False
        if self._state != "UNFINISHED":
            return False

        # initialize values
        ship_loc = None
        board = None
        message = None

        # determine which board and lists to look at, determine status change message in case move results in victory
        if player.upper() == "FIRST":  # if first player
            board = self._board_2       # look at player 2 board
            ship_loc = self._ships_loc_2
            message = "FIRST_WON"
            self._turn = "SECOND"  # update turn
        if player.upper() == "SECOND":  # if 2nd player
            board = self._board_1       # look at player 1 board
            ship_loc = self._ships_loc_1
            message = "SECOND_WON"
            self._turn = "FIRST"        # update turn

        # check if square is a valid location on the board
        if self._valid_location(square) is False:
            return False
        else:
            row, col = self._valid_location(square)  # get row, col from _valid_location method
        row_index = self._get_row_index(row)  # get row index from _get_row_index method
        col_index = col - 1

        # check ship_loc list to see if board location has ship on it
        for ship in ship_loc:
            if square in ship:  # if there is a ship, change the grid to blank ad remove the ship from ship_loc list
                board[row_index][col_index] = ""
                ship.remove(square)
            if len(ship) == 0:  # check all ships (sub-lists) in ship_loc for length, remove if length = 0
                ship_loc.remove(ship)
                self._remove_ship_from_player_total(player)  # remove ship from player total
            if len(ship_loc) == 0:
                self._state = message  # if length of ship_loc is 0 (meaning no ships) change game state
        return True
