from .parts.utils import * 
from .parts.sys_params import *

state_variables = { 
                'network': 0, # will initialize during config.py
                'funds':initial_values['initial_funds'],
                'sentiment': initial_values['initial_sentiment'],
                'effective_supply': (initial_values['supply']-initial_values['initial_funds'])*.8, #force some slack into the inequality
                'total_supply': initial_values['supply']

}
