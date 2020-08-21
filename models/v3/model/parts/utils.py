import networkx as nx
from scipy.stats import expon, gamma
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import seaborn as sns
from copy import deepcopy
#from cadCAD import configs


def trigger_threshold(requested, funds, supply, alpha, params):
    '''
    Function that determines threshold for proposals being accepted. 
    '''

    share = requested/funds
    if share < params['beta']:
        threshold = params['rho']*supply/(params['beta']-share)**2  * 1/(1-alpha)
        return threshold 
    else: 
        return np.inf

def initial_social_network(network, scale = 1, sigmas=3):
    '''
    Function to initialize network x social network edges
    '''
    participants = get_nodes_by_type(network, 'participant')
    
    for i in participants:
        for j in participants:
            if not(j==i):
                influence_rv = expon.rvs(loc=0.0, scale=scale)
                if influence_rv > scale+sigmas*scale**2:
                    network.add_edge(i,j)
                    network.edges[(i,j)]['influence'] = influence_rv
                    network.edges[(i,j)]['type'] = 'influence'
    return network
                    
def initial_conflict_network(network, rate = .25):
    '''
    Definition:
    Function to initialize network x conflict edges
    '''
    proposals = get_nodes_by_type(network, 'proposal')
    
    for i in proposals:
        for j in proposals:
            if not(j==i):
                conflict_rv = np.random.rand()
                if conflict_rv < rate :
                    network.add_edge(i,j)
                    network.edges[(i,j)]['conflict'] = 1-conflict_rv
                    network.edges[(i,j)]['type'] = 'conflict'
    return network

def gen_new_participant(network, new_participant_holdings):
    '''
    Definition:
    Driving processes for the  arrival of participants.

    Parameters:
    network: networkx object
    new_participant_holdings: Tokens of new participants

    Assumptions:
    Initialized network x object

    Returns:
    Update network x object
    '''
    
    i = len([node for node in network.nodes])
    
    network.add_node(i)
    network.nodes[i]['type']="participant"
    
    s_rv = np.random.rand() 
    network.nodes[i]['sentiment'] = s_rv
    network.nodes[i]['holdings']=new_participant_holdings
    
    for j in get_nodes_by_type(network, 'proposal'):
        network.add_edge(i, j)
        
        a_rv = a_rv = np.random.uniform(-1,1,1)[0]
        network.edges[(i, j)]['affinity'] = a_rv
        network.edges[(i,j)]['tokens'] = 0 #a_rv*network.nodes[i]['holdings']
        network.edges[(i, j)]['conviction'] = 0
        network.edges[(i,j)]['type'] = 'support'
    
    return network
    



def gen_new_proposal(network, funds, supply, funds_requested,params):
    '''
    Definition:
    Driving processes for the arrival of proposals.

    Parameters:
    network: networkx object
    funds: 
    supply:

    Assumptions:
    Initialized network x object

    Returns:
    Update network x object
    '''
    j = len([node for node in network.nodes])
    network.add_node(j)
    network.nodes[j]['type']="proposal"
    
    network.nodes[j]['conviction']=0
    network.nodes[j]['status']='candidate'
    network.nodes[j]['age']=0
    
    network.nodes[j]['funds_requested'] =funds_requested
    
    network.nodes[j]['trigger']= trigger_threshold(funds_requested, funds, supply, params['alpha'],params)
    
    participants = get_nodes_by_type(network, 'participant')
    proposing_participant = np.random.choice(participants)
    
    for i in participants:
        network.add_edge(i, j)
        if i==proposing_participant:
            network.edges[(i, j)]['affinity']=1
        else:
            a_rv = np.random.uniform(-1,1,1)[0]
            network.edges[(i, j)]['affinity'] = a_rv
            
        network.edges[(i, j)]['conviction'] = 0
        network.edges[(i,j)]['tokens'] = 0
        network.edges[(i,j)]['type'] = 'support'
        
    return network
        

