

# Isolates + Member + Star < Bridge < Organizer

import networkx as nx
from community import community_louvain
import operator
G = nx.read_weighted_edgelist('Only_50_Employees1.csv', delimiter=',', create_using = nx.DiGraph(), nodetype=str)



# ORGANIZERS
organizer = dict(nx.pagerank(G, weight=True))
n = int(len(organizer) * 0.10)
organizer_dict = dict(sorted(organizer.items(), key=operator.itemgetter(1), reverse=True)[:n])
organizer_dict = {x: 0 for x in organizer_dict}
del organizer
del n



# BRIDGES
G = nx.read_weighted_edgelist('Only_50_Employees1.csv', delimiter=',', create_using = nx.Graph(), nodetype=str)
gatekeeper = dict(nx.bridges(G))
gatekeeper_dict = {k: v for k, v in gatekeeper.items() if k not in organizer_dict}
gatekeeper_dict = {x: 1 for x in gatekeeper_dict}
del gatekeeper



# STAR
part = community_louvain.best_partition(G)                                                     # Finding Communities
def invert(d):                                                                                 # Turn {a:x, b:x} into {x:[a,b]}
    r = {}
    for k, v in d.items():
        r.setdefault(v, []).append(k)
    return r
invert_partition = invert(part)
star_dict = {}        # iterate over each community
for community_id in invert_partition.keys():                                                   #Extract the sub graph containing the community nodes
    temp_graph = G.subgraph(invert_partition[community_id])
    temp_degree = dict(temp_graph.degree())                                                    #Extract the degrees in the subgraph
    star_dict[community_id] = max(temp_degree, key=lambda x: temp_degree[x])                   #Store it in a dictionary, with key as community_id and value as the node with max degree
star_dict = dict((v,k) for k,v in sorted(star_dict.items(), key=operator.itemgetter(1)))
star_dict = {k: v for k, v in star_dict.items() if k not in organizer_dict}
star_dict = {k: v for k, v in star_dict.items() if k not in gatekeeper_dict}
star_dict = {x: 2 for x in star_dict}
del community_id, invert_partition, part, temp_degree



# ISOLATES
isolate_dict = dict(G.degree())
isolate_dict = {key:val for key, val in isolate_dict.items() if val == 1 or 0}
isolate_dict = {x: 3 for x in isolate_dict}


final_roles = {**organizer_dict, **gatekeeper_dict, **star_dict, **isolate_dict}














# ALTERNATIVE FUNCTIONS

Isolates & Bridges = Perfect

G = nx.read_weighted_edgelist('Only_50_Employees1.csv', delimiter=',', create_using = nx.Graph(), nodetype=str)
G = nx.read_edgelist('Only_50_Employees1No.csv', delimiter=',', create_using = nx.DiGraph(), nodetype=str)


Organizer Measure:
    organizer = dict(nx.pagerank(G, weight=True))       """A node is important based on how important its neighbours are (with a damping factor)"""
    hub_score, auth_score = nx.hits(G)           """A node is important based on a hub-score combined with an authority-score"""
    organizer = dict(nx.eigenvector_centrality(G))        """A node is important based on how important its neighbours are"""
    organizer = dict(nx.betweenness_centrality(G))        """A node is important based on shortest-path centrality"""


Star Partioning: 
    part = community_louvain.best_partition(G)
    part = nx.community.girvan_newman(G)
    Fast greedy modularity optimization
    Exhaustive modularity optimization via simulated annealing
    Fast modularity optimization
    Cfinder
    Markov-Cluster
    Structural
    Dynamic
    Spectral
    EM
    Potts Model






















