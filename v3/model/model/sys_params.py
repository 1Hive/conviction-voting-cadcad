import numpy as np

# Initial values
initial_values = {
    'initial_sentiment': 0.6,
    'n': 30, #initial participants
    'm': 7, #initial proposals
    'initial_funds': 4867.21, # in honey, as of 8-5-2020
    'supply': 22392.22, # Honey supply balance as of 8-5-2020  
}

# Parameters
sys_params = {
    'beta': 0.2, # maximum share of funds a proposal can take
    'rho': 0.0025, # tuning param for the trigger function
    'alpha': 1/2**3, # timescale set in days with 3 day halflife (from comments in contract comments)
    'sensitivity': .75,
    'tmin': 0, #unit days; minimum periods passed before a proposal can pass
    'min_supp': 1, #number of tokens that must be stake for a proposal to be a candidate
    'base_completion_rate': 45,
    'base_failure_rate': 180,
}