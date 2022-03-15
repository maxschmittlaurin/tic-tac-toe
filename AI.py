# Author : Maximilien Schmitt-Laurin
# Date : 31 octobre 2019

import numpy as np
import operator
import copy

class AI:

    def __init__(self):
        pass

    # Basic function of the AI, making random moves.
    # Almost never wins.
	
    def play_at_random(self, board):

        free_index = np.where(board == " ")
        move = np.random.choice(free_index[0])

        return move

    def play_good_move(self, board):

    	# The minimax algorithm and the creation of the tree of possible moves
    	# take more time when the board state is empty and it is the turn
    	# of the IA to play. We therefore give a default move in a corner of the
    	# board that we know is certainly optimal as the player has not yet
    	# played.

    	if self.check_is_empty_board(board):
    		best_move = 8

    	else:

    		possible_moves_tree = self.create_possible_moves_tree(board)

    		# We obtain the node that represents the best possible move
    		# contained in a tuple (node of the best possible move, minimax value)
    		# returned by the minimax function.

    		best_move_node = self.minimax(possible_moves_tree.get_root(), True)[0]

    		# We obtain the position of the square that corresponds to the best possible
			# move contained in a tuple
			# (state of the board, state of the game, position of the played square)
			# assigned to the 'data' attribute of the 'Node' instance.

    		best_move = best_move_node.get_data()[2]

    	return best_move

    # Returns a tree whose root is the current board state and the 
    # children of each node are the possible ́board states after a 
    # certain move played. A leaf in this tree means that the game
	# is finished.

    def create_possible_moves_tree(self, board):

    	# The nodes of the tree will store tuples
    	# (state of the board, state of the game, position of the played square)
    	# where "state of the game" is 1 if the AI won, -1 if the player won,
    	# 0 if the game is a draw and None if the game is not finished.

        root = Node((board, None, None))
        possible_moves_tree = Tree(root)
        self.find_next_possible_moves(possible_moves_tree.get_root(), True)

        return possible_moves_tree

    # Returns a tuple (node representing the best possible move to play, its
    # minimax value) according to a node that represents the current board 
    # state and whether it is the AI's turn or not.

    def minimax(self, node, ai_turn):

    	# If the node is a leaf, we return in a tuple the board state
    	# associated to this node and its minimax value.

    	if node.is_leaf():
    		return (node, node.get_data()[1])

    	# List of tuples (node representing a possible move, its minimax 
    	# value) that will be used to choose the best move among all 
    	# possible moves.

    	possible_moves = []

    	for child in node.children:
    		possible_moves.append((child, self.minimax(child, not ai_turn)[1]))

    	# We sort the list in ascending order according to the minimax 
    	# values of the moves (stored at the second position of each tuple).

    	possible_moves.sort(key = operator.itemgetter(1))

    	# If it is the AI's turn to play, the best possible move to play is the
    	# one with the highest minimax value.

    	if ai_turn:
    		return possible_moves[-1]

    	# If it is the player's turn to play, the best possible move to play is
    	# the one with the lowest minimax value.

    	else :
    		return possible_moves[0]

    # Determines the next possible moves according to a state of the board
	# (contained in a node).

    def find_next_possible_moves(self, node, ai_turn):

        board_state = node.get_data()[0]

        # We pass each square of the board in iteration...

        for i in range(len(board_state)):

        	# If a square is empty, a move could take place in that square
			# on the next turn.

            if board_state[i] == " ":

                possible_move_board_state = copy.deepcopy(board_state)

                if ai_turn:
                    possible_move_board_state[i] = "O"

                else:
                    possible_move_board_state[i] = "X"


                # If we get a draw with this next possible move, we indicate it
                # in the child node.

                if self.check_draw(possible_move_board_state):

                	child = Node((possible_move_board_state, 0, i))
                	node.add_child(child)

                # If the AI wins with this next possible move, it is indicated in the 
                # child node.

                elif self.check_victory(possible_move_board_state, "O"):

                	child = Node((possible_move_board_state, 1, i))
                	node.add_child(child)

                # If the player wins with this next possible move, it is indicated in the 
                # child node.

                elif self.check_victory(possible_move_board_state, "X"):

                	child = Node((possible_move_board_state, -1, i))
                	node.add_child(child)

                # Otherwise we only check the possible moves that can follow
                # this next possible move.

                else:
                	child = Node((possible_move_board_state, None, i))
                	node.add_child(child)
                	self.find_next_possible_moves(child, not ai_turn)

    # Determines if there is a victory on the board according to the symbol used.

    def check_victory(self, board, symbol):

    	# Chech if we have a victory on the first diagonal...
    	if board[0] == board[4] == board[8] == symbol:
    		return True

    	# Chech if we have a victory on the second diagonal...
    	if board[2] == board[4] == board[6] == symbol:
    		return True

    	for i in range(0, 3):

    		# Chech if you have a victory on a horizontal line of the board...
    		if board[i*3] == board[i*3+1] == board[i*3+2] == symbol:
    			return True

    		# Chech if you have a victory on a vertical line of the board...
    		if board[i] == board[i+3] == board[i+6] == symbol:
    			return True

    	return False

    # Determines if there is a draw on the board.

    def check_draw(self, board):

    	empty_case_exists = False

    	for i in range(len(board)):

    		if board[i] == " ":
    			empty_case_exists = True
    			break

    	return (not empty_case_exists and 
    	        not self.check_victory(board, "O") and 
    	        not self.check_victory(board, "X"))

    # Determines if the board is empty.

    def check_is_empty_board(self, board):

    	is_empty = True

    	for i in range(len(board)):

    		if board[i] != " ":
    			is_empty = False

    	return is_empty

class Tree:

    def __init__(self, root):
        self.root = root

    def get_root(self):
        return self.root

class Node:

    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def get_data(self):
        return self.data

    def get_children(self):
        return self.children

    def is_leaf(self):
        return len(self.children) == 0
