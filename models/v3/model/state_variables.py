from .parts.utils import * 
from .parts.sys_params import *
import networkx as nx


state_variables = { 
                'network': nx.DiGraph(), # will initialize during config.py as a networkX object
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
