
import numpy as np
from .initialization import *
from .conviction_helper_functions import * 
import networkx as nx

# parameters:
sensitivity = 0.75
tmin = 7

# Behaviors
def trigger_function(params, step, sL, s):
    '''
    This policy checks to see if each proposal passes or not. 
    '''
    network = s['network']
    funds = s['funds']
    #supply = s['supply']
    proposals = get_nodes_by_type(network, 'proposal')
    
    accepted = []
    triggers = {}
    funds_to_be_released = 0
    for j in proposals:
        if network.nodes[j]['status'] == 'candidate':
            requested = network.nodes[j]['funds_requested']
            age = network.nodes[j]['age']
            threshold = trigger_threshold(requested, funds, supply)
            if age > tmin:
                conviction = network.nodes[j]['conviction']
                if conviction >threshold:
                    accepted.append(j)
                    funds_to_be_released = funds_to_be_released + requested
        else:
            threshold = np.nan
            
        triggers[j] = threshold
        
        #catch over release and keep the highest conviction results
        if funds_to_be_released > funds:

            ordered = conviction_order(network, accepted)
            accepted = []
            release = 0
            ind = 0
            while release + network.nodes[ordered[ind]]['funds_requested'] < funds:
                accepted.append(ordered[ind])
                release= network.nodes[ordered[ind]]['funds_requested']
                ind=ind+1
                
                    
    return({'accepted':accepted, 'triggers':triggers})

# Mechanisms
def decrement_funds(params, step, sL, s, _input):
    '''
    If a proposal passes, funds are decremented by the amount of the proposal
    '''
    
    funds = s['funds']
    network = s['network']
    accepted = _input['accepted']

    #decrement funds
    for j in accepted:
        funds = funds - network.nodes[j]['funds_requested']
    
    key = 'funds'
    value = funds
    
    return (key, value)

def update_proposals(params, step, sL, s, _input):
    '''
    If proposal passes, its status is changed in the network object.
    '''
    
    network = s['network']
    accepted = _input['accepted']
    triggers = _input['triggers']
    participants = get_nodes_by_type(network, 'participant')
    proposals = get_nodes_by_type(network, 'proposals')
    #sensitivity = params['sensitivity']
    
    for j in proposals:
        network.nodes[j]['trigger'] = triggers[j]
    
    #bookkeeping conviction and participant sentiment
    for j in accepted:
        network.nodes[j]['status']='active'
        network.nodes[j]['conviction']=np.nan
        #change status to active
        for i in participants:
        
            #operating on edge = (i,j)
            #reset tokens assigned to other candidates
            network.edges[(i,j)]['tokens']=0
            network.edges[(i,j)]['conviction'] = np.nan
            
            #update participants sentiments (positive or negative) 
            affinities = [network.edges[(i,p)]['affinity'] for p in proposals if not(p in accepted)]
            if len(affinities)>1:
                max_affinity = np.max(affinities)
                force = network.edges[(i,j)]['affinity']-sensitivity*max_affinity
            else:
                force = 0
            
            #based on what their affinities to the accepted proposals
            #network.nodes[i]['sentiment'] = get_sentimental(network.nodes[i]['sentiment'], force, False)
            
    
    key = 'network'
    value = network
    
    return (key, value)