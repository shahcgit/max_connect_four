#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Written to be Python 2.4 compatible for omega
# Code has been modified by shahc to make it a functional and optimized game

import sys
from MaxConnect4Game import maxConnect4Game
# from minmax import min_max_decision
from minmax_alphabeta import alpha_beta_decision
from copy import deepcopy

def oneMoveGame(currentGame, depth_limit, output_filename):
    """This mode is used to make two AIs play against each other
    
    """

    currentGame.gameFile.close()

    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)

    actual_turn = deepcopy(currentGame.currentTurn)

    # Switching turns between max player and min player
    if actual_turn==1:
         currentGame.currentTurn = 2
    else:
        currentGame.currentTurn = 1
    
    # This will execute the alpha beta code
    decisions = alpha_beta_decision(currentGame, depth_limit=deepcopy(depth_limit), max_player=1)
    decision_val = -999999
    decision_col = 0

    # Choosing the max decision to play
    for d in decisions:
        if d['val'] > decision_val:
            decision_val = d['val']
            decision_col = d['column']
    
    currentGame.currentTurn = actual_turn
    currentGame.playPiece(decision_col)

    print 'Game state after move:'
    currentGame.printGameBoard()

    currentGame.countScore()
    print 'Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score)
    currentGame.printGameBoardToFileV2(output_filename)


def interactiveGame(currentGame, player, depth_limit):
    """This mode is used to play Human vs AI
    
    """
    HUMAN_FILE = 'human.txt'
    COMPUTER_FILE = 'computer.txt'
    currentGame.gameFile.close()

    if currentGame.pieceCount == 42:    # Is the board full already?
        print 'BOARD FULL\n\nGame Over!\n'
        sys.exit(0)

    print 'Game state at start!'

    currentGame.printGameBoard()

    currentGame.countScore()
    print 'Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score)

    # If human first then take human input and play it if valid
    if player == 'human-next':
        currentGame.currentTurn = 2
        
        user_input = None
        while True:
            user_input = raw_input('Enter column number[0-6]: ')
            if int(user_input) in range(0,7):
                break
            else:
                print 'Enter a valid column from 0 to 6'
            if currentGame.playPiece(int(user_input)):
                break
            else:
                print 'This column is full. Choose another column'
        currentGame.countScore()

        print 'HUMAN played:\n'
        currentGame.printGameBoard()
        currentGame.printGameBoardToFileV2(HUMAN_FILE)


        print 'Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score)
    
    # Then play the game for computer and human till the board is full
    while not currentGame.is_board_full():
        currentGame.currentTurn = 2
        decisions = alpha_beta_decision(currentGame, depth_limit=deepcopy(depth_limit), max_player=1)
        decision_val = -999999
        decision_col = 0
        for d in decisions:
            if d['val'] > decision_val:
                decision_val = d['val']
                decision_col = d['column']
        
        currentGame.currentTurn = 1
        currentGame.playPiece(decision_col)
        currentGame.countScore()

        print 'AI played:\n'
        currentGame.printGameBoard()
        currentGame.printGameBoardToFileV2(COMPUTER_FILE)

        print 'Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score)

        if currentGame.is_board_full():
            break

        user_input = None
        currentGame.currentTurn = 2
        
        while True:
            user_input = raw_input('Enter column number[0-6]: ')
            if int(user_input) in range(0,7):
                break
            else:
                print('Enter a valid column from 0 to 6')
            
            if currentGame.playPiece(int(user_input)):
                break
            else:
                print 'This column is full. Choose another column'
        currentGame.countScore()

        print 'Updated Game Board\n'
        currentGame.printGameBoard()
        currentGame.printGameBoardToFileV2(HUMAN_FILE)

        print 'Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score)

        if currentGame.is_board_full():
            break

    
    print 'BOARD FULL\n\nGame Over!\n'
    sys.exit(0)


def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print 'Four command-line arguments are needed:'
        print 'Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0]
        print 'or: %s one-move [input_file] [output_file] [depth]' % argv[0]
        sys.exit(2)

    # Get the Game mode(Interactive/One move) and the input file to read game state.
    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print '%s is an unrecognized game mode' % game_mode
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a blank game

    
    if game_mode == 'interactive':

        # Try to open the input file
        try:
            currentGame.gameFile = open(inFile, 'r')
            # Read the initial game state from the file and save in a 2D list
            file_lines = currentGame.gameFile.readlines()

            # Update the blank game with the values from the file
            currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
            currentGame.currentTurn = int(file_lines[-1][0])
            currentGame.gameFile.close()
        except:
            pass

        

        print '\nMaxConnect-4 game\n'
        print 'Game state before move:'
        currentGame.printGameBoard()

        # Update a few game variables based on initial state and print the score
        currentGame.checkPieceCount()
        currentGame.countScore()
        print 'Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score)

        interactiveGame(currentGame, player=argv[3], depth_limit=int(argv[4])) # Be sure to pass whatever else you need from the command line
    else: # game_mode will be 'one-move'
        # Try to open the input file
        try:
            currentGame.gameFile = open(inFile, 'r')
        except IOError:
            sys.exit("\nError opening input file.\nCheck file name.\n")

        # Read the initial game state from the file and save in a 2D list
        file_lines = currentGame.gameFile.readlines()

        # Update the blank game with the values from the file
        currentGame.gameBoard = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
        currentGame.currentTurn = int(file_lines[-1][0])
        currentGame.gameFile.close()

        print '\nMaxConnect-4 game\n'
        print 'Game state before move:'
        currentGame.printGameBoard()

        # Update a few game variables based on initial state and print the score
        currentGame.checkPieceCount()
        currentGame.countScore()
        print 'Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score)

        # Set up the output file
        outFile = argv[3]
        oneMoveGame(currentGame, depth_limit=int(argv[4]), output_filename=outFile) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)



