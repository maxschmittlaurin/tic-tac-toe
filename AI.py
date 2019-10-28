import numpy as np
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
        pass
        # À implémenter