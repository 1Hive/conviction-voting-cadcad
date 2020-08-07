
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
    arrival_rate = 10/(1+s['sentiment'])
    rv1 = np.random.rand()
    new_participant = bool(rv1<1/arrival_rate)

    network = s['network']
    
    proposals = get_nodes_by_type(network, 'proposal')
    participants = get_nodes_by_type(network, 'participant')

    candidate_proposals = [j for j in proposals if network.nodes[j]['status']=='candidate']
    subgraph_nodes = candidate_proposals+participants

    candidate_subgraph = s['network'].subgraph(subgraph_nodes)
    supporters = get_edges_by_type(candidate_subgraph, 'support')
    
    len_parts = len(participants)
    #supply = s['supply'] 
    expected_holdings = .01*supply/len_parts
    if new_participant:
        h_rv = expon.rvs(loc=0.0, scale=expected_holdings)
        new_participant_holdings = h_rv
    else:
        new_participant_holdings = 0
    
    network = s['network']
    affinities = [network.edges[e]['affinity'] for e in supporters if e[1] in candidate_proposals]
    median_affinity = np.median(affinities)
    
    fund_requests = [network.nodes[j]['funds_requested'] for j in candidate_proposals]
    
    funds = s['funds']
    total_funds_requested = np.sum(fund_requests)
    
    if total_funds_requested == 0:
        new_proposal = True
        new_proposal_ct = 3
    else:
        proposal_rate = 1/(1-median_affinity) * total_funds_requested/funds
        rv2 = np.random.rand()
        new_proposal = bool(rv2<1/proposal_rate)
        new_proposal_ct = int(1-median_affinity)+1

    expected_request = beta*s['funds']/10
    new_proposal_requested = [expon.rvs(loc=expected_request/10, scale=expected_request) for ct in range(new_proposal_ct)]
        
    sentiment = s['sentiment']
    funds = s['funds']
    scale_factor = funds*sentiment**2/10000
    
    if scale_factor <1:
        scale_factor = 1
    
    #this shouldn't happen but expon is throwing domain errors
    if sentiment>.4: 
        funds_arrival = expon.rvs(loc = 0, scale = scale_factor )
    else:
        funds_arrival = 0
    
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