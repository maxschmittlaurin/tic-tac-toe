# Author : Maximilien Schmitt-Laurin
# Date : 31 octobre 2019

import numpy as np
from AI import AI
from Stack import Stack
from Queue import Replay

class TicTacToeGame:

    def __init__(self):

        # We initiate the grid and we put empty strings to symbolize that no move has been played
        self.board_state = np.zeros([3,3], dtype='str')

        self.previous_board_states = Stack()

        self.ai = AI()

        for i in range(len(self.board_state)):
            self.board_state[i] = " "

    def start_new_game(self):

        self.player_order = ""

        while self.player_order != "f" and self.player_order != "s":
            self.player_order = input("\nPress 'f' to play first or 's' to play second : ")

        game_over = False
        self.print_board()

        # Game loop
        while game_over == False:
            game_over = self.playTurn()

        self.reverse_previous_board_states = Stack()

        # We reverse the order of the stack so that the next board state
        # to come out of the stack is the oldest state rather than 
        # the most recent.

        while not self.previous_board_states.isEmpty():

            b = self.previous_board_states.pop()
            self.reverse_previous_board_states.push(b)

        replay = Replay()

        # We fill our 'replay' structure with the board states
        # starting from the oldest state to the most recent.

        while not self.reverse_previous_board_states.isEmpty():

            b = self.reverse_previous_board_states.pop()
            replay.enqueue(b)

        print("\nDo you want to review your game ? Press the 'y' key if you do. If not and you want to quit, press any other key.")
        a = input("\nChoice :    ")

        if a == "y":

            # We initialize the board state to be replayed.
            replay.start_replay()

            # The current board state becomes the state
            # to be replayed.

            self.board_state = replay.current.data
            self.print_board()

            while True:

                print("\nPress the 'n' key to see the next move")
                print("\nPress the 'p' key to see the previous move")
                print("\nPress the 'q' key to exit")

                c = input("\nChoice :    ")

                if c == "n":

                    current_replay_node = replay.next()
                    
                    if current_replay_node is None:
                        break

                    else:
                        self.board_state = current_replay_node.data
                        self.print_board()
                        continue

                elif c == "p":

                    current_replay_node = replay.back()
                    
                    if current_replay_node is None:
                        break

                    else:
                        self.board_state = current_replay_node.data
                        self.print_board()
                        continue

                elif c == "q":
                    break

                else:
                    continue


    def playTurn(self):

        if self.player_order == "f":

            self.play_user_move()
            if self.check_game_over():
                return True
            self.play_ai_turn()

        else:
            self.play_ai_turn()

            if self.check_game_over():
                return True

            self.play_user_move()

        if self.check_game_over():
            return True

        return False

    def play_user_move(self):

        board = self.board_state.flatten()
        player_turn_over = False

        while player_turn_over != True:

            inp = input("\nChoose which square you want to play (1-9) or press 'u' to undo your move :        ")

            try:
                i = int(inp) - 1
            except:

                # If we want to undo...

                if inp == "u":

                    self.Undo()
                    self.print_board()
                    board = self.board_state.flatten()
                    continue;

                else:
                    i = 1000

            if i > 8 or i < 0:
                print("\nNon-existent square. Please choose a value between 1 and 9.")

            elif board[i] != " ":
                print("\nThe square is already occupied.")

            else:

                self.previous_board_states.push(self.board_state)

                board[i] = "X"
                self.board_state = np.reshape(board, (3, 3))
                player_turn_over = True
                self.print_board()

    # Find the board state just before the player's last move
    # and mark it as the current state.

    def Undo(self):

        if self.previous_board_states.size() < 2:
            print("\nImpossible to undo this move.")
            return

        else:

            # We must remove two states at the same time.

            # The previous board state whose move was played by
            # the AI is removed.

            self.previous_board_states.pop()

            # Remove the board state that was preceding the previous
            # state whose move was played by the player.

            self.board_state = self.previous_board_states.pop()

    def print_board(self):

        b = self.board_state.flatten()
        board = """
                   |----------|----------|----------|
                   |          |          |          |
                   |   {0}      |    {1}     |    {2}     |
                   |          |          |          |
                   |----------|----------|----------|
                   |          |          |          |
                   |   {3}      |    {4}     |    {5}     |
                   |          |          |          |
                   |----------|----------|----------|
                   |          |          |          |
                   |   {6}      |    {7}     |    {8}     |
                   |          |          |          |
                   |----------|----------|----------|"""

        print(board.format(b[0], b[1], b[2],
                           b[3], b[4], b[5],
                           b[6], b[7], b[8]))

    def play_ai_turn(self):

        board = self.board_state.flatten()
        move = self.ai.play_good_move(board)

        self.previous_board_states.push(self.board_state)

        board[move] = "O"
        self.board_state = np.reshape(board, (3, 3))
        print("\nYour opponent has just played his turn!")
        self.print_board()

    def check_game_over(self):
        to_check = []
        board = np.array(self.board_state)

        to_check.append([np.diagonal(board),np.fliplr(board).diagonal(), board[0], board[1], board[2],
                                                        board.T[0], board.T[1], board.T[2]])

        for col in to_check[0]:
            if col[0] == col[1] and col[1] == col[2] and col[2] != " ":
                print("\nThe " + col[0] + " win the game !")

                self.previous_board_states.push(self.board_state)

                return True

        if np.isin(" ", board) == False:
            print("\nIt's a draw !")

            self.previous_board_states.push(self.board_state)

            return True

        return False



