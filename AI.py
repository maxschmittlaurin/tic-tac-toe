import numpy as np
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
        
        possible_moves_tree = create_possible_moves_tree(board)

    # Retourne un arbre dont la racine est l’état courant du plateau et chaque
    # enfant de la racine est un des ́états du plateau possible après un coup
    # et ainsi de suite, jusqu’à atteindre une feuille, qui correspond à une fin
    # de partie.

    def create_possible_moves_tree(board):

        root = Node(board)
        possible_moves_tree = Tree(root)
        find_next_possible_moves(possible_moves_tree.get_root(), True)

        return possible_moves_tree


    # Détermine les prochains coups possibles selon un état du plateau
    # (contenu dans un noeud).

    def find_next_possible_moves(node, turn_ai):

        board_state = node.get_data()

        for i in range(len(board_state)):

            if board_state[i] == " ":

                possible_move = copy.deepcopy(board_state)

                if turn_ai:
                    possible_move[i] = "O"

                else:
                    possible_move[i] = "X"

                child = Node(possible_move)
                node.add_child(child)

                # if partie non termine...
                find_next_possible_moves(child, not turn_ai)


class Tree:

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

    def __init__(self, root):
        self.root = root

    def get_root(self):
        return self.root
