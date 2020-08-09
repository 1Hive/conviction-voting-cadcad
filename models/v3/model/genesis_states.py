from .model.conviction_helper_functions import * 
from .model.sys_params import *

# current hack until sim_config
initial_params = {
    'beta': 0.2, # maximum share of funds a proposal can take
    'rho': 0.0025, # tuning param for the trigger function
    'alpha': 0.875, # timescale set in days with 3 day halflife (from comments in contract comments)
}
genesis_states = { 
                'network':initialize_network(initial_values['n'],initial_values['m'],
                                            initial_values['initial_funds'],
                                            initial_values['supply'],initial_params),
                'funds':initial_values['initial_funds'],
                'sentiment': initial_values['initial_sentiment'],
                'effective_supply': (initial_values['supply']-initial_values['initial_funds'])*.8, #force some slack into the inequality
                'total_supply': initial_values['supply']

}
