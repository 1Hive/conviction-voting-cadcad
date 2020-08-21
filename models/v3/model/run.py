import pandas as pd
from .parts.utils import * 
from model import config 
from cadCAD.engine import ExecutionMode, ExecutionContext,Executor
from cadCAD import configs

def run():
    '''
    Definition:
    Run simulation
    '''
    # Single
    exec_mode = ExecutionMode()
    local_mode_ctx = ExecutionContext(context=exec_mode.local_mode)

    simulation = Executor(exec_context=local_mode_ctx, configs=configs)
    raw_system_events, tensor_field, sessions = simulation.execute()
    # Result System Events DataFrame
    df = pd.DataFrame(raw_system_events)

    return df



def postprocessing(df, sim_ind=-1):
    '''
    Function for postprocessing the simulation results to extract key information from the network object. 
    '''
    # subset to last substep of each simulation
    df= df[df.substep==df.substep.max()]

    sim_count = df.simulation.max()
    if sim_ind <0:
        sim_ind = sim_count+1+sim_ind

    df=df[df.simulation==sim_ind]

    # Extract information from dataframe
    df['conviction'] = df.network.apply(lambda g: np.array([g.nodes[j]['conviction'] for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='candidate']))
    df['participant_count'] = df.network.apply(lambda g: len([j for j in get_nodes_by_type(g, 'participant') if g.nodes[j]['type']=='participant']))
    df['candidate_count'] = df.network.apply(lambda g: len([j for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='candidate']))
    df['candidate_funds'] = df.network.apply(lambda g: np.sum([g.nodes[j]['funds_requested'] for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='candidate']))
    df['killed_count'] = df.network.apply(lambda g: len([j for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='killed']))
    df['killed_funds'] = df.network.apply(lambda g: np.sum([g.nodes[j]['funds_requested'] for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='killed']))
    df['candidate_funds_requested'] = df.network.apply(lambda g: np.array([g.nodes[j]['funds_requested'] for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='candidate']))
    df['active_count'] = df.network.apply(lambda g: len([j for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='active']))
    df['active_funds'] = df.network.apply(lambda g: np.sum([g.nodes[j]['funds_requested'] for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='active']))
    df['failed_count'] = df.network.apply(lambda g: len([j for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='failed']))
    df['failed_funds'] = df.network.apply(lambda g: np.sum([g.nodes[j]['funds_requested'] for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='failed']))
    df['completed_count'] = df.network.apply(lambda g: len([j for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='completed']))
    df['completed_funds'] = df.network.apply(lambda g: np.sum([g.nodes[j]['funds_requested'] for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='completed']))

    df['funds_requested'] = df.network.apply(lambda g: np.array([g.nodes[j]['funds_requested'] for j in get_nodes_by_type(g, 'proposal')]))
    df['share_of_funds_requested'] = df.candidate_funds_requested/df.funds

    df['share_of_funds_requested_all'] = df.funds_requested/df.funds

    df['triggers'] = df.network.apply(lambda g: np.array([g.nodes[j]['trigger'] for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='candidate' ]))
    df['conviction_share_of_trigger'] = df.conviction/df.triggers
    df['age'] = df.network.apply(lambda g: np.array([g.nodes[j]['age'] for j in get_nodes_by_type(g, 'proposal') if g.nodes[j]['status']=='candidate' ]))

    df['age_all'] = df.network.apply(lambda g: np.array([g.nodes[j]['age'] for j in get_nodes_by_type(g, 'proposal') ]))
    df['conviction_all'] = df.network.apply(lambda g: np.array([g.nodes[j]['conviction'] for j in get_nodes_by_type(g, 'proposal') ]))
    df['triggers_all'] = df.network.apply(lambda g: np.array([g.nodes[j]['trigger'] for j in get_nodes_by_type(g, 'proposal')  ]))

    df['conviction_share_of_trigger_all'] = df.conviction_all/df.triggers_all
    
    # extract metrics
    percentageOfActive = []
    percentageOfCompleted = []
    percentageOfKilled = []
    for i in range(0,len(df.timestep)):
        percentageOfActive.append(df.fractionOfProposalStages.values[i]['percentageOfActive'])
        percentageOfCompleted.append(df.fractionOfProposalStages.values[i]['percentageOfCompleted'])
        percentageOfKilled.append(df.fractionOfProposalStages.values[i]['percentageOfKilled'])

    df['percentageOfActiveProposals'] = percentageOfActive
    df['percentageOfCompletedProposals'] = percentageOfCompleted
    df['percentageOfKilledProposals'] = percentageOfKilled

    percentageOfActiveFundsRequested = []
    percentageOfCompletedFundsRequested = []
    percentageOfKilledFundsRequested = []
    for i in range(0,len(df.timestep)):
        percentageOfActiveFundsRequested.append(df.fractionOfFundStages.values[i]['percentageOfActiveFundsRequested'])
        percentageOfCompletedFundsRequested.append(df.fractionOfFundStages.values[i]['percentageOfCompletedFundsRequested'])
        percentageOfKilledFundsRequested.append(df.fractionOfFundStages.values[i]['percentageOfKilledFundsRequested'])

    df['percentageOfActiveFundsRequested'] = percentageOfActiveFundsRequested
    df['percentageOfCompletedFundsRequested'] = percentageOfCompletedFundsRequested
    df['percentageOfKilledFundsRequested'] = percentageOfKilledFundsRequested

    return df