# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 22:36:50 2017

@author: heng
"""

import numpy as np
import pandas as pd
import nash
import time

np.random.seed(2)  # reproducible

N_AGENTS = 2
N_STATES = 31   # the number of possible states 
STATES = [(1, 4), (2, 5), (2, 6), (2, 7), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10)]
ACTIONS = ['decelerate', 'maintain', 'accelerate']    # available action with grids to move
EPSILON = 0.9   # greedy police
ALPHA = 0.1     # learning rate
GAMMA = 0.9    # discount factor
MAX_EPISODES = 1000   # maximum episodes
FRESH_TIME = 0.3    # fresh time for one move


def build_q_table(states, actions):
    table = pd.DataFrame(
        np.zeros((len(actions), len(actions))),     # q_table initial values
		index=actions,
        columns=actions,    # actions's name
    )
    q_table = {state:table for state in states}
    #print table   # show table
    return q_table


def choose_action(state, q_table_1, q_table_2, eta_1, eta_2):
    # This is how to choose an action
    if (np.random.uniform() > EPSILON) or ((q_table_1[state].all().all() == 0) and (q_table_2[state].all().all()  == 0)):  # act non-greedy or state-action have no value
        action_1 = np.random.choice(ACTIONS)
        action_2 = np.random.choice(ACTIONS)
    else:
        # act greedy
        mu_1 = {k: v / sum(eta_1.values()) for k, v in eta_1.iteritems()}
        mu_2 = {k: v / sum(eta_2.values()) for k, v in eta_2.iteritems()}
        
        ficitious_action_2 = max(mu_1, key=mu_1.get)
        ficitious_action_1 = max(mu_2, key=mu_2.get)
        
        action_1 = q_table_1[state][ficitious_action_2].idxmax()
        action_2 = q_table_2[state][ficitious_action_1].idxmax()
    #print eta_1, eta_2
    #print action_1, action_2
    return action_1, action_2

def get_env_feedback(S, action_1, action_2):
    # This is how agent will interact with the environment
    movements = {'decelerate':1, 'maintain':2, 'accelerate':3}
    
    if (S[0] + movements[action_1] < 7) and (S[0] + movements[action_1] > 3):
        S_ = (S[0] + movements[action_1] + 3, min(10, S[1] + movements[action_2]))
    else:       
        S_ = (min(10, S[0] + movements[action_1]), min(10, S[1] + movements[action_2]))

    if action_1 == 'decelerate':
        R1 = -1
    elif action_1 == 'accelerate':
        R1 = -1
    else:
        R1 = 0

    if action_2 == 'decelerate':
        R2 = -1
    elif action_2 == 'accelerate':
        R2 = -1
    else:
        R2 = 0

    if S_[0] == S_[1]:
        R1 -= 10000	
        R2 -= 10000
    elif (S[0] < S[1] - 3) and (S_[0] > S_[1]):
        R1 -= 10000	
        R2 -= 10000
    elif (S[0] > S[1] - 3) and (S_[0] < S_[1]):
        R1 -= 10000	
        R2 -= 10000
    elif (S_[0] == 10) or (S_[1] == 10):
        R1 += 1000
        R2 += 1000     
    #print S_, R1, R2
    return S_, R1, R2


def rl():
    # main part of RL loop
	# for all agents, all states, all actions, set Q^i(S, A) = 0
    q_table_1 = build_q_table(STATES, ACTIONS)
    q_table_2 = build_q_table(STATES, ACTIONS)

    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = (1, 4) # initial state, agent1 in location 1 and agent2 in location4
        eta_1 = {'decelerate':1, 'maintain':1, 'accelerate':1} #history of actions of agent2
        eta_2 = {'decelerate':1, 'maintain':1, 'accelerate':1} #history of actions of agent1
          
        is_terminated = False

        while not is_terminated:

            action_1, action_2 = choose_action(S, q_table_1, q_table_2, eta_1, eta_2)
            eta_1[action_2] += 1 
            eta_2[action_1] += 1 
            
            S_, R1, R2 = get_env_feedback(S, action_1, action_2)  # take action & get next state and reward
            
            q_predict_1 = q_table_1[S].loc[action_1, action_2]
            q_predict_2 = q_table_2[S].loc[action_1, action_2]

            if (S_[0] != 10) and (S_[1] != 10):
                q_target_1 = R1 + GAMMA * q_table_1[S_].loc[action_1, action_2]   # next state is not terminal
                q_target_2 = R2 + GAMMA * q_table_2[S_].loc[action_1, action_2]   # next state is not terminal
            else:
                q_target_1 = R1     # next state is terminal
                q_target_2 = R2     # next state is terminal
                is_terminated = True    # terminate this episode

            temp1 = q_table_1[S].copy()
            temp1.loc[action_1, action_2] += ALPHA * (q_target_1 - q_predict_1)  
            q_table_1[S] = temp1
            
            temp2 = q_table_2[S].copy()
            temp2.loc[action_1, action_2] += ALPHA * (q_target_2 - q_predict_2)  
            q_table_2[S] = temp2
            S = S_  # move to next state

            step_counter += 1
    #print 'q_predict_1: %d' %(q_predict_1), 'q_predict_2: %d' %(q_predict_2)
    #print 'q_target_1: %d' %(q_target_1), 'q_target_2: %d' %(q_target_2)
    #print 'episode: %d' %(episode)
    return q_table_1, q_table_2

if __name__ == "__main__":
    q_table_1, q_table_2 = rl()
    #print q_table_1, q_table_2
