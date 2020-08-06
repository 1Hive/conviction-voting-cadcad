from .model.conviction_helper_functions import * 
from .model.sys_params import *

genesis_states = { 
                'network':initialize_network(initial_values['n'],initial_values['m'],
                                            initial_values['initial_funds'],
                                            initial_values['supply']),
                'funds':initial_values['initial_funds'],
                'sentiment': initial_values['initial_sentiment'],
                'effective_supply': initial_values['supply'],
                'funds_arrival': 0

}