def get_nodes_by_type(g, node_type_selection):
    '''
    Definition:
    Function to extract nodes based by named type

    Parameters:
    g: network x object
    node_type_selection: node type

    Assumptions:

    Returns:
    List column of the desired information as:

    Example:
    proposals = get_nodes_by_type(network, 'proposal')

    '''
    return [node for node in g.nodes if g.nodes[node]['type']== node_type_selection ]

def get_sentimental(sentiment, force, decay=.1):
    '''
    '''
    mu = decay
    sentiment = sentiment*(1-mu) + force*mu
    
    if sentiment > 1:
        sentiment = 1
    elif sentiment < 0:
        sentiment = 0
        
    return sentiment

def get_edges_by_type(g, edge_type_selection):
    '''
    Functions to extract edges based on type
    '''
    return [edge for edge in g.edges if g.edges[edge]['type']== edge_type_selection ]


def conviction_order(network, proposals):
    '''
    Function to sort conviction order
    '''
    ordered = sorted(proposals, key=lambda j:network.nodes[j]['conviction'] , reverse=True)
    
    return ordered
    


def social_links(network, participant, scale = 1):
    '''
    ''' 
    participants = get_nodes_by_type(network, 'participant')
    
    i = participant
    for j in participants:
        if not(j==i):
            influence_rv = expon.rvs(loc=0.0, scale=scale)
            if influence_rv > scale+scale**2:
                network.add_edge(i,j)
                network.edges[(i,j)]['influence'] = influence_rv
                network.edges[(i,j)]['type'] = 'influence'
    return network


def conflict_links(network,proposal ,rate = .25):
    '''
    '''
    proposals = get_nodes_by_type(network, 'proposal')
    
    i = proposal
    for j in proposals:
        if not(j==i):
            conflict_rv = np.random.rand()
            if conflict_rv < rate :
                network.add_edge(i,j)
                network.edges[(i,j)]['conflict'] = 1-conflict_rv
                network.edges[(i,j)]['type'] = 'conflict'
    return network

def social_affinity_booster(network, proposal, participant):
    '''
    '''
    participants = get_nodes_by_type(network, 'participant')
    influencers = get_edges_by_type(network, 'influence')
    
    j=proposal
    i=participant
    
    i_tokens = network.nodes[i]['holdings']
   
    influence = np.array([network.edges[(i,node)]['influence'] for node in participants if (i, node) in influencers ])
    tokens = np.array([network.edges[(node,j)]['tokens'] for node in participants if (i, node) in influencers ])    
    
    influence_sum = np.sum(influence)
    
    if influence_sum>0:
        boosts = np.sum(tokens*influence)/(influence_sum*i_tokens)
    else:
        boosts = 0
    
    return np.sum(boosts)
    

