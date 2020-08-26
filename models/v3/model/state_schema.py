from .parts.utils import * 
from .parts.sys_params import *
import networkx as nx
import numpy as np

# Schema check for testing simulation results
state_schema = { 
                'network': nx.DiGraph(), 
                'funds': np.float64(),
                'sentiment': np.float64(),
                'effective_supply': np.float64(), 
                'total_supply': np.float64(),
                # metrics variables
                'fractionOfSupplyForVoting': np.float64(),
                'fractionOfSupplyInPool': np.float64(),
                'fractionOfProposalStages': dict(),
                'fractionOfFundStages': dict()

}
