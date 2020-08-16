
import numpy as np
import pandas as pd
import networkx as nx
from .utils import * 

# Behaviors
def kpi_calculations(params, step, sL, s):
    '''
    Behavior for assessing the health of the system
    '''

    # read in state variables
    network = s['network']
    effective_supply = s['effective_supply']
    total_supply = s['total_supply']
    funds = s['funds']
    
    
    # calculate percentages
    fractionOfSupplyForVoting = effective_supply/total_supply
    fractionOfSupplyInPool = total_supply/funds
       
    
    proposals = get_nodes_by_type(network, 'proposal')

    # fraction of proposals in different stages
    total_proposals = len(proposals)
    active_proposals = len([j for j in proposals if network.nodes[j]['status']=='active'])
    completed_proposals = len([j for j in proposals if network.nodes[j]['status']=='completed'])
    killed_proposals = len([j for j in proposals if network.nodes[j]['status']=='killed'])
    proposal_stages = {'percentageOfActive': active_proposals/total_proposals,
                       'percentageOfCompleted':completed_proposals/total_proposals,
                       'percentageOfKilled':killed_proposals/total_proposals}
    
    #fraction of money in the different states
    total_funds_requested = []
    active_funds_requested = []
    completed_funds_requested = []
    killed_funds_requested = []

    for i in proposals:
        total_funds_requested.append(network.nodes[i]['funds_requested'])
        if network.nodes[i]['status'] == 'active':
            active_funds_requested.append(network.nodes[i]['funds_requested'])
        if network.nodes[i]['status'] == 'completed':
            completed_funds_requested.append(network.nodes[i]['funds_requested'])
        if network.nodes[i]['status'] == 'killed':
            killed_funds_requested.append(network.nodes[i]['funds_requested'])
            
    money_stages = {'percentageOfActiveFundsRequested': sum(active_funds_requested)/sum(total_funds_requested),
                       'percentageOfCompletedFundsRequested':sum(completed_funds_requested)/sum(total_funds_requested),
                       'percentageOfKilledFundsRequested':sum(killed_funds_requested)/sum(total_funds_requested)}
    
    return({'fractionOfSupplyForVoting':fractionOfSupplyForVoting, 
            'fractionOfSupplyInPool':fractionOfSupplyInPool,
            'fractionOfProposalStages':proposal_stages,
            'fractionOfFundStages':money_stages
           })
    
# Mechanisms 
def kpi_fractionOfSupplyForVoting(params, step, sL, s, _input):
    '''
    '''
    
    key = 'fractionOfSupplyForVoting'
    value = _input['fractionOfSupplyForVoting']
    
    return (key, value)


def kpi_fractionOfSupplyInPool(params, step, sL, s, _input):
    '''
    '''
    
    key = 'fractionOfSupplyInPool'
    value = _input['fractionOfSupplyInPool']
    
    return (key, value)

def kpi_proposal_stages(params, step, sL, s, _input):
    '''
    '''
    
    key = 'fractionOfProposalStages'
    value = _input['fractionOfProposalStages']
    
    return (key, value)


def kpi_fractionOfFundStages(params, step, sL, s, _input):
    '''
    '''
    
    key = 'fractionOfFundStages'
    value = _input['fractionOfFundStages']
    
    return (key, value)