def snap_plot(nets, size_scale = 1/10, dims = (10,10), savefigs=False):
    '''
    '''

    last_net = nets[-1]
        
    last_props=get_nodes_by_type(last_net, 'proposal')
    M = len(last_props)
    last_parts=get_nodes_by_type(last_net, 'participant')
    N = len(last_parts)
    pos = {}
    
    for ind in range(N):
        i = last_parts[ind] 
        pos[i] = np.array([0, 2*ind-N])

    for ind in range(M):
        j = last_props[ind] 
        pos[j] = np.array([1, 2*N/M *ind-N])

    
    if savefigs:
        counter = 0
        length = 10

    for net in nets:
        edges = get_edges_by_type(net, 'support')
        max_tok = np.max([net.edges[e]['tokens'] for e in edges])

        E = len(edges)
        
        net_props = get_nodes_by_type(net, 'proposal')
        net_parts = get_nodes_by_type(net, 'participant')
        net_node_label ={}
        
        num_nodes = len([node for node in net.nodes])
        
        node_color = np.empty((num_nodes,4))
        node_size = np.empty(num_nodes)

        edge_color = np.empty((E,4))
        cm = plt.get_cmap('Reds')

        cNorm  = colors.Normalize(vmin=0, vmax=max_tok)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    
        net_cand = [j for j in net_props if net.nodes[j]['status']=='candidate']

        for j in net_props:
            node_size[j] = net.nodes[j]['funds_requested']*size_scale
            if net.nodes[j]['status']=="candidate":
                node_color[j] = colors.to_rgba('blue')
                trigger = net.nodes[j]['trigger']      
                conviction = net.nodes[j]['conviction']
                percent_of_trigger = "          "+str(int(100*conviction/trigger))+'%'
                net_node_label[j] = str(percent_of_trigger)
            elif net.nodes[j]['status']=="active":
                node_color[j] = colors.to_rgba('orange')
                net_node_label[j] = ''
            elif net.nodes[j]['status']=="completed":
                node_color[j] = colors.to_rgba('green')
                net_node_label[j] = ''
            elif net.nodes[j]['status']=="failed":
                node_color[j] = colors.to_rgba('gray')
                net_node_label[j] = ''
            elif net.nodes[j]['status']=="killed":
                node_color[j] = colors.to_rgba('black')
                net_node_label[j] = ''

        for i in net_parts:    
            node_size[i] = net.nodes[i]['holdings']*size_scale/10
            node_color[i] = colors.to_rgba('red')
            net_node_label[i] = ''

        included_edges = []
        for ind in range(E):
            e = edges[ind]
            tokens = net.edges[e]['tokens']
            edge_color[ind] = scalarMap.to_rgba(tokens)
            if e[1] in net_cand:
                included_edges.append(e)
            

        iE = len(included_edges)
        included_edge_color = np.empty((iE,4))
        for ind in range(iE):
            e = included_edges[ind]
            tokens = net.edges[e]['tokens']
            included_edge_color[ind] = scalarMap.to_rgba(tokens)
        
    
            
        else:
            plt.figure(figsize=dims)
            nx.draw(net,
                pos=pos, 
                node_size = node_size,
                node_color = node_color, 
                edge_color = included_edge_color, 
                edgelist=included_edges,
                labels = net_node_label)
            plt.title('Tokens Staked by Partipants to Proposals')
            plt.tight_layout()
            plt.axis('on')
            plt.xticks([])
            plt.yticks([])
            if savefigs:
                plt.savefig('images/snap/'+str(counter)+'.png',bbox_inches='tight')

                counter = counter+1
            plt.show()

def pad(vec, length,fill=True):
    '''
    '''
    
    if fill:
        padded = np.zeros(length,)
    else:
        padded = np.empty(length,)
        padded[:] = np.nan
        
    for i in range(len(vec)):
        padded[i]= vec[i]
        
    return padded

def make2D(key, data, fill=False):
    '''
    '''
    maxL = data[key].apply(len).max()
    newkey = 'padded_'+key
    data[newkey] = data[key].apply(lambda x: pad(x,maxL,fill))
    reshaped = np.array([a for a in data[newkey].values])
    
    return reshaped



def affinities_plot(network, dims = (20, 5)):
    '''
    '''

        
    last_props=get_nodes_by_type(network, 'proposal')
    M = len(last_props)
    last_parts=get_nodes_by_type(network, 'participant')
    N = len(last_parts)

    affinities = np.empty((N,M))
    for i_ind in range(N):
        for j_ind in range(M):
            i = last_parts[i_ind]
            j = last_props[j_ind]
            affinities[i_ind][j_ind] = network.edges[(i,j)]['affinity']

    fig, ax = plt.subplots(figsize=dims)

    sns.heatmap(affinities.T,
                xticklabels=last_parts,
                yticklabels=last_props,
                square=True,
                cbar=True,
                cmap = plt.cm.RdYlGn,
                ax=ax)

    plt.title('affinities between participants and proposals')
    plt.ylabel('proposal_id')
    plt.xlabel('participant_id')




