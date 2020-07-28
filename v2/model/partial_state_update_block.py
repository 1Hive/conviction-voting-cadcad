from .model.system import *
from .model.participants import *
from .model.proposals import *

# The Partial State Update Blocks
partial_state_update_blocks = [
    { 
        # system.py: 
        'policies': { 
            'random': driving_process
        },
        'variables': {
            'network': update_network,
            'funds':increment_funds,
        }
    },
    {
      # participants.py   
      'policies': {
          'completion': check_progress 
        },
        'variables': { 
            'sentiment': update_sentiment_on_completion, #note completing decays sentiment, completing bumps it
            'network': complete_proposal
        }
    },
        {
      # proposals.py
      'policies': {
          'release': trigger_function 
        },
        'variables': { 
            'funds': decrement_funds, 
            'sentiment': update_sentiment_on_release, #releasing funds can bump sentiment
            'network': update_proposals 
        }
    },
    { 
        # participants.py
        'policies': { 
            'participants_act': participants_decisions
        },
        'variables': {
            'network': update_tokens 
        }
    }
]