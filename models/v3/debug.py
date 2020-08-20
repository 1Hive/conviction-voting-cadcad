from model import config
from model.parts.sys_params import initial_values
from model.parts.utils import *

import numpy as np
import pandas as pd
from model import run
pd.options.display.float_format = '{:.2f}'.format

# %matplotlib inline

rdf = run.run()