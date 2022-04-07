from collections import defaultdict
import numpy as np

class Node: 
    def __init__(self, state, parent, player):
        """

        Class for a node, which is to be used in the Monte Carlo Searc Tree -class

        PARAMS: state, parent, player

        """   

        self.state = state
        self.player = player
        self.parent = parent
        self.kids = defaultdict(lambda: None)
        self.kids_rollout = defaultdict(lambda: None)
        self.evaluate = 0
        self.count = 0
        

    def update_count(self):
        """

        Method - Increment the visits-counter of the node. 

        PARAMS: nothing

        RETURNS: nothing 

        """
        self.count +=1
        

    def update_evaluate(self, eval):
        """

        Method - Update the evaluation of a node. 

        PARAMS: eval

        RETURNS: nothing 

        """
        self.evaluate += eval


    def get_player(self):
        """

        Method - Fetch the player int. 

        PARAMS: nothing

        RETURNS: int 

        """
        return self.player


    def get_state(self):
        """

        Method - Fetch the node state 

        PARAMS: nothing

        RETURNS: int? 

        """
        return self.state


    def get_kids(self):
        """

        Method - Fetch the kids for the node 

        PARAMS: nothing

        RETURNS: dict of kids 

        """
        return self.kids
    
    def get_roll_kids(self):
        """

        Method - Fetch the kids for the node 

        PARAMS: nothing

        RETURNS: dict of kids 

        """
        return self.kids_rollout

    def add_kid(self, kid, action, rollout = False):
        """

        Method - Add a kid to to node 

        PARAMS: kid, action, rollout
  
        RETURNS: nothing

        """
        
        if rollout == True:
            self.kids_rollout[action] = kid

        else:
            self.kids[action] = kid
            


    def get_kid_with_action(self, action, rollout = False):
        """

        Method - Fetch a kid with a action 

        PARAMS: action, rollout

        RETURNS: kid node

        """
        
        if rollout == True:
            return self.kids_rollout[action]
        else:
            return self.kids[action]


    def remove_kid(self, action, rollout = False):
        """

        Method - Remove the kid with the action from the input

        PARAMS: action, rollout

        RETURNS: kid node

        """
        if rollout == True:
            self.kids_rollout[action] = None
        else:
            self.kids[action] = None
        

    
    def get_action_count(self, action):
        """

        Method - Fetch the action count from the kid with the action input

        PARAMS: action

        RETURNS: kid, or 0

        """

        if self.kids[action]:
            return self.kids[action].count
        else:
            return 0

    
    def get_kids_count(self):
        """

        Method - Fetch the numbers of kids the node have
        
        PARAMS: nothinh

        RETURNS: int

        """

        return len(self.kids)

    
    def get_parent(self):
        """

        Method - Fetch the parent of the node 

        PARAMS: nothing

        RETURNS: parent

        """

        return self.parent


    def get_q_value(self, action):
        """

        Method - Fetch the q-value

        PARAMS: action

        RETURNS: int

        """
    
        if self.get_action_count(action) == 0:
            return 0
        return self.get_kid_with_action(action).evaluate / (self.get_action_count(action))

    
    def get_u_value(self, action, exploration_weight):
        """

        Method - Fetch the u-value

        PARAMS: action, exploration_weight

        RETURNS: int (flooat?)

        """
        return exploration_weight * np.sqrt(np.log(self.count) / (1 + self.get_action_count(action)))
        
        
    """ FÅR SE OM VI SKAL BEHOLDE DENNE UNDER """
        
    def UCT(self, player, exploration_weight):
        
        if player == 2:
                exploration_weight = exploration_weight*-1
                
                
        if self.count == 0:
            return exploration_weight * float("inf")
        else:
            exploitation = self.evaluate  / (self.count)
        
        exploration = exploration_weight * np.sqrt(2 * np.log(self.parent.count) / (self.count))
        
        if player == 1:
            return exploitation + exploration
        else:
            return exploitation + exploration