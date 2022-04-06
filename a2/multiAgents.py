from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #print("prevFood",prevFood) #Grid
        #print("successorGameState",successorGameState)
        #print("newPos",newPos)
        #print("newFood",newFood) #Grid
        #print("newGhostStates",*newGhostStates) #Ghost attr
        #print(len(newGhostStates)) #ghost num
        #print("newScaredTimes",newScaredTimes)
        # successorGameState.getScore() time pass  -1, eat food +10, win +500, lose -500, hunted ghost +200

        #Problem: manhattanDistance ignore walls, if there is wall between pellet and pacman, pacman wont move to eat as moving increases distance 
        base_score=1000
        foodxy = newFood.asList()
        ghostnum = len(newGhostStates)
        foodnum = len(foodxy)
        mindis = 9999
        if foodnum==0:
          mindis = 0
        for i in range(foodnum):
          dis=manhattanDistance(newPos,foodxy[i])
          if dis < mindis:
            mindis=dis
        # print("mindis",mindis)
        # print("foodnum",foodnum)
        base_score-=mindis
        base_score-=(foodnum*100) #encourage eating, assume after eating closest food, the next closest food is within distance 100, so it is worth eating
        
        # caplist = successorGameState.getCapsules()
        # for cap in caplist:
        #   if newPos==cap: base_score+=1000
        minsc=9999
        for scare in newScaredTimes:
            if scare <minsc: minsc=scare
        #print(scare)
        if not (scare>2):
          for i in range(1,ghostnum+1):
            ghostxy = successorGameState.getGhostPosition(i)
            if manhattanDistance(newPos,ghostxy)<2 : base_score-=9999
 
        # print("base",base_score)
        return base_score
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #depth 1 with 3 agent= max(L0) min(L1) min(L2) terminal(L3)
        anum=gameState.getNumAgents()
        lowest=self.depth*anum #terminal layer
        layer=0 #start at first layer max


        def maxv(gameState, layer):
          if gameState.isWin() or gameState.isLose() or layer==lowest: #terminal utility
            return self.evaluationFunction(gameState)
          v = -9999999
          for a in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, a)
            v = max(v, minv(successor, layer+1))
          return v
          
        def minv(gameState, layer):
          if gameState.isWin() or gameState.isLose() or layer==lowest: #terminal utility
            return self.evaluationFunction(gameState)
          v = 9999999
          i = layer%anum
          for a in gameState.getLegalActions(i):
            successor = gameState.generateSuccessor(i, a)
            if i == anum-1:
              v = min(v, maxv(successor, layer+1))
            else:
              v = min(v, minv(successor, layer+1))
          return v
        
        maxa = -9999999
        for a in gameState.getLegalActions(0): #layer 0 kick off recursion
          successor = gameState.generateSuccessor(0, a)
          returnedv = minv(successor, layer+1) 
          if returnedv>maxa: 
            maxa=returnedv
            arg=a
        return arg



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #depth 1 with 3 agent= max(L0) min(L1) min(L2) terminal(L3)
        anum=gameState.getNumAgents()
        lowest=self.depth*anum #terminal layer
        layer=0 #start at first layer max


        def maxv(gameState, layer, alpha, beta):
          if gameState.isWin() or gameState.isLose() or layer==lowest: #terminal utility
            return self.evaluationFunction(gameState)
          v = -9999999
          for a in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, a)
            v = max(v, minv(successor, layer+1, alpha, beta))
            if v > beta: return v
            alpha = max(alpha, v)
          return v
          
        def minv(gameState, layer, alpha, beta):
          if gameState.isWin() or gameState.isLose() or layer==lowest: #terminal utility
            return self.evaluationFunction(gameState)
          v = 9999999
          i = layer%anum
          for a in gameState.getLegalActions(i):
            successor = gameState.generateSuccessor(i, a)
            if i == anum-1:
              v = min(v, maxv(successor, layer+1, alpha, beta))
            else:
              v = min(v, minv(successor, layer+1, alpha, beta))
            if v < alpha: return v
            beta = min(beta, v)
          return v
        
        maxa = -9999999
        alpha, beta = -9999999, 9999999
        for a in gameState.getLegalActions(0): #layer 0 kick off recursion
          successor = gameState.generateSuccessor(0, a)
          returnedv = minv(successor, layer+1, alpha, beta) 
          if returnedv>maxa: 
            maxa=returnedv
            arg=a
          alpha = max(alpha, maxa)
        return arg
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        anum=gameState.getNumAgents()
        lowest=self.depth*anum #terminal layer
        layer=0 #start at first layer max


        def maxv(gameState, layer):
          if gameState.isWin() or gameState.isLose() or layer==lowest: #terminal utility
            return self.evaluationFunction(gameState)
          v = -9999999
          for a in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, a)
            v = max(v, exv(successor, layer+1))
          return v
          
        def exv(gameState, layer):
          if gameState.isWin() or gameState.isLose() or layer==lowest: #terminal utility
            return self.evaluationFunction(gameState)
          v = 0
          i = layer%anum
          actions = gameState.getLegalActions(i)
          for a in actions:
            successor = gameState.generateSuccessor(i, a)
            if i == anum-1:
              v += maxv(successor, layer+1)
            else:
              v += exv(successor, layer+1)
          v = v/len(actions)
          return v
        
        maxa = -9999999
        for a in gameState.getLegalActions(0): #layer 0 kick off recursion
          successor = gameState.generateSuccessor(0, a)
          returnedv = exv(successor, layer+1) 
          if returnedv>maxa: 
            maxa=returnedv
            arg=a
        return arg

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      Inspired by Hints and Observations, and p.138 of Powerpoint 1
      There are three functions for calculating scores in ghost-hunting, pellet-nabbing, food-gobbling.

      ghost-hunting function "hunt(GameState)" return a hunting score:
      When the ScaredTimes is > 1, it encourages Pacman to hunt the ghost within 10 unit. The encouragement is huge by using Exponent of 3. ScaredTimes is set to be >1 because there is at least 2 unit time remaining to play safe, if not, Pacman dies easily when ScaredTimes back to 0 and Pacman is close to ghost.
      When the ScaredTimes is 0 or 1, it discourages Pacman to go near the ghost. It ensures Pacman is 3 steps away from ghost to play safe. The discouragement is huge by using Exponent of 3.
      Hunting ghosts and escaping from ghosts are the core of Pacman, so Exponent of 3 is used to show its importance.

      pellet-nabbing function "pellet(GameState)" return a pellet score:
      It encourages Pacman to go near pellet by using reciprocal of the manhattanDistance between Pacman and pellet, then multipy the reciprocal by 20. States with a nearby capsule obtain higher score. It increases the possibility of eating pellet and start hunting ghost.

      food-gobbling function "food(GameState)" return a total food score:
      It encourages Pacman to go to places with more food by summing up all the reciprocal of the manhattanDistance between Pacman and food. When Pacmen is in area with high density of food, the score is higher than inside area with few food. 

      Finally, use the built in getScore() function to get the system score.
      currentGameState.getScore() time pass -1, eat food +10, win +500, lose -500, hunted ghost +200
      It gives reward to eating and hunting, and gives penalty to spending more time.
      By adding this score to the above three scores, the final score is the score for betterEvaluation.
    """
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getPacmanPosition()

    #ghost-hunting
    def hunt(GameState):
      GhostStates = currentGameState.getGhostStates()
      ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

      ghostnum = len(GhostStates)
      ghunt = 0
      for i in range(1,ghostnum+1):
        ghostxy = GameState.getGhostPosition(i)
        gpdis = manhattanDistance(Pos,ghostxy)
        if ScaredTimes[i-1]>1: #at least 2 unit time remaining to play safe, if not, Pacman dies easily when ScaredTimes end and Pacman is close to ghost 
          if (10 - gpdis) > 0:ghunt += ((10 - gpdis) ** 3) #gain score if that ghost is within 10 steps
        else:
          if (3 - gpdis) > 0: ghunt -= ((3 - gpdis) ** 3) #deduct score if ghost within 3 steps
      return ghunt


    #pellet-nabbing
    def pellet(GameState):
      capxy = GameState.getCapsules()
      capnum = len(capxy)
      reciprocal = 0
      for i in range(capnum): #states where pacman has a nearby capsule obtain higher score
        reciprocal = max((20/manhattanDistance(Pos,capxy[i])), reciprocal)
      return reciprocal

    #food-gobbling
    def food(GameState): 
      foodxy = GameState.getFood().asList()
      foodnum = len(foodxy)
      reciprocalsum = 0
      for i in range(foodnum): #states where pacman has more food nearby obtain higher score
        reciprocalsum += (1/manhattanDistance(Pos,foodxy[i]))
      return reciprocalsum

    score = currentGameState.getScore() #time pass -1, eat food +10, win +500, lose -500, hunted ghost +200
    final = (score + hunt(currentGameState) + pellet(currentGameState) + food(currentGameState))
    #print(final)
    return final

# Abbreviation
better = betterEvaluationFunction

