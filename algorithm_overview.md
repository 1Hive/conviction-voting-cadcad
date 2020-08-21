# Mathematically Formalizing the Conviction Voting Algorithm

## Background
---
Conviction Voting is an approach to organizing a communities preferences into discrete decisions in the management of that communities resources. Strictly speaking conviction voting is less like voting and more like signal processing. Framing the approach and the initial algorithm design was done by Michael Zargham and published in a short research proposal [Social Sensor Fusion](https://github.com/BlockScience/conviction/blob/master/social-sensorfusion.pdf). This work is based on a dynamic resource allocation algorithm presented in Dr. Zargham's PhD Thesis.

The work proceeded in collaboration with the Commons Stack, including expanding on the python implementation to makeup part of the Commons Simulator game. An implemention of Conviction Voting as a smart contract within the Aragon Framework was developed by [1Hive](https://1hive.org/) and is currently being used for community decision making around allocations their community currency, Honey.

## Defining the Word Problem
___

Suppose a group of people want to coordinate to make a collective decision. Social dynamics such as discussions, signaling, and even changing ones mind based on feedback from others input play an important role in these processes. While the actual decision making process involves a lot of informal processes, in order to be fair the ultimate decision making process still requires a set of formal rules that the community collecively agrees to, which serves to functionally channel a plurality of preferences into a discrete outcomes. In our case we are interested in a procedure which supports asynchronous interactions, an provides visibility into likely outcomes prior to their resolution to serve as a driver of good faith, debate and healthy forms of coalition building. Furthermore, participations should be able to show support for multiple initiatives, and to vary the level of support shown. Participants a quantity of signaling power which may be fixed or variable, homogenous or heterogenous. For the purpose of this document, we'll focus on the case where the discrete decisions to be made are decisions to allocate funds from a shared funding pool towards projects of interest to the community.

## Converting to a Math Problem
___

Let's start taking these words and constructing a mathematical representation that supports a design that meets the description above. To start we need to define participants.

### Defining the Participants

___

Let $\mathcal{A}$ be the set of participants. Consider a participant $a\in \mathcal{A}$. Any participant $a$ has some capacity to participate in the voting process $h[a]$. In a fixed quantity, homogenous system $h[a] = h$ for all $a\in \mathcal{A}$ where $h$ is a constant. The access control process managing how one becomes a participant determines the total supply of "votes" $S = \sum_{a\in \mathcal{A}} = n\cdot h$ where the number of participants is $n = |\mathcal{A}|$. In a smart contract setting, the set $\mathcal{A}$ is a set of addresses, and $h[a]$ is a quantity of tokens held by each address $a\in \mathcal{A}$.

### Defining Proposals & Shared Resources

___

Next, we introduce the idea of proposals.  Consider a proposal $i\in \mathcal{C}$. Any proposal $i$ is associated with a request for resources $r[i]$. Those requested resources would be allocated from a constrained pool of communal resources currently totaling $R$. The pool of resources may become depleted because when a proposal $i$ passes $R^+= R-r[i]$. Therefore it makes sense for us to consider what fraction of the shared resources are being request $\mu_i = \frac{r[i]}{R}$, which means that thre resource depletion from passing proposals can be bounded by requiring $\mu_i < \mu$ where $\mu$ is a constant representing the maximum fraction of the shared resources which can be dispersed by any one proposal. In order for the system to be sustainable a source of new resources is required. In the case where $R$ is funding, new funding can come from revenues, donations, or in some DAO use cases minting tokens.

### Defining Participants Preferences for Proposals

___

Most of the interesting information in this system is distributed amongst the participants and it manifests as preferences over the proposals. This can be thought of as a matrix $W\in \mathbb{R}^{n \times m}$.
![image of participant/proposal affinity matrix](https://i.imgur.com/vERr8Zv.png)

These private hidden signals drive discussions and voting actions. Each participant individually decides how to allocate their votes across the available proposals. Participant $a$ supports proposal $i$ by setting $x[a,i]>0$ but they are limited by their capacity $\sum_{k\in \mathcal{C}} x[a,k] \le h[a]$.  Assuming each participant chooses a subset of the proposals to support, a support graph is formed.
![pic](https://i.imgur.com/KRh8tKn.png)

## Aggregating Information

___

In order to break out of the synchronous ad-hoc voting model, a dynamical systems model of this system is introduced that fuses collective community preferences into a single signal. The mathematical derivation of this process can be found below.

### Participants Allocate Voting Power

___

![pic](https://i.imgur.com/DZRDwk6.png)
In the above diagram, we examine the participant view. Participant $a$ with holdings $h$ at time $t$ supports proposals $i$ and $j$ with $x$ conviction. The sum of all conviction asserted by participant $a$ is between 0 and the total holdings of participant $a$.

### System Accounting of Proposal Conviction

___

![pic](https://i.imgur.com/euAei5R.png)

In the above diagram, we examine the proposal view. Proposal $j$ with total conviction $y$ at time $t$ is supported by participants $a$, $b$ and $c$ with $x$ conviction. The total conviction $y$ at time $t+1$ is equal to the total conviction at time $t$ decremented by an exponential decay $\\alpha$ plus the sum of all conviction from $k$ agents in time step $t$.

### Understanding the Alpha Parameter
___
For a deeper exploration of the $alpha$ parameter, please read more in the [Deriving Alpha notebook](https://nbviewer.jupyter.org/github/BlockScience/Aragon_Conviction_Voting/blob/master/models/v3/Deriving_Alpha.ipynb)


## Converting Signals to Discrete Decisions
___

Conviction can be considered like a fluctuating kinetic energy, with the Trigger function acting as a required activation energy for proposals to pass. This is the mechanism by which a continuous community preference turns into a discrete action event: passing a proposal. See the [Trigger Function Explanation notebook](https://nbviewer.jupyter.org/github/BlockScience/Aragon_Conviction_Voting/blob/master/models/v3/Trigger_Function_Explanation.ipynb) for more details around the trigger function and how it works.

### The Trigger Function
___
For a deeper exploration of the trigger function, please read more in the [Trigger Function Explainer notebook](https://nbviewer.jupyter.org/github/BlockScience/Aragon_Conviction_Voting/blob/master/models/v3/Trigger_Function_Explanation.ipynb)


### Resolving Passed Proposals
___

![pic](https://i.imgur.com/lmOl9HE.png)

## Social Systems Modeling
___

In the conviction voting model, multiple graph structures are used to represent participants and proposals to represent a subjective, exploratory modeling of the social system interacting.

### Sentiment:

* Global Sentiment denotes the outside world appreciating the output of the community. 
* Local Sentiment denotes the agents within the system feeling good about output of the community. 
* Sentiment increases when proposals pass and work is completed in the community, and decreases when proposals fail and community progress stalls.

### Relationships between Participants:

* Edges from participant to participant denote influence (to represent subjective social influence) and are assigned randomly via mixing processes.

![Participant Influence Graph](https://i.imgur.com/zQziRA7.png)

### Relationships between Proposals

* Edges from proposal to proposal represent conflict, which can be positive or negative. 
* Some proposals are synergistic (passing one makes the other more desirable). 
* Some proposals are (partially) substitutable (passing one makes the other less desirable).

![Proposal Conflict Graph](https://i.imgur.com/CNjLhmr.png)

## Glossary of Notation
___
### Summary of State Variables

 Notation | Definition|
|--- | --- |
|$\mathcal{A}_t$ | |
|$\mathcal{C}_t$ | |
|$n_t$ | |
|$m_t$ | |
|$W_t$ | |
|$X_t$ | Individual participant conviction at time t|
|$y_t$ | Total aggregated community conviction at time t|
|$y^*_t$ | |
|$R_t$ | Available resources in the communal funding pool|
|$S_t$ | Effective supply of tokens available for community governance|

<br> 
<br>

## Summary Laws of Motion / State Transition

* A new address $a$ joins the community of participants:
$\mathcal{A}_{t+1} = \mathcal{A}_t \cup \{a\}$
$h_{t+1}[a]= \Delta h >0$

* An address $a$ leaves the community of participants:
$\mathcal{A}_{t+1} = \mathcal{A}_t \backslash \{a\}$
$h_{t+1}[a]= 0$

* A proposal $i$ is added to the set of candidates
$\mathcal{C}_{t+1} = \mathcal{C}_t \cup \{i\}$

* A proposal $i$ is removed from the set of candidates
$\mathcal{C}_{t+1} = \mathcal{C}_t \backslash\{i\}$

* Resources are added to the shared resource pool
$R_{t+1}= R_t+ \Delta r$

* Update Conviction Required to pass proposals
$y^*_{t+1} = [\cdots ,f(\mu_i), \cdots]$
where $\mu_i = \frac{r[i]}{R_t}$

* A participant allocates their support
$X_{t+1}[a,: ] = [\cdots,x[a,i],\cdots]$
s.t. $\sum_{i\in \mathcal{C}_t}x[a,i]\le h[a]$

* A proposal is passed given $y_t[i] \ge y^*_t[i]$
$\mathcal{C}_{t+1} = \mathcal{C}_t \backslash\{i\}$
$R_{t+1}= R_t- r[i]$

* Update Conviction
$y_{t+1}[i] =\alpha\cdot y_t[i] + \sum_{a\in \mathcal{A}_t} x[a, i]$

<br> 

## Parameters

 Notation | Definition|
|--- | --- |
|$\alpha$ | The decay rate for previously accumulated conviction |
|$\beta$ | Upper bound on share of funds dispersed in the example Trigger Function|
|$f(z)$| Trigger function that determines when a proposal has sufficient conviction to pass|
|$\rho$ | Scale Parameter for the example Trigger Function  |

Recall that the Trigger Function, $f(z)$ satisfies $f:[0,1]\rightarrow \mathbb{R}_+$
e.g. $f(z) = \frac{\rho S }{(1-\alpha)(z-\beta)^2}$

<br>

## Additional Considerations when Deploying CV

* Timescales
    * whether your system is operating in block times, or more human understandable timescales like hours, days or weeks, these considerations need to be factored into your model
* Minimum candidacy times
    * proposals should be active for a minimum period to ensure appropriate dialog occurs within the community, regardless of level of support
* Minimum conviction required for small proposals
    * to prevent small proposal spamming from draining the communal funding pool, all proposals should have some minimum conviction required to pass
* Effective supply
    * to avoid slow conviction aggregation due to "inactive" tokens (e.g. locked up in cold storage or liquidity pool, without active participation in governance), effective supply is the portion of tokens that are active in community governance
* Proposal statuses
    * proposals can exist in multiple status types, which can be expanded as this model grows
