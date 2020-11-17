#Tic-Tac-Toe Game
#Complete game functions

import random, sys, time, math, pygame
from pygame.locals import *
import numpy as np
import copy

#define window
FPS = 30
WINDOW_WIDTH = 340
WINDOW_HEIGHT = 480
TOP_MARGIN = 160
MARGIN = 20
GAMEBOARD_SIZE = 3
WIN_MARK = 3
GRID_SIZE = WINDOW_WIDTH - 2 * (MARGIN)

HALF_WINDOW_WIDTH = int(WINDOW_WIDTH / 2)
HALF_WINDOW_HEIGHT = int(WINDOW_HEIGHT / 2)

##set colors
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
RED          = (200,  72,  72)
LIGHT_ORANGE = (198, 108,  58)
ORANGE       = (180, 122,  48)
GREEN        = ( 72, 160,  72)
BLUE         = ( 66,  72, 200)
YELLOW       = (162, 162,  42)
NAVY         = ( 75,   0, 130)
PURPLE       = (143,   0, 255)
BADUK        = (220, 179,  92)

def ReturnName():
    return 'tictactoe'


def Return_Num_Action():
    return GAMEBOARD_SIZE * GAMEBOARD_SIZE


def Return_BoardParams():
    return GAMEBOARD_SIZE, WIN_MARK

