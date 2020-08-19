from .parts.utils import * 
from .parts.sys_params import *

state_variables = { 
                'network': initialize_network(initial_values['n'],initial_values['m'],
                                            initial_values['funds'],
                                            initial_values['supply'],initial_values['params']),
                'funds':initial_values['funds'],
                'sentiment': initial_values['sentiment'],
                'effective_supply': (initial_values['supply']-initial_values['funds'])*.8, 
                'total_supply': initial_values['supply'],
                # metrics variables
                'fractionOfSupplyForVoting': 0,
                'fractionOfSupplyInPool': 0,
                'fractionOfProposalStages': 0,
                'fractionOfFundStages': 0

}
