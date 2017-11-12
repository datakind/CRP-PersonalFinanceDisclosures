"""
PAC_to_PFD.py
Hyung Joo Park
11/2017 Datakind DataDive
"""

import numpy as np
import pandas as pd
import networkx as nx

if __name__ == "__main__":

    #We define a conflict of interest relationship to be a case when a PAC
    #donates money to a politician (CID) who happens to disclose that he
    #holds assets in the industry (RealCode) that the PAC is also associated
    #with.
    #To discover these relationships, we need to merge the PFD data with the 
    #pacs_all data.
    #This script does that and will output a GraphML file of a bipartite
    #directed graph (the direction being PACID -> CID) that contains all the
    #conflict of interest relationships we discover. The edges are weighted by 
    #the total amount the PAC donated to that particular politician.
    #To help with the graphing, we set the attribute id = 1 for PACID nodes
    #and id = 2 for CID nodes. 

    df_PFD = pd.read_csv("data/Goal1_PFD_1of3.csv")
    df_PFD["RealCode_comb"] = df_PFD["RealCode"] + "," + df_PFD["RealCode2"]
    df_PAC = pd.read_csv("data/Campaign_Finance_data/pacs_all.csv")

    Cycle = 2010
    CalendarYear = 10 # Make sure this value aligns with Cycle
    df_PFD = df_PFD[df_PFD["CalendarYear"] == CalendarYear]
    df_PAC = df_PAC[df_PAC["Cycle"] == Cycle]

    #Here, we figure out how much money a PAC (uniquely identified by PACID
    #and RealCode) donated to a politician (CID) by grouping on those three
    #fields and summing Amount.  (pacid_to_cid_amounts)
    #Also, we calculate how many types of assets a politician (CID) has for a 
    #given type of industry (RealCode).  (cid_rc_counts)

    df_PAC_gb = df_PAC.groupby(by=["PACID", "CID", "RealCode"])
    df_PFD_gb = df_PFD.groupby(by=["CID","RealCode"])
    pacid_to_cid_amounts = df_PAC_gb["Amount"].sum()
    cid_rc_counts = df_PFD_gb.size()

    #We want to merge the two datasets from above (pacid_to_cid_amounts and
    #cid_rc_counts) so that we can determine, in a given, year a conflict of
    #interest relationship.  To do this, we create the following two dataframes:
    #
    #df_paccid: DataFrame with PACID, CID, RealCode, Amount
    #df_cidrc: DataFrame with CID and RealCodes
    #          where RealCodes is a concatenated string of all the RealCode
    #          values associated with a particular CID

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

    #The next two lines do the following:
    # - Select rows where RealCode from df_paccid is in RealCodes
    #   (this action makes sure that the industry that the PACID associates with
    #    is included in the list of RealCodes that the CID has assets in)
    # - Select rows where the PACID's donation is greater than 0.
    df_final = df_merged[df_merged.apply(lambda x: x.RealCode in x.RealCodes, axis = 1)]
    df_final = df_final[df_final.Amount > 0]

    #The following code uses networkx to build the bipartite graph and output
    #it into a GraphML file.
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


    #The following lines were used to study pacs_all and PFD datasets 
    #separately.  The code may not run properly.


    # #PART 1: PAC TO CID graph

    # G = nx.DiGraph()

    # pacnodes = []
    # cidnodes = []

    # edge_list = []

    # thresh = np.percentile(pacid_to_cid_amounts,95)

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