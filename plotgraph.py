import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy


def plotgraph(dataset, industry_name):

    dataset_subset = pd.DataFrame(dataset.dropna().query('RealCode == @industry_name'))

    graph = nx.from_pandas_dataframe(dataset_subset, 'RealCode', 'CID', ['Amount', 'NumInvestments'])

    node_size = dataset_subset.groupby('RealCode')['Amount'].sum().to_dict()

    temp = dataset_subset.groupby('CID')['Amount'].sum().to_dict()
    for key, value in temp.items(): temp[key] = 0
    node_size.update(temp)
    del temp

    nx.set_node_attributes(graph, node_size, 'TotalDonations')


    # initialize the graph
    pos = nx.spring_layout(graph, scale=5, weight='Amount', k=15)
    plt.figure(figsize=(75,75))

    # modify node size and color
    nodes = graph.nodes()
    sizes = [nodes[i]['TotalDonations'] for i in nodes]
    node_colors = [nodes[i] for i in nodes]
    for i in range(len(sizes)):
        if sizes[i] < 1:
            sizes[i] = 200
            node_colors[i] = 'red'
        else:
            sizes[i] = 2000
            node_colors[i] = 'cyan'

    nx.draw_networkx(graph, pos,
                    font_size=8,
                    node_size=sizes,
                    node_color=node_colors)


    # add edge colors
    edges = graph.edges()
    colors = [graph[u][v]['NumInvestments'] for u,v in edges]
    for i in range(len(colors)):
        if colors[i]<5:
            colors[i] = '#0000ff' #blue
        elif colors[i]<10:
            colors[i] = '#ab0fff' #purple
        elif colors[i]<15:
            colors[i] = '#ffae00' #orange
        else:
            colors[i] = '#ff0000' #red

    nx.draw_networkx_edges(graph, pos, edge_color = colors)#, width=log(weights))


    # add edge labels
    edge_labels = nx.get_edge_attributes(graph,'NumInvestments')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels = edge_labels, font_size=12)

    # save the graph as a pdf
    plt.savefig("%sgraph.pdf" % industry_name)
    
    return plt


## example ##
# use the format of industry_df
# as used in the main python code
# plotgraph(industry_df,'A2000')
