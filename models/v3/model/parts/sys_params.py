import numpy as np

# Initial values
initial_values = {
    'sentiment': 0.6,
    'n': 30, #initial participants
    'm': 7, #initial proposals
    'funds': 4867.21, # in honey, as of 8-5-2020
    'supply': 22392.22, # Honey total supply balance as of 8-5-2020  
}


# Alpha from solidity code - uint256 _decay = 9999599; // 3 days halftime. halftime_alpha = (1/2)**(1/t)
# Half life associated with solidity code alpha (in number of blocks on xDai). 
# Our simulation is associated with timesteps, so our half life is based of of days.
# Parameters
params = {
    'beta': [0.2], # maximum share of funds a proposal can take
    'rho': [0.0025], # tuning param for the trigger function
    'alpha': [2**(-1/3)], # timescale set in days with 3 day halflife (see above)
    'gamma': [0.001], # expansion of supply per per day
    'sensitivity': [.75],
    'tmin': [1], #unit days; minimum periods passed before a proposal can pass
    'min_supp': [1], #number of tokens that must be stake for a proposal to be a candidate
    'base_completion_rate': [45], # expected number of days to complete a proposals.
    'base_failure_rate': [180], # expected number of days until a proposal will fail
    'base_engagement_rate' :[0.3], # Probability of being active on a certain day if 100% sentiment 
    'lowest_affinity_to_support': [0.3], # lowest affinity to required to support a proposal
}

