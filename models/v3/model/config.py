import math
from decimal import Decimal
from datetime import timedelta
import numpy as np
from typing import Dict, List

from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import bound_norm_random, ep_time_step, config_sim, access_block
from copy import deepcopy
from cadCAD import configs
from .state_variables import state_variables
from .partial_state_update_block import partial_state_update_blocks
from .parts.sys_params import * 
from .parts.utils import * 


sim_config = config_sim({
    'T': range(100), #day 
    'N': 1,
    'M': params,
})

seeds = {
    'p': np.random.RandomState(1),
}

exp = Experiment()

exp.append_configs(
    sim_configs=sim_config,
    initial_state=state_variables,
    seeds=seeds,
    partial_state_update_blocks=partial_state_update_blocks
)

# Initialize network x
config_initialization(configs,initial_values)


def get_configs():
    '''
    Function to extract the configuration information for display in a notebook.
    '''

        
    return sim_config,state_variables,partial_state_update_blocks
