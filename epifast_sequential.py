import argparse
import os
#import matplotlib.pylab as plt
import json
import networkx as nx
from networkx.readwrite import json_graph
# Import packages for data cleaning
import numpy as np
#import pandas as pd
import re # For finding specific strings in the text
# Import packages for data visualization
import networkx as nx
#import matplotlib.pyplot as plt
#test = nx.DiGraph()
import random
import sys
#print('test')
import networkx as nx
G = nx.DiGraph()
# add nodes, edges, etc to G ...


def add_both_edge(G, node1, node2):
    """
    adding both edges with weight 1
    """
    G.add_edge(node1, node2, weight=1)
    G.add_edge(node2, node1, weight=1)
    #print('added')

#Call intervention when more than 2% of population is infected
#return list of edges 
#default percent_remove = 10%
def intervention1(G, percent_removed=10):
    #number of edges removed
    #When more than 0.1% of the population are infectious,
    percent = float(percent_removed) / 100
    num_removed_edges = int(G.number_of_edges() * percent)
    #randomly choose edges
    selected =  random.sample(G.edges(), num_removed_edges)
    #add its reverse as well 
    #for edge in selected:
    #    #if the reverse edge is not in selected
    #    if (edge[1], edge[0]) not in selected:
    #        selected.append((edge[1], edge[0]))
    return selected


#Call intervention 2 when there are 2% of population is infected
#return list of edges to remove with number of threshold is greater
#default percent_remove = 10%
#default threshold of number of outer edges = 3
def intervention2(G, percent_removed, threshold):
    #number of edges removed
    #collect nodes if one of the nodes with number of edges greater or equal to 3
    selected_edges = [(u,v) for u,v in G.edges() if (len(G.out_edges(u)) > threshold or len(G.out_edges(v)) > threshold)]
    #for u,v in G.edges():
    #    print(u)
    #    print(len(G.out_edges(u)))  
    #print(selected_edges)
    percent = float(percent_removed) / 100
    num_removed_edges = int(G.number_of_edges() * percent)
    #randomly choose edgesi
    #print(num_removed_edges)
    selected =  random.sample(list(selected_edges), num_removed_edges)
    #for edge in selected:
    #    #if the reverse edge is not in selected
    #    if (edge[1], edge[0]) not in selected:
    #        selected.append((edge[1], edge[0]))
    return selected

def update(G, rate, S, E, I, R, newly_exposed):
    #update daily based on rate 
    #S, E, I, and R represents list of nodes with number of days in 
    for ne in newly_exposed:
        E[ne] = rate['t_e'] + 1
        newly_exposed.remove(ne)
    for i in I.keys():
        I[i] -= 1
        if I[i] == 0:
            del I[i]
            #Remove recovered node from the graph 
            G.remove_node(i)
            R.append(i)
    for e in E.keys():
        E[e] -= 1
        if E[e] == 0:
            del E[e]
            I[e] = rate['t_i']

def sequential(G, rate, S, E, I, R, NE, T, t_rate):
    for t in range(T):
        #first thing of the day
        #update at morning 
        update(G, rate, S, E, I, R, NE)

        #no intervention at this level
        #
        for i in I.keys():
            contact = G.out_edges(i)
            for c in contact:
                #calculate transmissibility 
                #p(w(u,v)) = 1-(1-r)^{(w(u,v))}
                #TODO actually impliment weighted but since the weight is uniformed, the p(w(u,v)) = 0.5 
                #if v is adjacenet to u. 
                #if transmissed
                if (c[1] in S) and (np.random.binomial(1, t_rate) >0):
                    NE.append(c[1])
                    S.remove(c[1])
        print("%s\t%s\t%s\t%s\t%s\t%s" % (str(t+1), str(len(S)), str(len(E.keys())), str(len(I.keys())), str(len(R)), str(len(NE))))

def seq_intervention1(G, rate, S, E, I, R, NE, T, t_rate, remove_edge_percent=10):
    for t in range(T):
        #first thing of the day
        #update at morning 
        update(G, rate, S, E, I, R, NE)

        #no intervention at this level
                #no intervention at this level
        #intervention 1
        removed_edges = []
        #if infected people are greater than 0.1% of population
        if len(I.keys()) > (len(S) + len(E.keys()) + len(I.keys()) + len(R) + len(NE)) * 0.0001:
            #print((len(S) + len(E.keys()) + len(I.keys()) + len(R) + len(NE))  * 0.0001)
            #print("intervention activated")
            removed_edges = intervention1(G, remove_edge_percent)
            #print(removed_edges)
        for i in I.keys():
            contact = G.out_edges(i)
            for c in contact:
                #calculate transmissibility 
                #p(w(u,v)) = 1-(1-r)^{(w(u,v))}
                #TODO actually impliment weighted but since the weight is uniformed, the p(w(u,v)) = 0.5 
                #if v is adjacenet to u. 
                #if transmissed
                if (c not in removed_edges) and (c[1] in S) and (np.random.binomial(1, 0.5) >0):
                    NE.append(c[1])
                    S.remove(c[1])

        print("%s\t%s\t%s\t%s\t%s\t%s" % (str(t+1), str(len(S)), str(len(E.keys())), str(len(I.keys())), str(len(R)), str(len(NE))))

