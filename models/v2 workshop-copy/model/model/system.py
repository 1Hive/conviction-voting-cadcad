
import numpy as np
import pandas as pd
from .initialization import *
from .conviction_helper_functions import * 
import networkx as nx
from scipy.stats import expon, gamma



# Behaviors
def driving_process(params, step, sL, s):
    '''
    Driving process for adding new participants (their funds) and new proposals.
    '''
    ###WORKSHOP###
    #construct heuristics for arrival of 
    #new funds (added to communal funds)
    #new participants (and personal funds)
    #new Proposals

    ### helpful data collection from the state
    funds = s['funds']
    network = s['network']
    sentiment = s['sentiment']
    proposals = get_nodes_by_type(network, 'proposal')
    participants = get_nodes_by_type(network, 'participant')
    candidate_proposals = [j for j in proposals if network.nodes[j]['status']=='candidate']
    
    #### Part 1:
    # Arrival of New Funds

    #### Part 2:
    # Arrival of a new participant?
    # how much holdings do they have?

    #### Part 3:
    # Arrival of new proposals?
    # How many?
    # how much funds are they requesting?


    return({'new_participant':new_participant, #True/False
            'new_participant_holdings':new_participant_holdings, #funds held by new participant if True
            'new_proposal':new_proposal, #True/False
            'new_proposal_ct': new_proposal_ct, #int
            'new_proposal_requested':new_proposal_requested, #list funds requested by new proposal if True, len =ct
            'funds_arrival':funds_arrival}) #quantity of new funds arriving to the communal pool

    
# Mechanisms 
def update_network(params, step, sL, s, _input):
    '''
    Add new participants and proposals to network object
    '''

    network = s['network']
    funds = s['funds']
    #supply = s['supply']

    new_participant = _input['new_participant'] 
    new_proposal = _input['new_proposal']

    if new_participant:
        new_participant_holdings = _input['new_participant_holdings']
        network = gen_new_participant(network, new_participant_holdings)
    
    if new_proposal:
        for ct in range(_input['new_proposal_ct']):
            funds_req = _input['new_proposal_requested'][ct]
            network= gen_new_proposal(network,funds,supply, beta, rho, alpha, funds_req)
    
    #update age of the existing proposals
    proposals = get_nodes_by_type(network, 'proposal')
    
    for j in proposals:
        network.nodes[j]['age'] =  network.nodes[j]['age']+1
        if network.nodes[j]['status'] == 'candidate':
            requested = network.nodes[j]['funds_requested']
            network.nodes[j]['trigger'] = trigger_threshold(requested, funds, supply, beta, rho, alpha)
        else:
            network.nodes[j]['trigger'] = np.nan
            
    key = 'network'
    value = network
    
    return (key, value)

def increment_funds(params, step, sL, s, _input):
    '''
    Increase funds by the amount of the new particpant's funds.
    '''
    funds = s['funds']
    funds_arrival = _input['funds_arrival']

    #increment funds
    funds = funds + funds_arrival
    
    key = 'funds'
    value = funds
    
    return (key, value)