def trigger_sweep(field, trigger_func,params,supply=10**9, x_extra=.001):
    '''
    '''
    rho = params['rho'][0]
    beta = params['beta'][0]
    xmax=beta- np.sqrt(rho)
    alpha = params['alpha'][0]

    if field == 'effective_supply':
        share_of_funds = np.arange(0,xmax*(1+x_extra),.001)
        total_supply = np.arange(0,supply*10, supply/100) 
        demo_data_XY = np.outer(share_of_funds,total_supply)

        demo_data_Z0=np.empty(demo_data_XY.shape)
        demo_data_Z1=np.empty(demo_data_XY.shape)
        demo_data_Z2=np.empty(demo_data_XY.shape)
        demo_data_Z3=np.empty(demo_data_XY.shape)
        for sof_ind in range(len(share_of_funds)):
            sof = share_of_funds[sof_ind]
            for ts_ind in range(len(total_supply)):
                ts = total_supply[ts_ind]
                tc = ts /(1-alpha)
                trigger = trigger_func(sof, 1, ts, alpha,beta, rho) 
                demo_data_Z0[sof_ind,ts_ind] = np.log10(trigger)
                demo_data_Z1[sof_ind,ts_ind] = trigger
                demo_data_Z2[sof_ind,ts_ind] = trigger/tc #share of maximum possible conviction
                demo_data_Z3[sof_ind,ts_ind] = np.log10(trigger/tc)
        return {'log10_trigger':demo_data_Z0,
                'trigger':demo_data_Z1,
                'share_of_max_conv': demo_data_Z2,
                'log10_share_of_max_conv':demo_data_Z3,
                'total_supply':total_supply,
                'share_of_funds':share_of_funds,
                'alpha':alpha}
    elif field == 'alpha':
        #note if alpha >.01 then this will give weird results max alpha will be >1
        alpha = np.arange(0,1,.001)
        share_of_funds = np.arange(0,xmax*(1+x_extra),.001)
        demo_data_XY = np.outer(share_of_funds,alpha)

        demo_data_Z4=np.empty(demo_data_XY.shape)
        demo_data_Z5=np.empty(demo_data_XY.shape)
        demo_data_Z6=np.empty(demo_data_XY.shape)
        demo_data_Z7=np.empty(demo_data_XY.shape)
        for sof_ind in range(len(share_of_funds)):
            sof = share_of_funds[sof_ind]
            for a_ind in range(len(alpha)):
                ts = supply
                a = alpha[a_ind]
                tc = ts /(1-a)
                trigger = trigger_func(sof, 1, ts, a, beta, rho)
                demo_data_Z4[sof_ind,a_ind] = np.log10(trigger)
                demo_data_Z5[sof_ind,a_ind] = trigger
                demo_data_Z6[sof_ind,a_ind] = trigger/tc #share of maximum possible conviction
                demo_data_Z7[sof_ind,a_ind] = np.log10(trigger/tc)
        
        return {'log10_trigger':demo_data_Z4,
               'trigger':demo_data_Z5,
               'share_of_max_conv': demo_data_Z6,
               'log10_share_of_max_conv':demo_data_Z7,
               'alpha':alpha,
               'share_of_funds':share_of_funds,
               'supply':supply}
        
    else:
        return "invalid field"
    
def trigger_plotter(share_of_funds,Z, color_label,y, ylabel,cmap='jet'):
    '''
    '''
    dims = (10, 5)
    fig, ax = plt.subplots(figsize=dims)

    cf = plt.contourf(share_of_funds, y, Z.T, 100, cmap=cmap)
    cbar=plt.colorbar(cf)
    plt.axis([share_of_funds[0], share_of_funds[-1], y[0], y[-1]])
    #ax.set_xscale('log')
    plt.ylabel(ylabel)
    plt.xlabel('Share of Funds Requested')
    plt.title('Trigger Function Map')

    cbar.ax.set_ylabel(color_label)
    
