import networkx as nx
from scipy.stats import expon, gamma
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import seaborn as sns

default_beta = 0.2
default_rho = 0.02

def trigger_threshold(requested, funds, supply, beta = default_beta, rho = default_rho):
    '''
    Function that determines threshold for proposals being accepted. 
    '''
    share = requested/funds
    if share < beta:
        return rho*supply/(beta-share)**2
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
    #network.nodes[i]['sentiment'] = s_rv
    network.nodes[i]['holdings']=new_participant_holdings
    
    for j in get_nodes_by_type(network, 'proposal'):
        network.add_edge(i, j)
        
        rv = np.random.rand()
        a_rv = 1-4*(1-rv)*rv #polarized distribution
        network.edges[(i, j)]['affinity'] = a_rv
        network.edges[(i,j)]['tokens'] = a_rv*network.nodes[i]['holdings']
        network.edges[(i, j)]['conviction'] = 0
        network.edges[(i,j)]['type'] = 'support'
    
    return network
    



def gen_new_proposal(network, funds, supply, scale_factor = 1.0/100):
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
    
    rescale = funds*scale_factor
    r_rv = gamma.rvs(3,loc=0.001, scale=rescale)
    network.nodes[j]['funds_requested'] = r_rv
    
    network.nodes[j]['trigger']= trigger_threshold(r_rv, funds, supply)
    
    participants = get_nodes_by_type(network, 'participant')
    proposing_participant = np.random.choice(participants)
    
    for i in participants:
        network.add_edge(i, j)
        if i==proposing_participant:
            network.edges[(i, j)]['affinity']=1
        else:
            rv = np.random.rand()
            a_rv = 1-4*(1-rv)*rv #polarized distribution
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
    #print(influence)
    tokens = np.array([network.edges[(node,j)]['tokens'] for node in participants if (i, node) in influencers ])
    #print(tokens)
    
    
    influence_sum = np.sum(influence)
    
    if influence_sum>0:
        boosts = np.sum(tokens*influence)/(influence_sum*i_tokens)
    else:
        boosts = 0
    
    return np.sum(boosts)
    

def snap_plot(nets, size_scale = 1/500, ani = False, dims = (20,20), savefigs=False):
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
    
    if ani:
        figs = []
        fig, ax = plt.subplots(figsize=dims)
    
    if savefigs:
        counter = 0
        length = 10
        import string
        unique_id = ''.join([np.random.choice(list(string.ascii_letters + string.digits)) for _ in range(length)])
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
        
#        nx.draw(net,
#                pos=pos, 
#                node_size = node_size,
#                node_color = node_color, 
#                edge_color = included_edge_color, 
#                edgelist=included_edges,
#                labels = net_node_label)
#        plt.title('Tokens Staked by Partipants to Proposals')
        
        if ani:
            nx.draw(net,
                    pos=pos, 
                    node_size = node_size,
                    node_color = node_color, 
                    edge_color = included_edge_color, 
                    edgelist=included_edges,
                    labels = net_node_label, ax=ax)
            figs.append(fig)
            
        else:
            nx.draw(net,
                pos=pos, 
                node_size = node_size,
                node_color = node_color, 
                edge_color = included_edge_color, 
                edgelist=included_edges,
                labels = net_node_label)
            plt.title('Tokens Staked by Partipants to Proposals')
            if savefigs:
                plt.savefig(unique_id+'_fig'+str(counter)+'.png')
                counter = counter+1
            plt.show()
        
    if ani:
        False
        #anim = animation.ArtistAnimation(fig, , interval=50, blit=True, repeat_delay=1000)
        #plt.show()

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


def quantile_plot(xkey, ykey, dataframe, dq=.1, logy=False, return_df = False):
    '''
    '''
    qX = np.arange(0,1+dq,dq)
    
    data = dataframe[[xkey,ykey]].copy()
    
    qkeys = []
    for q in qX:
        qkey= 'quantile'+str(int(100*q))
        #print(qkey)
        data[qkey] = data[ykey].apply(lambda arr: np.quantile(arr,q) )
        #print(data[qkey].head())
        qkeys.append(qkey)
    
    data[[xkey]+qkeys].plot(x=xkey,  logy=logy)
        
    plt.title(ykey + " Quantile Plot" )
    plt.ylabel(ykey)
    labels = [str(int(100*q))+"$^{th}$ Percentile" for q in qX ]
    
    plt.legend(labels, ncol = 1,loc='center left', bbox_to_anchor=(1, .5))
    if return_df:
        return data

def affinities_plot(df):
    '''
    '''
    last_net= df.network.values[-1]
    last_props=get_nodes_by_type(last_net, 'proposal')
    M = len(last_props)
    last_parts=get_nodes_by_type(last_net, 'participant')
    N = len(last_parts)

    affinities = np.empty((N,M))
    for i_ind in range(N):
        for j_ind in range(M):
            i = last_parts[i_ind]
            j = last_props[j_ind]
            affinities[i_ind][j_ind] = last_net.edges[(i,j)]['affinity']

    dims = (20, 5)
    fig, ax = plt.subplots(figsize=dims)

    sns.heatmap(affinities.T,
                xticklabels=last_parts,
                yticklabels=last_props,
                square=True,
                cbar=True,
                ax=ax)

    plt.title('affinities between participants and proposals')
    plt.ylabel('proposal_id')
    plt.xlabel('participant_id')