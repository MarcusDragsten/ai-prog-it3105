import tensorflow as tf
from Actor import ANET
import os
from StateManager import StateManager
from NeuralNetwork import cross_entropy_loss
import numpy as np
import math

import copy
# import matplotlib.pyplot as plt
# from matplotlib.patches import Rectangle

#  for grafikk




import matplotlib
import matplotlib.pyplot as plt

class Topp:
    def __init__(self, config, topp_config):
        self.state_manager = StateManager(config)
        
        """ MULIG DU MÅ ENDRE DENNE SIMEN """
        path_list = [anet_path for anet_path in os.scandir("Project2/TrainedNets/{folder}".format(folder=config['network_folder_name']))]
        
        self.anets = self.get_anets(path_list)
        self.number_of_anets = len(self.anets)
        self.number_of_games = topp_config['number_of_games']
        self.winner1 = 0
        self.winner2 = 0
        self.serie1 = 0
        self.serie2 = 0
        self.serie_total = np.zeros((self.number_of_anets,), int)
        self.champions = None
        self.total = None
        self.vis_game_states = []
        self.number_of_vis = 1
        self.game_number = 0
        
        
        
    def get_anets(self, path_list):
        
        anets = []

        for i, path in enumerate(path_list):
            
            model = tf.keras.models.load_model(path, custom_objects={"custom_cross_entropy": cross_entropy_loss})
            anet = ANET(model, None, None, None, None, None,0, 1, self.state_manager)
            anets.append((int(path.name), anet))
           
        anets.sort(key=lambda x: x[0])
        
        return anets
            
    
    def play_one_game(self, agent1, agent2, game_vis):
        
        agents = (self.anets[agent1][1], self.anets[agent2][1])
        
        
        gamestate = self.state_manager.get_state()
        self.state_manager.reset_game()
        current_player = 0
        
        # print("GAMESTATE FROM TOPP", gamestate)
        self.game_number +=1
        
        while not self.state_manager.is_finished(gamestate):
            
            action = agents[current_player].get_action(False, gamestate, current_player + 1, True)
            
            # Grafikk
            gamestate = self.state_manager.get_state()
            
            if self.number_of_vis >= self.game_number:
                self.vis_game_states.append(copy.deepcopy(gamestate))
            
            
            self.state_manager.do_move(action)
            gamestate = self.state_manager.get_state()
            
            if current_player == 0:
                current_player = 1
            else:
                current_player = 0
        
        
        if game_vis:
            self.vis_game()
           
            
            
                
        winner = self.state_manager.get_winner(gamestate)
        
        if winner == 1:
                self.winner1 +=1
                # print(f'Player {agent1} won')
        elif winner == 2:
                self.winner2 +=1
                # print(f'Player {agent2} won')
        
        return winner
    
    def bestVSbest(self):
        for game in range(self.number_of_games):
            self.play_one_game(2, 2)
        # print('spiller 1:', self.winner1)
        # print('spiller 2:', self.winner2)
                       
        
         
        
    def play_round_robin(self):
        
        champions = np.zeros((self.number_of_anets, self.number_of_anets), int)
        total = np.zeros((self.number_of_anets,), int)
        winner1 = np.zeros((self.number_of_anets,), int)
        winner2 = np.zeros((self.number_of_anets,), int)
        
        
        # print(total)
        game_vis = False
        
        for agent1 in range(self.number_of_anets):
            
            for agent2 in range(self.number_of_anets):
                if agent1 == agent2:
                    continue
                
                
                self.serie1 = 0
                self.serie2 = 0
                for game in range(math.floor(self.number_of_games / 2)):
                    
                    self.state_manager.reset_game()
                    outcome = self.play_one_game(agent1, agent2, game_vis)
                    game_vis = False

                    if outcome == 1:
                        # print("Player", agent1, "won against player", agent2,)
                        # print("Matrix before win", champions)
                        champions[agent1][agent2] += 1
                        total[agent1] += 1
                        self.serie1 += 1
                        
                        # print("Matrix after win", champions)
                    elif outcome == 2:
                        # print("Player", agent2, "won against player", agent1,)
                        # print("Matrix before win", champions)
                        total[agent2] += 1
                        champions[agent2][agent1] += 1
                        self.serie2 += 1
                        # print("Matrix after win", champions)
                if self.serie1 > self.serie2:
                    self.serie_total[agent1] += 1
                else:
                    self.serie_total[agent2]+= 1


        
        self.champions = champions        
        self.total = total        
        # print(self.champions)
        # print(self.total)
        # print('spiller 1:', self.winner1)
        # print('spiller 2:', self.winner2)
        # print('serie_total', self.serie_total)
        
        topp_robin = True
        topp_total = True
        
        
        if topp_robin:
            self.visualize_robin()
            
        if topp_total:
            self.visualize_total()



    def visualize_robin(self):
      
    
        width = 5
        
        max_height = np.max(self.serie_total)
        max_width = len( self.total)*width
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.title("Round robin")
        ax.set_ylabel('Number of series win in round robin ')
        ax.set_xlabel('More trained nets to the right')
        

        print('total serier', self.serie_total)
        for i, height in enumerate(self.serie_total):
            
            rect3 = matplotlib.patches.Rectangle((width*i,0 ), 4, height,color ='yellow')
            ax.add_patch(rect3)
            
        plt.xlim([0, max_width])
        plt.ylim([0, max_height+2])
        
        plt.show()
        
    def visualize_total(self):
        
        width = 5
        
        max_height = np.max(self.total)
        max_width = len( self.total)*width
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.title("Total victories")
        ax.set_ylabel('Number wins ')
        ax.set_xlabel('More trained nets to the right')
        

        print('total won', self.total)
        for i, height in enumerate(self.total):
            
            rect3 = matplotlib.patches.Rectangle((width*i,0 ), 4, height,color ='blue')
            ax.add_patch(rect3)
            
        plt.xlim([0, max_width])
        plt.ylim([0, max_height+2])
        
        plt.show()
        
    
    def vis_game(self):
        # print('self.vis_game', self.vis_game_states, self.number_of_vis)
        self.state_manager.vis_entire_game(self.vis_game_states, self.number_of_vis)
            

        
        