class GameState:
    def __init__(self):
        global FPS_CLOCK, DISPLAYSURF, BASIC_FONT, TITLE_FONT, GAMEOVER_FONT

        pygame.init()
        FPS_CLOCK = pygame.time.Clock()

        DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption('TicTacToe')

        BASIC_FONT = pygame.font.Font('freesansbold.ttf', 16)
        TITLE_FONT = pygame.font.Font('freesansbold.ttf', 24)
        GAMEOVER_FONT = pygame.font.Font('freesansbold.ttf', 48)

        # Set initial parameters
        self.init = False
        self.num_mark = 0

        # No stone: 0, Black stone: 1, White stone = -1
        self.gameboard = np.zeros([GAMEBOARD_SIZE, GAMEBOARD_SIZE])

        self.x_win = 0
        self.o_win = 0
        self.count_draw = 0

        # black turn: 0, white turn: 1
        self.turn = 0

        # black wins: 1, white wins: 2, draw: 3, playing: 0
        self.win_index = 0

        # List of X coordinates and Y coordinates
        self.X_coord = []
        self.Y_coord = []

        for i in range(GAMEBOARD_SIZE):
            self.X_coord.append(
                MARGIN + i * int(GRID_SIZE / (GAMEBOARD_SIZE)) + int(
                    GRID_SIZE / (GAMEBOARD_SIZE * 2)))
            self.Y_coord.append(
                TOP_MARGIN + i * int(GRID_SIZE / (GAMEBOARD_SIZE)) + int(
                    GRID_SIZE / (GAMEBOARD_SIZE * 2)))

    def step(self):
        pass
    
    def terminate(self):
         pygame.quit()
         sys.exit()

    def draw_main_board(self):
        pass

    def title_msg(self):
        pass

    def rule_msg(self):
        ruleSurf1 = BASIC_FONT.render('Win: O or X mark has to be 3 in a row',
                                      True, WHITE)
        ruleRect1 = ruleSurf1.get_rect()
        ruleRect1.topleft = (MARGIN, 50)
        DISPLAYSURF.blit(ruleSurf1, ruleRect1)

        ruleSurf2 = BASIC_FONT.render('(horizontal, vertical, diagonal)', True,
                                      WHITE)
        ruleRect2 = ruleSurf1.get_rect()
        ruleRect2.topleft = (MARGIN, 70)
        DISPLAYSURF.blit(ruleSurf2, ruleRect2)

    def score_msg(self):
        scoreSurf1 = BASIC_FONT.render('Score: ', True, WHITE)
        scoreRect1 = scoreSurf1.get_rect()
        scoreRect1.topleft = (MARGIN, 105)
        DISPLAYSURF.blit(scoreSurf1, scoreRect1)

        scoreSurf2 = BASIC_FONT.render('O = ' + str(self.o_win) + '  vs  ',
                                       True, WHITE)
        scoreRect2 = scoreSurf2.get_rect()
        scoreRect2.topleft = (scoreRect1.midright[0], 105)
        DISPLAYSURF.blit(scoreSurf2, scoreRect2)

        scoreSurf3 = BASIC_FONT.render('X = ' + str(self.x_win) + '  vs  ',
                                       True, WHITE)
        scoreRect3 = scoreSurf3.get_rect()
        scoreRect3.topleft = (scoreRect2.midright[0], 105)
        DISPLAYSURF.blit(scoreSurf3, scoreRect3)

        scoreSurf4 = BASIC_FONT.render('Draw = ' + str(self.count_draw), True,
                                       WHITE)
        scoreRect4 = scoreSurf4.get_rect()
        scoreRect4.topleft = (scoreRect3.midright[0], 105)
        DISPLAYSURF.blit(scoreSurf4, scoreRect4)

    def turn_msg(self):
        if self.turn == 0:
            turnSurf = BASIC_FONT.render("O's Turn!", True, WHITE)
            turnRect = turnSurf.get_rect()
            turnRect.topleft = (MARGIN, 135)
            DISPLAYSURF.blit(turnSurf, turnRect)
        else:
            turnSurf = BASIC_FONT.render("X's Turn!", True, WHITE)
            turnRect = turnSurf.get_rect()
            turnRect.topleft = (WINDOW_WIDTH - 75, 135)
            DISPLAYSURF.blit(turnSurf, turnRect)


    def check_win(self):
        # Check four stones in a row (Horizontal)
        for row in range(GAMEBOARD_SIZE):
            for col in range(GAMEBOARD_SIZE - WIN_MARK + 1):
                # Black win!
                if np.sum(self.gameboard[row, col:col + WIN_MARK]) == WIN_MARK:
                    return 1
                # White win!
                if np.sum(self.gameboard[row, col:col + WIN_MARK]) == -WIN_MARK:
                    return 2

        # Check four stones in a colum (Vertical)
        for row in range(GAMEBOARD_SIZE - WIN_MARK + 1):
            for col in range(GAMEBOARD_SIZE):
                # Black win!
                if np.sum(self.gameboard[row: row + WIN_MARK, col]) == WIN_MARK:
                    return 1
                # White win!
                if np.sum(
                        self.gameboard[row: row + WIN_MARK, col]) == -WIN_MARK:
                    return 2

        # Check four stones in diagonal (Diagonal)
        for row in range(GAMEBOARD_SIZE - WIN_MARK + 1):
            for col in range(GAMEBOARD_SIZE - WIN_MARK + 1):
                count_sum = 0
                for i in range(WIN_MARK):
                    if self.gameboard[row + i, col + i] == 1:
                        count_sum += 1
                    if self.gameboard[row + i, col + i] == -1:
                        count_sum -= 1

                # Black Win!
                if count_sum == WIN_MARK:
                    return 1

                # White WIN!
                if count_sum == -WIN_MARK:
                    return 2

        for row in range(WIN_MARK - 1, GAMEBOARD_SIZE):
            for col in range(GAMEBOARD_SIZE - WIN_MARK + 1):
                count_sum = 0
                for i in range(WIN_MARK):
                    if self.gameboard[row - i, col + i] == 1:
                        count_sum += 1
                    if self.gameboard[row - i, col + i] == -1:
                        count_sum -= 1

                # Black Win!
                if count_sum == WIN_MARK:
                    return 1

                # White WIN!
                if count_sum == -WIN_MARK:
                    return 2

        # Draw (board is full)
        if self.num_mark == GAMEBOARD_SIZE * GAMEBOARD_SIZE:
            return 3

        return 0

    def display_win(self, win_index):
        pass


if __name__ == "__main__":
    main()