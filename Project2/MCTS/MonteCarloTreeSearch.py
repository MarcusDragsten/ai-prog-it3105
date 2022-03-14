# import sys
# sys.path.append("..") 
 
from Node import Node
import numpy as np

# from StateManager import StateManager
# from parameters import 




class MCTS:
    def ___init___(self, exploration_weight, actor, stateManager):
        """

        Class for Monte Carlo Searc Tree

        PARAMS: exploration_weight, actor, stateManager

        RETURN: nothing

        """
        self.root = Node(
            state = stateManager.get_state(),
            parent = None,
            player = stateManager.get_current_player() # input?
            )

        self.exp_weight = exploration_weight
        self.actor = actor # obj
        self.stateManager = stateManager # obj

# Main-kok
    def get_normalized_distribution(self):
        """

        Method fetching the distribution

        PARAMS: nothing

        RETURNS: the normalized distribution 

        """

        
        """
        Gets the distribution of visit counts of the children of the root
        :return: The normalized distribution
        """
        # Mix med niclas
        board_shape = self.simworld.get_grid().shape
        distribution = np.zeros(board_shape)
        for action in self.root.kid: #Itererer alle barna til roten? Ikke alle?
                distribution.append(float(self.root.kid[action].count) / float(self.root.count))
        return distribution.flatten()

        # Dette er fra main. Kan evt testes
        # board_shape = self.simworld.get_grid().shape
        # distribution = np.zeros(board_shape)
        # for action in self.root.kid: #Itererer alle barna til roten? Ikke alle?
        #     kid = self.root.kid[action]
        #     distribution[action] = kid.count
        # distribution = distribution.flatten()
        # return distribution / np.sum(distribution)    

        



    def mcts(self):
        """

        Method for running the mcts algorithm.

        PARAMS: nothing 

        RETURNS: nothing

        """

        if self.stateManager.game_done(self.root.get_state): #Sjekk opp metodNavn til done
            return # Kunne returnert noe her for å skille seg fra kok. 
        
        # Bør legge inn en raise her hvis det ikke eksisterer en node


    # 1. Tree Search - Traversing the tree from the root to a leaf node by using the tree policy
        leaf = self.search() # returns current_node

        # Check if the leaf is at the end
        if self.stateManager.game_done(leaf.get_state()):
            rew = self.stateManager.get_reward(leaf.get_state())
            self.backpropagation(leaf, rew)
            return

        
    # 2. Node Expansion - Generating some or all child states of a parent state, 
    # and then connecting the tree node housing the parent state (a.k.a. parent node) 
    # to the nodes housing the child states (a.k.a. child nodes).

        # Find ALL the leaf for the input node
        kids = self.new_leafs(leaf)


    # 3. Leaf Evaluation - Estimating the value of a leaf node in the tree by doing
    # a rollout simulation using the default policy from the leaf node’s state to a final state

        # Chooses one of the new kids found in new_leafs
        kid = np.random(kids)

        # Leaf evaluation // a rollout
        leaf, rew = self.leaf_evaluation(kid)



    # 4. Backpropagation - Passing the evaluation of a final state back up the tree, 
    # updating relevant data (see course lecture notes) at all nodes and edges 
    # on the path from the final state to the tree root.

        # Kommenatren under er kok
        # If only nodes in MCT should be updated change leaf to successor
        self.backpropagation(kid, rew)
   

    def update_root(self, action):
        """

        Method for updating the root

        PARAMS: action

        RETURNS: nothing

        """
        _temp_root = self.root.get_kid(action)
        if not _temp_root: # kok - usikker hva som skjer her
            self.root = Node(
                state = self.stateManager.get_state(),
                parent = None, 
                player = self.stateManager.get_current_player()
            )
        self.root = _temp_root

    def search(self):
        """

        Method for traversing the tree from the root to a leaf node by using the actor.

        PARAMS: nothing

        RETURNS: a leaf node

        """


        current_node = self.root

        #  Er vell bare å bruke player her?
        player = current_node.get_player()   
        flag = 0   
        if player == 1:
            flag = 1
        elif player == 2:
            flag = -1
        else:
            raise TypeError("Sorry, the player int is not compatible")

        max = -flag * float('inf')
        current_best = None
        kids = current_node.get_kids()

        for action in kids:
            # hvorfor a?
            a = current_node.get_q_value(action) + flag * current_node.get_u_value(action, self.exp_weight)
            
            if (a < max and flag == -1) or (a > max and flag == 1):
                max = a
                current_best = action

            flag *= -1
            current_node = current_node.get_kid_with_action(current_best)
            return current_node


    
    def new_leafs(self, leaf): # Node expansion
        """

        Method - Generating all(atm) child states of a parent state, 
              and then connecting the tree node housing the parent state (a.k.a. parent node) 
              to the nodes housing the kid states (a.k.a. kid nodes)

        PARAMS: leaf-node

        RETURNS: a set of new kids from the input parent 'leaf'

        """
        # merk at denne finne alle nye leafs. 

        state = leaf.get_state()
        # player = leaf.get_player()

        state_action_list, player = self.stateManager.get_kids(state, player)
        kids = []

        for state, action in state_action_list:
            kids = leaf.get_kid_with_action(action, rollout = True)
            leaf.remove_kid(action, rollout = True)

            if not kid: # Sjekk om man kan bruke noe annet her
                kid = Node(state, leaf, player)
            leaf.add_kid(kid, action)
            kids.append(kid)
        return kids


    def leaf_evaluation(self, from_node):  # rollout
        """

        Method for traversing the tree from the root to a leaf node by using the actor.

        PARAMS: from_node

        RETURNS: a leaf node

        """
        
        leaf = from_node.get_state()
        player = from_node.get_player()
        done = self.stateManager.game_done(leaf) #Sjekk opp metodNavn
        parent = from_node 

        while done == False:
            action = self.actor.get_action(leaf, player)
            leaf, player = self.stateManager(player, leaf, action)
            next_leaf = parent.get_kid_with_action(action, rollout = True)

            if not next_leaf:
                next_leaf = Node(leaf, parent, player)
                parent.add_kid(next_leaf, action, rollout = True)
            parent = next_leaf
            done = self.stateManager.game_done(leaf) #Sjekk opp metodNavn
        
        final_leaf = parent.get_state()  # Kan smelle disse sammen
        rew = self.stateManager.get_reward(final_leaf) # Kan smelle disse sammen
        # Disse to over bør egt ikke lagres som egne variabler, da de ikke brukes    
        return parent , rew


    def backpropagation(self, leaf, rew):
        """

        Method - Passing the evaluation of a final state back up the tree,
              updating relevant data at all nodes and edges on the path from 
              the final state to the tree root.

        PARAMS: leaf-node , reward


        RETURNS: a set of new kids from the input parent 'leaf'

        """
    
        current_node = leaf

        while self.root != current_node:
            current_node.update_evaluate(rew)
            current_node.update_count()

            # Update current_node to it's parent for the next iteration
            current_node = current_node.get_parent()
        
        self.root.update_evaluate(rew)
        self.root.update_count()
















       




      
        

            


                
            

