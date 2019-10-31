# Nom : Maximilien Schmitt-Laurin
# Date : 31 octobre 2019

import numpy as np
import operator
import copy

class AI:

    def __init__(self):
        pass

    # Fonction de base de l'AI, faire des moves au hasard.
    # Ne gagne pratiquement jamais.
    def play_at_random(self, board):

        free_index = np.where(board == " ")
        move = np.random.choice(free_index[0])

        return move

    # Votre fonction pour l'AI, qui doit ne jamais perdre ! Pour les détails, voir la
    # description du TP .
    def play_good_move(self, board):

    	if self.check_is_empty_board(board):
    		best_move = 8

    	else:

    		possible_moves_tree = self.create_possible_moves_tree(board)

    		# On obtient le noeud qui représente le meilleur coup possible.

    		best_move_node = self.minimax(possible_moves_tree.get_root(), True)[0]

    		# On obtient la position de la case qui correspond au meilleur
			# coup possible.

    		best_move = best_move_node.get_data()[2]

    	return best_move

    # Retourne un arbre dont la racine est l’état courant du plateau et chaque
    # enfant de la racine est un des ́états du plateau possible après un coup
    # et ainsi de suite, jusqu’à atteindre une feuille, qui correspond à une fin
    # de partie.

    def create_possible_moves_tree(self, board):

    	# Les noeuds de l'arbre vont stocker des tuples
    	# (état du plateau, état de la partie, position de la case jouée)
    	# où "état de la partie" vaut 1 si l'AI a gagné, -1 si c'est le 
    	# joueur qui a gagné, 0 si la partie est nulle et None si la 
    	# partie n'est pas terminée.

        root = Node((board, None, None))
        possible_moves_tree = Tree(root)
        self.find_next_possible_moves(possible_moves_tree.get_root(), True)

        return possible_moves_tree

    # 

    def minimax(self, node, ai_turn):

    	# Si le noeud est une feuille, on retourne dans un tuple le
    	# noeud et la valeur minimax du coup.

    	if node.is_leaf():
    		return (node, node.get_data()[1])
    		#return (node, node.get_data()[1])

    	# List des prochains coups possibles représentés sous formes
    	# de tuples (noeud contenant les infos du coup, valeur minimax du coup)

    	possible_moves = []

    	for child in node.children:
    		possible_moves.append((child, self.minimax(child, not ai_turn)[1]))
    		#possible_moves.append(self.minimax(child, not ai_turn))

    	# On trie la List des coups possibles (représentés par des tuples)
    	# en ordre croissant selon les valeurs minimax des coups (stockées
    	# à la deuxième position de chaque tuple).

    	possible_moves.sort(key = operator.itemgetter(1))

    	# Si le noeud simule le coup de l'AI, le meilleur coup est celui
    	# qui a la plus grande valeur parmis celles retournées par les
    	# enfants.

    	if ai_turn:
    		return possible_moves[-1]
    		#return possible_moves[-1]

    	# Si le noeud simule le coup du joueur, le meilleur coup est celui
    	# qui a la plus petite valeur parmis celles retournées par les
    	# enfants.

    	else :
    		return possible_moves[0]
    		#return possible_moves[0]

    # Détermine les prochains coups possibles selon un état du plateau
    # (contenu dans un noeud).

    def find_next_possible_moves(self, node, ai_turn):

        board_state = node.get_data()[0]

        # On passe chaque case du plateau en itération...

        for i in range(len(board_state)):

        	# Si une case est vide, un coup pourrait avoir lieu dans
        	# cette case au prochain tour.

            if board_state[i] == " ":

                possible_move_board_state = copy.deepcopy(board_state)

                if ai_turn:
                    possible_move_board_state[i] = "O"

                else:
                    possible_move_board_state[i] = "X"


                # Si on obtient une partie nulle avec ce prochain coup
                # possible, on l'indique dans le noeud enfant.

                if self.check_draw(possible_move_board_state):

                	child = Node((possible_move_board_state, 0, i))
                	node.add_child(child)

                # Si l'AI gagne avec ce prochain coup possible, on
                # l'indique dans le noeud enfant.

                elif self.check_victory(possible_move_board_state, "O"):

                	child = Node((possible_move_board_state, 1, i))
                	node.add_child(child)

                # Si le joueur gagne avec ce prochain coup possible,
                # on l'indique dans le noeud enfant.

                elif self.check_victory(possible_move_board_state, "X"):

                	child = Node((possible_move_board_state, -1, i))
                	node.add_child(child)

                # Sinon on vérifie seulement les coups possibles qui
                # peuvent suivre ce prochain coup possible.

                else:
                	child = Node((possible_move_board_state, None, i))
                	node.add_child(child)
                	self.find_next_possible_moves(child, not ai_turn)

    # Détermine si on a une victoire sur le plateau selon le symbole
    # utilisé.

    def check_victory(self, board, symbol):

    	# Si on a une victoire sur la première diagonale...
    	if board[0] == board[4] == board[8] == symbol:
    		return True

    	# Si on a une victoire sur la deuxième diagonale...
    	if board[2] == board[4] == board[6] == symbol:
    		return True

    	for i in range(0, 3):

    		# Si on a une victoire sur une ligne horizontale du plateau...
    		if board[i*3] == board[i*3+1] == board[i*3+2] == symbol:
    			return True

    		# Si on a une victoire sur une ligne verticale du plateau...
    		if board[i] == board[i+3] == board[i+6] == symbol:
    			return True

    	return False

    # Détermine si on a une partie nulle sur le plateau.

    def check_draw(self, board):

    	empty_case_exists = False

    	for i in range(len(board)):

    		if board[i] == " ":
    			empty_case_exists = True
    			break

    	return (not empty_case_exists and 
    	        not self.check_victory(board, "O") and 
    	        not self.check_victory(board, "X"))

    # Détermine si le plateau est vide.

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
