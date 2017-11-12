import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy

pacs = pd.read_csv('Campaign_Finance_data/pacs_all.csv', encoding = "ISO-8859-1")
conginvest = pd.read_csv('Goal1_PFD_1of3.csv', encoding = "ISO-8859-1")

# RealCodeOut is congresspeople investing
# RealCodeIn is industry giving money to congresspeople
conginvest = conginvest[['CID', 'RealCode']].rename(columns={'RealCode':'RealCodeOut'}). \
    groupby(['CID','RealCodeOut']).size().reset_index(name='NumInvestments')
pacs = pacs[['Cycle', 'CID', 'PACID', 'Amount', 'RealCode']].rename(columns={'RealCode':'RealCodeIn'})

# Table of PAC contributions by industry code and to which congressperson
contributions = pacs. \
    groupby(['PACID', 'RealCodeIn', 'CID'])['Amount']. \
    sum().reset_index()

# merge conginvest with contributions to have all the data in one table
df = contributions.merge(conginvest,
                         left_on=['CID','RealCodeIn'], right_on=['CID','RealCodeOut'], how='left'). \
                        drop('RealCodeOut', axis=1). \
                        rename(columns={'RealCodeIn': 'RealCode'})

industry_df = df.groupby(['RealCode', 'CID'])['Amount', 'NumInvestments']. \
    sum().reset_index()

# Creating the graph #

industry_subset = pd.DataFrame(industry_df.dropna()[:50])

G = nx.from_pandas_dataframe(industry_subset, 'RealCode', 'CID', ['Amount', 'NumInvestments'])

node_size = industry_subset.groupby('RealCode')['Amount'].sum().to_dict()

temp = industry_subset.groupby('CID')['Amount'].sum().to_dict()
for key, value in temp.items(): temp[key] = 0
node_size.update(temp)
del temp

nx.set_node_attributes(G, node_size, 'size')

# initialize the graph
pos = nx.spring_layout(G, scale=10, weight='Amount', k=10)
plt.figure(figsize=(75,75))


# modify node size and color
nodes = G.nodes()
sizes = [nodes[i]['size'] for i in nodes]
node_colors = [nodes[i] for i in nodes]
for i in range(len(sizes)):
    if sizes[i] < 1:
        sizes[i] = 300
        node_colors[i] = 'red'
    else:
        sizes[i] = 10000
        node_colors[i] = 'cyan'

nx.draw_networkx(G, pos,
                font_size=8,
                node_size=sizes,
                node_color=node_colors)


# add edge colors
edges = G.edges()
colors = [G[u][v]['NumInvestments'] for u,v in edges]
for i in range(len(colors)):
    if colors[i]<5:
        colors[i] = '#0000ff' #blue
    elif colors[i]<10:
        colors[i] = '#ab0fff' #purple
    elif colors[i]<15:
        colors[i] = '#ffae00' #orange
    else:
        colors[i] = '#ff0000' #red


weights = [G[u][v]['Amount'] for u,v in edges]
# decided not to use weights because it makes it harder to
# use the number of nodes we have

nx.draw_networkx_edges(G, pos, edge_color = colors)#, width=log(weights))


# add edge labels
edge_labels = nx.get_edge_attributes(G,'NumInvestments')
nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels, font_size=12)

# save the graph as a pdf
plt.savefig('mini-graph.pdf', dpi=800)


# save the whole graph (not subset) as a gpickle for easy distribution
H = nx.from_pandas_dataframe(industry_df, 'RealCode', 'CID', ['Amount', 'NumInvestments'])
node_size = industry_df.groupby('RealCode')['Amount'].sum().to_dict()

temp = industry_df.groupby('CID')['Amount'].sum().to_dict()
for key, value in temp.items(): temp[key] = 0
node_size.update(temp)
del temp

nx.set_node_attributes(G, node_size, 'TotalDonations')

nx.write_gpickle(H,"NetworkxGraph.gpickle")
