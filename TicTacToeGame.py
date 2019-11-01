# Nom : Maximilien Schmitt-Laurin
# Date : 31 octobre 2019

import numpy as np
from AI import AI
from Stack import Stack
from Queue import Replay

class TicTacToeGame:

    def __init__(self):

        # On initie la grille et on met des strings vides pour symboliser aucun move en fait
        self.board_state = np.zeros([3,3], dtype='str')

        self.previous_board_states = Stack()

        self.ai = AI()
        for i in range(len(self.board_state)):
            self.board_state[i] = " "

    def start_new_game(self):
        self.player_order = ""
        while self.player_order != "f" and self.player_order != "s":
            self.player_order = input("Press 'f' to play first or 's' to play second ")

        game_over = False
        self.print_board()
        # Boucle de jeu
        while game_over == False:
            game_over = self.playTurn()

        self.reverse_previous_board_states = Stack()

        # On inverse l'ordre de la pile de sorte que le prochain état
        # de plateau à être 'pop' est l'état le plus ancien plutôt que du 
        # plus récent.

        while not self.previous_board_states.isEmpty():

            b = self.previous_board_states.pop()
            self.reverse_previous_board_states.push(b)

        replay = Replay()

        # On remplie notre structure 'replay' avec les états du plateau
        # partant du plus ancien état au plus récent.

        while not self.reverse_previous_board_states.isEmpty():

            b = self.reverse_previous_board_states.pop()
            replay.enqueue(b)

        print("Désirez-vous revoir votre partie ? Appuyez sur la touche 'y' si oui. Si ce n'est pas le cas et vous voulez quitter, appuyez sur n'importe quelle autre touche.")
        a = input("Choix :    ")

        if a == "y":

            # On initialise l'état courant du plateau à rejouer.
            replay.start_replay()

            # L'état courant du plateau à rejouer devient l'état actuel du
            # plateau.

            self.board_state = replay.current.data
            self.print_board()

            while True:

                print("Appuyez sur la touche 'n' pour voir le prochain coup")
                print("Appuyez sur la touche 'p' pour voir le coup précédent")
                print("Appuyez sur la touche 'q' pour quitter")

                c = input("Choix :    ")

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

            inp = input("Entrez la case que vous vouler jouer ou appuyez sur 'u' pour effacer votre coup joué :    ")

            try:
                i = int(inp) - 1
            except:

                # Si on veut 'undo'...

                if inp == "u":

                    self.Undo()
                    self.print_board()
                    board = self.board_state.flatten()
                    continue;

                else:
                    i = 1000

            if i > 8 or i < 0:
                print("Case inexistante. Prenez une valeur entre 0 et 9.")

            elif board[i] != " ":
                print("Case déjà occupée")

            else:

                self.previous_board_states.push(self.board_state)

                board[i] = "X"
                self.board_state = np.reshape(board, (3, 3))
                player_turn_over = True
                self.print_board()

    # Retrouve l’état du plateau juste avant le dernier coup du joueur
    # et le met comme ́etat courant du plateau.

    def Undo(self):

        if self.previous_board_states.size() < 2:
            print("Impossible d'effacer le dernier coup joué")
            return

        else:

            # On doit revenir deux états en arrière de la partie.

            # On enlève l'état précédent du plateau dont le coup a
            # été joué par l'AI.

            self.previous_board_states.pop()

            # On enlève l'état du plateau qui précède l'état précédent
            # dont le coup a été joué par le jour.

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
        self.print_board()

    def check_game_over(self):
        to_check = []
        board = np.array(self.board_state)

        to_check.append([np.diagonal(board),np.fliplr(board).diagonal(), board[0], board[1], board[2],
                                                        board.T[0], board.T[1], board.T[2]])

        for col in to_check[0]:
            if col[0] == col[1] and col[1] == col[2] and col[2] != " ":
                print("Les " + col[0] + " remportent la partie !")

                self.previous_board_states.push(self.board_state)

                return True

        if np.isin(" ", board) == False:
            print("Partie nulle !")

            self.previous_board_states.push(self.board_state)

            return True

        return False