def trigger_grid(supply_sweep, alpha_sweep):
    
    fig, axs = plt.subplots(nrows=2, ncols=1,figsize=(20,20))
    axs = axs.flatten()

    share_of_funds = alpha_sweep['share_of_funds']
    Z = alpha_sweep['share_of_max_conv']
    y = alpha_sweep['alpha']
    ylabel = 'alpha'
    supply = alpha_sweep['supply']

    cp0=axs[0].contourf(share_of_funds, y, Z.T,100, cmap='jet', )
    axs[0].axis([share_of_funds[0], share_of_funds[-1], y[0], y[-1]])
    axs[0].set_ylabel(ylabel)
    axs[0].set_xlabel('Share of Funds Requested')
    axs[0].set_xticks(np.arange(0,.175,.025))
    axs[0].set_title('Trigger Function Map - Alpha sweep; Supply ='+str(supply))
    cb0=plt.colorbar(cp0, ax=axs[0],ticks=np.arange(0,1.1,.1))
    cb0.set_label('share of max conviction to trigger')

    
    share_of_funds = supply_sweep['share_of_funds']
    Z = supply_sweep['share_of_max_conv']
    y = supply_sweep['total_supply']
    ylabel = 'Effective Supply'
    alpha = supply_sweep['alpha']

    #max_conv = y/(1-alpha)

    cp1=axs[1].contourf(share_of_funds, y, Z.T,100, cmap='jet', )
    axs[1].axis([share_of_funds[0], share_of_funds[-1], y[0], y[-1]])
    axs[1].set_ylabel(ylabel)
    axs[1].set_xlabel('Share of Funds Requested')
    axs[1].set_xticks(np.arange(0,.175,.025))
    axs[1].set_title('Trigger Function Map - Supply sweep; alpha='+str(alpha))
    #axs[1].set_label('log10 of conviction to trigger')
    cb1=plt.colorbar(cp1, ax=axs[1], ticks=np.arange(0,1.1,.1))
    cb1.set_label('share of max conviction to trigger')


def initialize_network(n,m, initial_funds, supply, params):
    '''
    Definition:
    Function to initialize network x object

    Parameters:

    Assumptions:

    Returns:

    Example:
    '''
    # initilize network x graph
    network = nx.DiGraph()
    # create participant nodes with type and token holding
    for i in range(n):
        network.add_node(i)
        network.nodes[i]['type']= "participant"
        
        h_rv = expon.rvs(loc=0.0, scale= supply/n)
        network.nodes[i]['holdings'] = h_rv 
        
        s_rv = np.random.rand() 
        network.nodes[i]['sentiment'] = s_rv
    
    participants = get_nodes_by_type(network, 'participant')
    initial_supply = np.sum([ network.nodes[i]['holdings'] for i in participants])
       
    
    # Generate initial proposals
    for ind in range(m):
        j = n+ind
        network.add_node(j)
        network.nodes[j]['type']="proposal"
        network.nodes[j]['conviction'] = 0
        network.nodes[j]['status'] = 'candidate'
        network.nodes[j]['age'] = 0
        
        # This is a gamma random variable (wikipedia link) - scipy link
        r_rv = gamma.rvs(3,loc=0.001, scale=(initial_funds * params['beta'])*.05)
        network.nodes[j]['funds_requested'] = r_rv
        
        network.nodes[j]['trigger']= trigger_threshold(r_rv, initial_funds, initial_supply, params['alpha'],params)
        
        for i in range(n):
            network.add_edge(i, j)
            
            rv = np.random.rand()
            a_rv = np.random.uniform(-1,1,1)[0]
            network.edges[(i, j)]['affinity'] = a_rv
            network.edges[(i, j)]['tokens'] = 0
            network.edges[(i, j)]['conviction'] = 0
            network.edges[(i, j)]['type'] = 'support'
            
        proposals = get_nodes_by_type(network, 'proposal')
        total_requested = np.sum([ network.nodes[i]['funds_requested'] for i in proposals])
        
        network = initial_conflict_network(network, rate = .25)
        network = initial_social_network(network, scale = 1)
        
    return network


def config_initialization(configs,initial_values):
    '''
    from copy import deepcopy
    from cadCAD import configs
    '''
    # Initialize network x
    for c in configs:
        c.initial_state = deepcopy(c.initial_state)

        print("Params (config.py) : ", c.sim_config['M'])

        c.initial_state['network'] = initialize_network(initial_values['n'],initial_values['m'],
                                                initial_values['funds'],
                                                initial_values['supply'],c.sim_config['M'])
        
        return c.initial_state['network']