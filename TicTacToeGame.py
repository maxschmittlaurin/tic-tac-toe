import numpy as np
from AI import AI
class TicTacToeGame:

    def __init__(self):

        # On initie la grille et on met des strings vides pour symboliser aucun move en fait
        self.board_state = np.zeros([3,3], dtype='str')
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
            try:
                i = int(input("Entree la case que vous voulez jouer:    ")) - 1
            except:
                i = 1000

            if i > 8 or i < 0:
                print("Case inexistante. Prenez une valeure entre 0 et 9.")

            elif board[i] != " ":
                print("Case déja occupee")

            else:
                board[i] = "X"
                self.board_state = np.reshape(board, (3, 3))
                player_turn_over = True
                self.print_board()



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
        move = self.ai.play_at_random(board)

        board[move] = "O"
        self.board_state = np.reshape(board, (3, 3))
        self.print_board()

    def check_game_over(self):
        to_check = []
        board = np.array(self.board_state)

        to_check.append([np.diagonal(board),np.diagonal(board.transpose()), board[0], board[1], board[2],
                                                        board.T[0], board.T[1], board.T[2]])

        for col in to_check[0]:
            if col[0] == col[1] and col[1] == col[2] and col[2] != " ":
                print("Les " + col[0] + " remportent la partie !")
                return True

        if np.isin(" ", board) == False:
            print("Partie nulle !")
            return True

        return False



