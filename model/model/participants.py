
import numpy as np
from .initialization import *
from .conviction_helper_functions import * 
import networkx as nx


# Phase 2
# Behaviors
def check_progress(params, step, sL, s):
    '''
    Driving processes: completion of previously funded proposals
    '''
    
    network = s['network']
    proposals = get_nodes_by_type(network, 'proposal')
    
    completed = []
    failed = []
    for j in proposals:
        if network.nodes[j]['status'] == 'active':
            grant_size = network.nodes[j]['funds_requested']
            likelihood = 1.0/(base_completion_rate+np.log(grant_size))
            
            failure_rate = 1.0/(base_failure_rate+np.log(grant_size))
            if np.random.rand() < likelihood:
                completed.append(j)
            elif np.random.rand() < failure_rate:
                failed.append(j)
    
    return({'completed':completed, 'failed':failed})


    
# Mechanisms
def complete_proposal(params, step, sL, s, _input):
    '''
     Book-keeping of failed and completed proposals. Update network object
     '''
    
    network = s['network']
    participants = get_nodes_by_type(network, 'participant')
    proposals = get_nodes_by_type(network, 'proposal')
    #competitors = get_edges_by_type(network, 'conflict')
    
    completed = _input['completed']
    for j in completed:
        network.nodes[j]['status']='completed'

        # for c in proposals:
        #      if (j,c) in competitors:
        #          conflict = network.edges[(j,c)]['conflict']
        #          for i in participants:
        #              network.edges[(i,c)]['affinity'] = network.edges[(i,c)]['affinity'] *(1-conflict)

        for i in participants:
            force = network.edges[(i,j)]['affinity']
            # sentiment = network.nodes[i]['sentiment']
            # network.nodes[i]['sentiment'] = get_sentimental(sentiment, force, decay=0)

                
    
    failed = _input['failed']
    for j in failed:
        network.nodes[j]['status']='failed' 
        for i in participants:
            force = -network.edges[(i,j)]['affinity']
            # sentiment = network.nodes[i]['sentiment']
            # network.nodes[i]['sentiment'] = get_sentimental(sentiment, force, decay=0)
    
    key = 'network'
    value = network
    
    return (key, value)


# Phase 3
# Behaviors
def participants_decisions(params, step, sL, s):
    '''
    High sentiment, high affinity =>buy
    Low sentiment, low affinities => burn
    Assign tokens to top affinities
    '''
    network = s['network']
    participants = get_nodes_by_type(network, 'participant')
    proposals = get_nodes_by_type(network, 'proposal')
    candidates = [j for j in proposals if network.nodes[j]['status']=='candidate']
    #sensitivity = params['sensitivity']
    
    gain = .01
    delta_holdings={}
    proposals_supported ={}
    for i in participants:
        
        #engagement_rate = .3*network.nodes[i]['sentiment']
        engagement_rate = .3*initial_sentiment
        if np.random.rand()<engagement_rate:
        
            #force = network.nodes[i]['sentiment']-sensitivity
            force = initial_sentiment - sensitivity
            delta_holdings[i] = network.nodes[i]['holdings']*gain*force
            
            support = []
            for j in candidates:
                booster = social_affinity_booster(network, j, i)
                affinity = network.edges[(i, j)]['affinity']+booster
                cutoff = sensitivity*np.max([network.edges[(i,p)]['affinity'] for p in candidates])
                if cutoff <.5:
                    cutoff = .5
                
                if affinity > cutoff:
                    support.append(j)
            
            proposals_supported[i] = support
        else:
            delta_holdings[i] = 0
            proposals_supported[i] = [j for j in candidates if network.edges[(i,j)]['tokens']>0 ]
    
    return({'delta_holdings':delta_holdings, 'proposals_supported':proposals_supported})

# Mechanisms
def update_tokens(params, step, sL, s, _input):
    '''
    Description:
    Udate everyones holdings and their conviction for each proposal
    '''
    
    network = s['network']
    delta_holdings = _input['delta_holdings']
    proposals = get_nodes_by_type(network, 'proposal')
    candidates = [j for j in proposals if network.nodes[j]['status']=='candidate']
    proposals_supported = _input['proposals_supported']
    participants = get_nodes_by_type(network, 'participant')
    
    for i in participants:
        network.nodes[i]['holdings'] = network.nodes[i]['holdings']+delta_holdings[i]
        supported = proposals_supported[i]
        total_affinity = np.sum([ network.edges[(i, j)]['affinity'] for j in supported])
        for j in candidates:
            if j in supported:
                normalized_affinity = network.edges[(i, j)]['affinity']/total_affinity
                network.edges[(i, j)]['tokens'] = normalized_affinity*network.nodes[i]['holdings']
            else:
                network.edges[(i, j)]['tokens'] = 0
            
            prior_conviction = network.edges[(i, j)]['conviction']
            current_tokens = network.edges[(i, j)]['tokens']
            network.edges[(i, j)]['conviction'] =current_tokens+alpha*prior_conviction
    
    for j in candidates:
        network.nodes[j]['conviction'] = np.sum([ network.edges[(i, j)]['conviction'] for i in participants])
        total_tokens = np.sum([network.edges[(i, j)]['tokens'] for i in participants ])
        if total_tokens < min_supp:
            network.nodes[j]['status'] = 'killed'
    
    key = 'network'
    value = network
    
    return (key, value)



