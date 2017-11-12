def plotgraph(dataset, industry_name=None, save=False):

    # show a graph network of political donations and assets owned
    # by congresspeople

    # generally an industry_name should be specified because the grpah
    # will become too cluttered otherwise. However, if you want to
    # filter the graph first, then you can leave industry_name
    # blank to show connections across industries
    if industry_name == None:
        dataset_subset = pd.DataFrame(dataset.dropna())
    else:
        dataset_subset = pd.DataFrame(dataset.dropna().query('RealCode == @industry_name'))

    # create the graph with edge attributes Amount and NumInvestments
    # RealCode is the industry
    # CID is the politician
    # Amount is the amount of money industries have donated to the politician
    # NumInvestments is the number of investments the politician has made in an industry
    graph = nx.from_pandas_dataframe(dataset_subset, 'RealCode', 'CID', ['Amount', 'NumInvestments'])

    # node_size is used as a node attribute
    node_size = dataset_subset.groupby('RealCode')['Amount'].sum().to_dict()


    temp = dataset_subset.groupby('CID')['Amount'].sum().to_dict()
    for key, value in temp.items(): temp[key] = 0
    node_size.update(temp)
    del temp

    nx.set_node_attributes(graph, node_size, 'TotalDonations')


    # initialize the graph
    # these numbers can be customized - scale increases the size
    # weight sets the length of the edges
    # k scales the amount of distance between nodes
    pos = nx.spring_layout(graph, scale=5, weight='Amount', k=15)
    # figsize is the dimensions of the resulting plot
    plt.figure(figsize=(75,75))

    # modify node size and color
    nodes = graph.nodes()
    sizes = [nodes[i]['TotalDonations'] for i in nodes]
    node_colors = [nodes[i] for i in nodes]
    for i in range(len(sizes)):
        # politician nodes
        if sizes[i] < 1:
            sizes[i] = 200
            node_colors[i] = 'red'
        # industry nodes
        else:
            sizes[i] = 2000
            node_colors[i] = 'cyan'

    # actually draw the network
    # font_size sets size of nodes and edges, but
    # edge font_size is overwritten later
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

    nx.draw_networkx_edges(graph, pos, edge_color = colors)


    # add edge labels
    edge_labels = nx.get_edge_attributes(graph,'NumInvestments')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels = edge_labels, font_size=12)

    # save the graph as a pdf
    if save==True and industry_name != None:
        plt.savefig("%sgraph.pdf" % industry_name)

    return plt
