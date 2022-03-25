from game import Directions
import random, util
from game import Agent

#######################################################
#            This portion is written for you          #
#######################################################

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
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


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        we assume ghosts act in turn after the pacman takes an action
        so your minimax tree will have multiple min layers (one for each ghost)
        for every max layer

        gameState.generateChild(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state

        self.evaluationFunction(state)
        Returns pacman SCORE in current state (useful to evaluate leaf nodes)

        self.depth
        limits your minimax tree depth (note that depth increases one means
        the pacman and all ghosts has already decide their actions)
        """
        actions_set = gameState.getLegalActions(0)
        v = -100000000
        sp_depth = self.depth
        for action in actions_set:
            self.depth -= 1
            cal_max_value = self.min_value(gameState.generateChild(0, action), 1)
            # print(action, cal_max_value)
            if  cal_max_value > v:
                v = cal_max_value
                res_action = action
            self.depth = sp_depth

        return res_action

    def max_value(self, gameState,agentIndex):
        if self.depth <= 0 or gameState.isWin() or gameState.isLose(): 
            return self.evaluationFunction(gameState)

        actions_set = gameState.getLegalActions(agentIndex)
        v = -100000000
        self.depth -= 1
        for action in actions_set:
            nextState = gameState.generateChild(agentIndex, action)
            v = max(v, self.min_value(nextState, agentIndex+1))

        return v

    def min_value(self, gameState, agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        actions_set = gameState.getLegalActions(agentIndex)
        v = +100000000
        for action in actions_set:
            nextState = gameState.generateChild(agentIndex, action)
            num_agent = gameState.getNumAgents()
            if agentIndex == num_agent -1:
                v = min(v, self.max_value(nextState, 0))
            else:
                v = min(v, self.min_value(nextState, agentIndex+1))
        
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -1000000000
        beta = +1000000000
        actions_set = gameState.getLegalActions(0)
        v = -100000000
        sp_depth = self.depth
        for action in actions_set:
            self.depth -= 1
            cal_max_value = self.min_value(gameState.generateChild(0, action), 1, alpha, beta)
            alpha = max (alpha, cal_max_value)
            
            if  cal_max_value > v:
                v = cal_max_value
                res_action = action
            
            self.depth = sp_depth

        return res_action

    def max_value(self, gameState,agentIndex, alpha, beta):
        if self.depth <= 0 or gameState.isWin() or gameState.isLose(): 
            return self.evaluationFunction(gameState)

        actions_set = gameState.getLegalActions(agentIndex)
        v = -100000000
        self.depth -= 1
        for action in actions_set:
            nextState = gameState.generateChild(agentIndex, action)
            v = max(v, self.min_value(nextState, agentIndex+1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, gameState, agentIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        actions_set = gameState.getLegalActions(agentIndex)
        v = +100000000
        for action in actions_set:
            nextState = gameState.generateChild(agentIndex, action)
            num_agent = gameState.getNumAgents()
            if agentIndex == num_agent -1:
                v = min(v, self.max_value(nextState, 0, alpha, beta))
            else:
                v = min(v, self.min_value(nextState, agentIndex+1, alpha, beta))

            if v <= alpha:
                return v
            beta = min(beta, v)
        return v