def seq_intervention2(G, rate, S, E, I, R, NE, T, t_rate, remove_edge_percent=10, threshold=5):
    for t in range(T):
        #first thing of the day
        #update at morning 
        update(G, rate, S, E, I, R, NE)

        #no intervention at this level
        
        removed_edges = []
        #if infected people are greater than 0.1% of population
        if len(I.keys()) > (len(S) + len(E.keys()) + len(I.keys()) + len(R) + len(NE)) * 0.0001:
            #print((len(S) + len(E.keys()) + len(I.keys()) + len(R) + len(NE))  * 0.0001)
            #print("intervention activated")
            removed_edges = intervention2(G, remove_edge_percent, threshold)
            #print(removed_edges)
        for i in I.keys():
            contact = G.out_edges(i)
            for c in contact:
                #calculate transmissibility 
                #p(w(u,v)) = 1-(1-r)^{(w(u,v))}
                #TODO actually impliment weighted but since the weight is uniformed, the p(w(u,v)) = 0.5 
                #if v is adjacenet to u. 
                #if transmissed
                if (c not in removed_edges) and (c[1] in S) and (np.random.binomial(1, 0.5) >0):
                    NE.append(c[1])
                    S.remove(c[1])

        print("%s\t%s\t%s\t%s\t%s\t%s" % (str(t+1), str(len(S)), str(len(E.keys())), str(len(I.keys())), str(len(R)), str(len(NE))))
        
print("Starting.....")

parser =argparse.ArgumentParser()
parser.add_argument("--input_format",
                    nargs='+',
                    required=True,
                    help="{json/raw} whether the file is in networkx json('nodes'=[], 'edges'=[]) or format of space separated as Dr. Eubank's ")
parser.add_argument("--input_file",
                    nargs='+',
                    required=True,
                    help="Name of the input file")
parser.add_argument("--output_file",
                    nargs='+',
                    required=True,
                    help="Name of the output file")
parser.add_argument("--time", required=False, type=int, default="300", help="Simulation period in days")
parser.add_argument("--init_infection", required=False, type=int, default="20", help="Number of initial infectious people")
parser.add_argument("--transmission_rate", required=False, type=str, default="0.5", help="probability of disease transmission for a contact of one unit time")
parser.add_argument("--incubation_period", required=False, type=int, default="2", help="Average time period(in days) to be in exposed phase")
parser.add_argument("--infectious_period", required=False, type=int, default="4", help="Average time period(in days) to be infectious to other nodes")
parser.add_argument("--intervention", required=False, type=int, default="0", help="Options for intervention. Default 0. 0=No intervention, 1=Intervention 1, 2=intervention2")
parser.add_argument("--remove_edge_percent", required=False, type=int, default=10, help="With intervention option removing 10% of edges")
parser.add_argument("--threshold", required=False, type=int, default=5, help="Only edges from node with 5+ edges will be considered to be removed with intervention 2")



args = parser.parse_args()
input_format = args.input_format[0]
input_file = args.input_file[0]
output_file = args.output_file[0]
#sys.stdout=open(output_file, 'w')
time = args.time
init_infection = args.init_infection
transmission_rate = float(args.transmission_rate)
#print(args.transmission_rate)
#print(transmission_rate)
intervention = args.intervention
t_e = args.incubation_period
t_i = args.infectious_period
remove_edge_percent = args.remove_edge_percent
threshold = args.threshold

rate = {'t_e': t_e, 't_i':t_i}
t_r=transmission_rate
T=time

G=nx.DiGraph()
if (input_format == 'raw'):
    ver_number = {}
    ver_ver = {}
    just_number = []
    line_count = 0
    map_file = open(input_file+'.json', "w+")
    with open(input_file) as fp:
        line = fp.readline()
        ver_name = ""
        ver_list = []
        while line:
            values = line.split()
            if len(values) ==2: #vertex    degree
                if(len(ver_list) != 0): 
                    ver_ver[ver_name] = ver_list
                    ver_list = []
                just_number.append(int(values[1]))
                ver_number[values[0]] = int(values[1])
                ver_name = values[0]
            else: #     vertex    weight   0
                ver_list.append(values[0])
                #G.add_edge(int(ver_name), int(values[0]), weight=float(values[1]))
                add_both_edge(G, ver_name, values[0])
            #print(line)
            line = fp.readline()
    map_file.write(json.dumps(dict(nodes=G.nodes(), edges=G.edges())))
    map_file.close()
elif (input_format == 'json'):
    d = json.load(open(input_file, "r"))
    G.add_nodes_from(d['nodes'])
    G.add_edges_from(d['edges'])
else:
    print("Invalid input format")
    sys.exit()

print("finished reading the graph")

exposed = {}
removed = []
newly_exposed = []
#randomly pick 20 nodes
infectious = {}
init_infectious_nodes = random.sample(list(G.nodes()), init_infection)
for init_i_nodes in init_infectious_nodes:
    infectious[init_i_nodes] = rate['t_i']
print("calling sequentials")
susceptible=[node for node in list(G.nodes()) if node not in init_infectious_nodes]


print("Day\tSusceptible\tExposed\tInterfectious\tRecovered\tNewly Exposed")
if (intervention == 0):
    sequential(G, rate, susceptible, exposed, infectious, removed, newly_exposed, T, t_r)
elif (intervention == 1):
    seq_intervention1(G, rate, susceptible, exposed, infectious, removed, newly_exposed, T, t_r, remove_edge_percent)
elif (intervention == 2):
    seq_intervention2(G, rate, susceptible, exposed, infectious, removed, newly_exposed, T, t_r, remove_edge_percent, threshold)
else:
    print("Invalid intervention input")
