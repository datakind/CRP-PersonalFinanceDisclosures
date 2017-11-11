import numpy as np
import pandas as pd
import networkx as nx

if __name__ == "__main__":
    #df_lob = pd.read_csv("Goal1_lobbying_2of3.csv")
    df_PFD = pd.read_csv("data/Goal1_PFD_1of3.csv")
    df_PFD["RealCode_comb"] = df_PFD["RealCode"] + "," + df_PFD["RealCode2"]
    df_PAC = pd.read_csv("data/Campaign_Finance_data/pacs_all.csv")

    Cycle = 2010
    CalendarYear = 10

    df_PFD = df_PFD[df_PFD["CalendarYear"] == CalendarYear]
    df_PAC = df_PAC[df_PAC["Cycle"] == Cycle]

    df_PAC_gb = df_PAC.groupby(by=["PACID", "CID", "RealCode"])
    df_PFD_gb = df_PFD.groupby(by=["CID","RealCode"])

    pacid_to_cid_amounts = df_PAC_gb["Amount"].sum()
    cid_rc_counts = df_PFD_gb.size()

    thresh = np.percentile(pacid_to_cid_amounts,95)

    cid_rc_dict = {}
    cid_rc_list = []

    for i in range(len(cid_rc_counts)):
        cid, rc = cid_rc_counts.index[i]
        if cid in cid_rc_dict: cid_rc_dict[cid].append(rc)
        else: cid_rc_dict[cid] = [rc]

    for key in cid_rc_dict:
        cid_rc_list.append([key,",".join(cid_rc_dict[key])])

    
    df_paccid = pacid_to_cid_amounts.reset_index()
    df_cidrc = pd.DataFrame(cid_rc_list) 
    df_cidrc.columns = ["CID", "RealCodes"]

    df_merged = df_paccid.merge(df_cidrc,on="CID")

    df_final = df_merged[df_merged.apply(lambda x: x.RealCode in x.RealCodes, axis = 1)]
    df_final = df_final[df_final.Amount > 0]

    G = nx.DiGraph()
    pacnodes = []
    cidnodes = []
    edge_list = []

    G.add_nodes_from(df_final["PACID"],id = 1)
    G.add_nodes_from(df_final["CID"], id = 2)

    for i in range(len(df_final)):
         pacid = df_final.iloc[i]["PACID"]
         cid = df_final.iloc[i]["CID"]
         amnt = df_final.iloc[i]["Amount"]
         edge_list.append((pacid,cid,int(amnt)))
         G.add_edge(pacid,cid,weight= int(amnt))

    nx.write_graphml(G,"PAC_to_PFD.graphml")    

    # #PART 1: PAC TO CID graph

    # G = nx.DiGraph()

    # pacnodes = []
    # cidnodes = []

    # edge_list = []

    # for i in range(len(pacid_to_cid_amounts)):
    #     pacid, cid = pacid_to_cid_amounts.index[i]
    #     amnt = pacid_to_cid_amounts[(pacid,cid)]
    #     if amnt >= thresh:
    #         pacnodes.append(pacid)
    #         cidnodes.append(cid)
    #         edge_list.append((pacid,cid,int(amnt)))
    
    # G.add_nodes_from(pacnodes,id = 1)
    # G.add_nodes_from(cidnodes,id = 2)
    # #G.add_edges_from(edge_list)
    # for pacid, cid, amt in edge_list:
    #     G.add_edge(pacid,cid,weight=amt)

    # nx.write_graphml(G,"PAC_to_CID.graphml")

    # #PART 2: CID TO PFD graph
    # G2 = nx.DiGraph()
    # cidnodes = []
    # rcnodes = []

    # edge_list = []

    # for i in range(len(cid_rc_counts)):
    #     cid, rc = cid_rc_counts.index[i]
    #     if len(rc) == 5:
    #         counts = cid_rc_counts[(cid,rc)]
    #         cidnodes.append(cid)
    #         rcnodes.append(rc)
    #         edge_list.append((cid,rc,int(counts)))
    
    # G2.add_nodes_from(cidnodes,id = 2)
    # G2.add_nodes_from(rcnodes,id = 3)
    # #G.add_edges_from(edge_list)
    # for cid, rc, counts in edge_list:
    #     G2.add_edge(cid,rc,weight=counts)

    # nx.write_graphml(G2,"CID_to_PFD.graphml")




