
import numpy as np
import pandas as pd
from .initialization import *
from .conviction_helper_functions import * 
import networkx as nx
from scipy.stats import expon, gamma

# hyperparameters
sentiment = 0.6


# Behaviors
def driving_process(params, step, sL, s):
    '''
    Driving process for adding new participants (their funds) and new proposals.
    '''
    arrival_rate = 10/(1+sentiment)
    rv1 = np.random.rand()
    new_participant = bool(rv1<1/arrival_rate)
    supporters = get_edges_by_type(s['network'], 'support')
    
    len_parts = len(get_nodes_by_type(s['network'], 'participant'))
    #supply = s['supply'] 
    expected_holdings = .1*supply/len_parts
    if new_participant:
        h_rv = expon.rvs(loc=0.0, scale=expected_holdings)
        new_participant_holdings = h_rv
    else:
        new_participant_holdings = 0
    
    network = s['network']
    affinities = [network.edges[e]['affinity'] for e in supporters ]
    median_affinity = np.median(affinities)
    
    proposals = get_nodes_by_type(network, 'proposal')
    fund_requests = [network.nodes[j]['funds_requested'] for j in proposals if network.nodes[j]['status']=='candidate' ]
    
    funds = s['funds']
    total_funds_requested = np.sum(fund_requests)
    
    proposal_rate = 1/median_affinity * (1+total_funds_requested/funds)
    rv2 = np.random.rand()
    new_proposal = bool(rv2<1/proposal_rate)
    
    #sentiment = s['sentiment']
    funds = s['funds']
    scale_factor = funds*sentiment**2/10000
    
    if scale_factor <1:
        scale_factor = 1
    
    #this shouldn't happen but expon is throwing domain errors
    if sentiment>.4: 
        funds_arrival = expon.rvs(loc = 0, scale = scale_factor )
    else:
        funds_arrival = 0
    
    return({'new_participant':new_participant,
            'new_participant_holdings':new_participant_holdings,
            'new_proposal':new_proposal, 
            'funds_arrival':funds_arrival})

    
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
        network= gen_new_proposal(network,funds,supply)
    
    #update age of the existing proposals
    proposals = get_nodes_by_type(network, 'proposal')
    
    for j in proposals:
        network.nodes[j]['age'] =  network.nodes[j]['age']+1
        if network.nodes[j]['status'] == 'candidate':
            requested = network.nodes[j]['funds_requested']
            network.nodes[j]['trigger'] = trigger_threshold(requested, funds, supply)
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