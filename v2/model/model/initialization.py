
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
#alpha = 1 - 0.9999599 #native timescale for app as in contract code
alpha = .5**3 #timescale set in days with 3 day halflife (from comments in contract comments)
supply = 21706 # Honey supply balance as of 7-17-2020  
initial_sentiment = .6


n= 24 #initial participants
m= 3 #initial proposals


sensitivity = .75
tmin = 7 #unit days; minimum periods passed before a proposal can pass
min_supp = 50 #number of tokens that must be stake for a proposal to be a candidate
# sentiment_decay = .01 #termed mu in the state update function
base_completion_rate = 100
base_failure_rate = 200 

initial_funds = 48000 # in xDai

network = initialize_network(n,m,initial_funds,supply)
