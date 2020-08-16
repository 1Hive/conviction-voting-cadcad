from .parts.system import *
from .parts.participants import *
from .parts.proposals import *
from .parts.metrics import *

# The Partial State Update Blocks
partial_state_update_blocks = [
    { 
        # system.py: 
        'policies': { 
            'random': driving_process
        },
        'variables': {
            'network': update_network,
            'effective_supply': increment_supply,
        }
     },
     {
        'policies': { 
            'random': minting_rule
        },
        'variables': {
            'total_supply': mint_to_supply,
            'funds':mint_to_funds,

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
    },
    {
        # metrics.py
        'policies': {
            'calculations': kpi_calculations
        },
        'variables':{
            'fractionOfSupplyForVoting': kpi_fractionOfSupplyForVoting,
            'fractionOfSupplyInPool': kpi_fractionOfSupplyInPool,
            'fractionOfProposalStages':kpi_proposal_stages,
            'fractionOfFundStages': kpi_fractionOfFundStages
        }
    }
            
]

            
 