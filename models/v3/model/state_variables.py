from .parts.utils import * 
from .parts.sys_params import *
import networkx as nx

# copy of this structure called state_scheme.py with the name of the class. 
# add utility for checking state. Tell you what fails. Dictionary with key if true/false.
# use https://pydantic-docs.helpmanual.io/? and then flow into pytest. # run type check at the end of the
# simulation before the results. 
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
