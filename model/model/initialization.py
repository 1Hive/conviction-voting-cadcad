
# import libraries
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from .conviction_helper_functions import * 

# Parameters
# maximum share of funds a proposal can take
beta = .2 #later we should set this to be param so we can sweep it
# tuning param for the trigger function
rho = .001
supply = 1231286.81



n= 60 #initial participants
m= 3 #initial proposals

initial_sentiment = .6

theta =.35
alpha = 0.5
sensitivity = .75
tmin = 7 #unit days; minimum periods passed before a proposal can pass
min_supp = 50 #number of tokens that must be stake for a proposal to be a candidate
sentiment_decay = .01 #termed mu in the state update function
base_completion_rate = 100
base_failure_rate = 200 
tax_rate = .02

initial_funds = 40781.42

def initialize_network(n,m, inital_funds, expected_supply = 10**6):
    '''
    Definition:
    Function to initialize network x object

    Parameters:

    Assumptions:

    Returns:

    Example:
    '''
    # initilize network x graph
    network = nx.DiGraph()
    # create participant nodes with type and token holding
    for i in range(n):
        network.add_node(i)
        network.nodes[i]['type']= "participant"
        
        h_rv = expon.rvs(loc=0.0, scale= expected_supply/n)
        network.nodes[i]['holdings'] = h_rv # SOL check
        
        # s_rv = np.random.rand() 
        # network.nodes[i]['sentiment'] = s_rv
    
    participants = get_nodes_by_type(network, 'participant')
    initial_supply = np.sum([ network.nodes[i]['holdings'] for i in participants])
       
    
    # Generate initial proposals
    for ind in range(m):
        j = n+ind
        network.add_node(j)
        network.nodes[j]['type']="proposal"
        network.nodes[j]['conviction'] = 0
        network.nodes[j]['status'] = 'candidate'
        network.nodes[j]['age'] = 0
        
        r_rv = gamma.rvs(3,loc=0.001, scale=10000)
        network.nodes[j]['funds_requested'] = r_rv
        
        network.nodes[j]['trigger']= trigger_threshold(r_rv, initial_funds, initial_supply,beta=beta,rho=rho)
        
        for i in range(n):
            network.add_edge(i, j)
            
            rv = np.random.rand()
            a_rv = 1-4*(1-rv)*rv #polarized distribution
            network.edges[(i, j)]['affinity'] = a_rv
            network.edges[(i, j)]['tokens'] = 0
            network.edges[(i, j)]['conviction'] = 0
            network.edges[(i, j)]['type'] = 'support'
            
        proposals = get_nodes_by_type(network, 'proposal')
        total_requested = np.sum([ network.nodes[i]['funds_requested'] for i in proposals])
        
        # network = initial_conflict_network(network, rate = .25)
        # network = initial_social_network(network, scale = 1)
        
    return network, initial_funds, initial_supply, total_requested
#initializers
network, initial_funds, initial_supply, total_requested = initialize_network(n,m,initial_funds)
