import numpy as np

# Initial values
initial_values = {
    'initial_sentiment': 0.6,
    'n': 30, #initial participants
    'm': 7, #initial proposals
    'initial_funds': 4867.21, # in honey, as of 8-5-2020
    'supply': 22392.22, # Honey total supply balance as of 8-5-2020  
}

# Parameters
params = {
    'beta': [0.2], # maximum share of funds a proposal can take
    'rho': [0.0025], # tuning param for the trigger function
    'alpha': [0.875], # timescale set in days with 3 day halflife (from comments in contract comments)
    'gamma': [0.001], # expansion of supply per per day
    'sensitivity': [.75],
    'tmin': [0], #unit days; minimum periods passed before a proposal can pass
    'min_supp': [1], #number of tokens that must be stake for a proposal to be a candidate
    'base_completion_rate': [45],
    'base_failure_rate': [180],
    'base_engagement_rate' :[0.3],
    'lowest_affinity_to_support': [0.3],
}