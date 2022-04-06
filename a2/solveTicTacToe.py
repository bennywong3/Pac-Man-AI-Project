#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        """ 
                    [  0  ,   1  ,  2  ,   3  ,   4  ,   5  ,   6  ,   7  ,   8  ]
        """
        self.p1 =  [[True, False, False, False, False, False, False, False, False],
                    [False, True, False, False, False, False, False, False, False],
                    [True, False, False, False, False, True, False, True, False]]

        self.pa =  [[True, False, False, False, False, False, False, False, True], 
                    [False, True, False, True, False, False, False, False, False], 
                    [False, True, False, False, False, False, False, True, False], 
                    [True, True, False, False, False, False, True, False, False], 
                    [True, False, True, False, True, False, False, False, False], 
                    [True, False, True, False, False, False, False, True, False], 
                    [True, False, False, False, True, True, False, False, False], 
                    [True, True, False, True, True, False, False, False, False], 
                    [True, True, False, True, False, True, False, False, False], 
                    [True, True, False, True, False, False, False, False, True], 
                    [True, True, False, False, False, False, False, True, True], 
                    [True, False, True, False, False, False, True, False, True], 
                    [False, True, False, True, False, True, False, True, False], 
                    [True, True, False, False, True, True, True, False, False], 
                    [True, True, False, False, False, True, True, True, False], 
                    [True, True, False, False, False, True, True, False, True], 
                    [True, True, False, True, False, True, False, True, True]]
        self.pb =  [[True, False, True, False, False, False, False, False, False], 
                    [True, False, False, False, True, False, False, False, False], 
                    [True, False, False, False, False, True, False, False, False], 
                    [False, True, False, False, True, False, False, False, False], 
                    [True, True, False, True, False, False, False, False, False], 
                    [False, True, False, True, False, True, False, False, False], 
                    [True, True, False, False, True, True, False, False, False], 
                    [True, True, False, False, True, False, True, False, False], 
                    [True, True, False, False, False, True, True, False, False], 
                    [True, True, False, False, False, False, True, True, False], 
                    [True, True, False, False, False, False, True, False, True], 
                    [True, False, True, False, True, False, False, True, False], 
                    [True, False, False, False, True, True, False, True, False], 
                    [True, True, False, True, False, True, False, True, False], 
                    [True, True, False, True, False, True, False, False, True]]
        self.pc =  [[False, False, False, False, False, False, False, False, False]]
        self.pd =  [[True, True, False, False, False, True, False, False, False], 
                    [True, True, False, False, False, False, False, True, False], 
                    [True, True, False, False, False, False, False, False, True]]
        self.pab = [[True, True, False, False, True, False, False, False, False], 
                    [True, False, True, False, False, False, True, False, False], 
                    [False, True, False, True, True, False, False, False, False], 
                    [True, True, False, False, False, True, False, True, False], 
                    [True, True, False, False, False, True, False, False, True]]
        self.pad = [[True, True, False, False, False, False, False, False, False]]
        self.pcc = [[False, False, False, False, True, False, False, False, False]]

        self.allpattern = self.p1 + self.pa + self.pb + self.pc + self.pd + self.pab +self.pad + self.pcc
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])


    #helper functions

    def rotation(self, board):
        """
            0 1 2       6 3 0
            3 4 5  to   7 4 1
            6 7 8       8 5 2
        """
        totalboard = [] #all four rotations 0, 90, 180, 270
        totalboard.append(board)
        rotated = board.copy()
        for i in range(3):
            temp = board.copy()
            temp[0] = rotated[6]
            temp[1] = rotated[3]
            temp[2] = rotated[0]
            temp[3] = rotated[7]
            temp[4] = rotated[4]
            temp[5] = rotated[1]
            temp[6] = rotated[8]
            temp[7] = rotated[5]
            temp[8] = rotated[2]
            rotated = temp.copy()
            totalboard.append(rotated)
        return totalboard

    def reflection(self, board):
        totalboard = []

        reflect1 = board.copy() #horizontal reflection using y axis
        reflect1[0] = board[2]
        reflect1[2] = board[0]
        reflect1[3] = board[5]
        reflect1[5] = board[3]
        reflect1[6] = board[8]
        reflect1[8] = board[6]
        totalboard.append(reflect1)

        reflect2 = board.copy() #vertical reflection using x axis
        reflect2[0] = board[6]
        reflect2[6] = board[0]
        reflect2[1] = board[7]
        reflect2[7] = board[1]
        reflect2[2] = board[8]
        reflect2[8] = board[2]
        totalboard.append(reflect2)

        reflect3 = board.copy() #diagonal reflection using 0 4 8
        reflect3[1] = board[3]
        reflect3[3] = board[1]
        reflect3[2] = board[6]
        reflect3[6] = board[2]
        reflect3[5] = board[7]
        reflect3[7] = board[5]
        totalboard.append(reflect3)

        reflect4 = board.copy() #diagonal reflection using 2 4 6
        reflect4[1] = board[5]
        reflect4[5] = board[1]
        reflect4[0] = board[8]
        reflect4[8] = board[0]
        reflect4[3] = board[7]
        reflect4[7] = board[3]
        totalboard.append(reflect4)

        return totalboard

    def nonisomorphicways(self, board):
        totalboard = self.rotation(board)
        for reflect in self.reflection(board): #get rid of duplicated board in reflect & rotate
            if reflect not in totalboard: totalboard.append(reflect)
        return totalboard

    def fingerprint(self, board):
        if self.deadTest(board) == True: 
            return '1'
        
        boardwithin102 = []
        for b in self.nonisomorphicways(board):
            if b in self.allpattern: boardwithin102 = b
        if boardwithin102 in self.p1: return '1'
        elif boardwithin102 in self.pa: return 'a'
        elif boardwithin102 in self.pb: return 'b'
        elif boardwithin102 in self.pc: return 'c'
        elif boardwithin102 in self.pd: return 'd'
        elif boardwithin102 in self.pab: return 'ab'
        elif boardwithin102 in self.pad: return 'ad'
        elif boardwithin102 in self.pcc: return 'cc'
        else: return '1' #should not happen

    def result(self, boards):
        ans=''
        fplist=[] #char array storing all 3 fingerprints
        for i in range(3):
            fplist.append(self.fingerprint(boards[i]))
        for fp in fplist:
            if fp != '1':
                ans+=fp
        return ans

        




class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        self.wincon = ['cc', 'a', 'bb', 'bc', 'cb']

    def getAction(self, gameState, gameRules):
        optimal = []
        actions = gameState.getLegalActions(gameRules)
        for a in actions:
            successor = gameState.generateSuccessor(a)
            susresult = gameRules.result(successor.boards)
            if susresult in self.wincon:
                optimal.append(a)
        if len(optimal) == 0: optimal.append(random.choice(actions)) #if no optimal move (shd not happen)
        return random.choice(optimal)


class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
