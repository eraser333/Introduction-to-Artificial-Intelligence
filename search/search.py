"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

#######################################################
#            This portion is written for you          #
#######################################################

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A example of heuristic function which estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial. You don't need to edit this function
    """
    return 0

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    previous_dict = dict()
    frontier.push(problem.getStartState())
    previous_dict[problem.getStartState()] = "start"

    while not frontier.isEmpty():
        cur_state = frontier.pop()

        if problem.isGoalState(cur_state):
            goal_state = cur_state
            break

        for next_state in problem.expand(cur_state):
            if next_state[0] not in previous_dict:
                frontier.push(next_state[0])
                previous_dict[next_state[0]] = (cur_state , next_state[1]) 

    path = []
    while previous_dict[goal_state] != "start":
        path.append(previous_dict[goal_state][1])
        goal_state = previous_dict[goal_state][0]
    
    path.reverse()
    return path

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    previous_dict = dict()

    start_state = problem.getStartState()
    frontier.push(start_state)
    previous_dict[start_state] = "start"

    while not frontier.isEmpty():
        cur_state = frontier.pop()

        if problem.isGoalState(cur_state):
            goal_state = cur_state
            break
        
        for next_state in problem.expand(cur_state):
            if next_state[0] not in previous_dict:
                frontier.push(next_state[0])
                previous_dict[next_state[0]] = (cur_state , next_state[1]) 

    path = []
    while previous_dict[goal_state] != "start":
        path.append(previous_dict[goal_state][1])
        goal_state = previous_dict[goal_state][0]
    
    path.reverse()
    return path

def uniformCostSearch(problem):
    """Search the node of least cost from the root."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    previous_dict = dict()
    path_cost = dict()

    start_state = problem.getStartState()
    frontier.push(start_state, 0)
    previous_dict[start_state] = "start"
    path_cost[start_state] = 0

    while not frontier.isEmpty():
        cur_state = frontier.pop()
        if problem.isGoalState(cur_state):
            goal_state = cur_state
            break

        for next_state in problem.expand(cur_state):  
            new_path_cost =  path_cost[cur_state]+ next_state[2]
            if next_state[0] not in previous_dict:
                frontier.push(next_state[0], new_path_cost) 
                previous_dict[next_state[0]] = (cur_state , next_state[1]) 
                path_cost[next_state[0]] = new_path_cost
            else:
                if path_cost[next_state[0]] > new_path_cost:
                    frontier.update(next_state[0], new_path_cost) 
                    previous_dict[next_state[0]] = (cur_state , next_state[1]) 
                    path_cost[next_state[0]] = new_path_cost

    path = []
    while previous_dict[goal_state] != "start":
        path.append(previous_dict[goal_state][1])
        goal_state = previous_dict[goal_state][0]
    
    path.reverse()
    return path

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    previous_dict = dict()
    g_cost = dict()
    f_cost = dict()

    start_state = problem.getStartState()
    f_start = heuristic(start_state, problem)
    frontier.push(start_state, f_start)
    previous_dict[start_state] = "start"
    g_cost[start_state] = 0
    f_cost[start_state] = f_start

    while not frontier.isEmpty():
        cur_state = frontier.pop()
        if problem.isGoalState(cur_state):
            goal_state = cur_state
            break
        
        for next_state in problem.expand(cur_state):
            new_g_cost = g_cost[cur_state] + next_state[2]
            new_f_cost = new_g_cost + heuristic(next_state[0], problem)
            if next_state[0] not in previous_dict:
                frontier.push(next_state[0], new_f_cost) 
                g_cost[next_state[0]] = new_g_cost
                f_cost[next_state[0]] = new_f_cost
                previous_dict[next_state[0]] = (cur_state , next_state[1]) 
            else:
                if f_cost[next_state[0]] > new_f_cost:
                    frontier.update(next_state[0], new_f_cost)
                    g_cost[next_state[0]] = new_g_cost
                    f_cost[next_state[0]] = new_f_cost
                    previous_dict[next_state[0]] = (cur_state , next_state[1]) 


    path = []
    while previous_dict[goal_state] != "start":
        path.append(previous_dict[goal_state][1])
        goal_state = previous_dict[goal_state][0]
    
    path.reverse()
    return path

