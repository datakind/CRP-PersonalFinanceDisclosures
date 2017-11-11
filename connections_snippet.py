import networkx as nx

def connections(industry, congressperson):
    print(industry + ' has invested $',
      G[industry][congressperson]['Amount'],
      'in ' + congressperson+ ', and ' + congressperson + ' has made',
      G[industry][congressperson]['NumInvestments'],
      'investments in ' + industry)
