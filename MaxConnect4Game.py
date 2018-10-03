#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega
# Code has been modified by shahc to make it a functional and optimized game

from copy import copy, deepcopy
import random
import sys

class maxConnect4Game:
    def __init__(self, startGameBoard=None, currentTurn=1):
        self.gameBoard = startGameBoard or [[0 for _column in range(7)] for _row in range(6)]
        self.currentTurn = currentTurn
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        random.seed()

    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        print ' -----------------'
        print ' | 0 1 2 3 4 5 6 | '
        print ' -----------------'
    
    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    def printGameBoardToFileV2(self, filename):
        f = open(filename, 'a+')
        for row in self.gameBoard:
            f.write(''.join(str(col) for col in row) + '\r\n')
        f.write('%s\r\n' % str(self.get_next_player()))
        f.close()


    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1

    # The AI section. Currently plays randomly.
    def aiPlay(self):
        randColumn = random.randrange(0,7)
        result = self.playPiece(randColumn)
        if not result:
            self.aiPlay()
        else:
            self.currentTurn = self.get_next_player()

    def countScore(self):
        """Calculate number of 4-in-a-row each player has and updates the 
        playerScore values in the instance

        """
        self.player1Score = 0
        self.player2Score = 0

        # Check horizontally
        for row in self.gameBoard:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1

    def get_current_board(self):
        return deepcopy(self.gameBoard)

    def get_next_player(self):
        if self.currentTurn == 1:
            return 2
        elif self.currentTurn == 2:
            return 1
    
    def is_board_full(self):
        """Counts pieces in the board that are not 0.
        Then checks if the count is 42 and returns a boolean.
        
        """
        self.checkPieceCount()
        return self.pieceCount == 42
    
    def eval(self, max_player):
        """Heuristic which depending on the max player it will return a positive 
        or negative score
        
        """
        if max_player == 1:
            if self.player1Score > self.player2Score:
                return self.player1Score
            elif self.player1Score < self.player2Score:
                return -1 * self.player2Score
            else:
                return 0
        elif max_player == 2:
            if self.player1Score > self.player2Score:
                return -1 * self.player1Score
            elif self.player1Score < self.player2Score:
                return self.player2Score
            else:
                return 0