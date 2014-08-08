import networkx as nx
import matplotlib.pyplot as plt
import argparse
import sys
import os

def main():

     parser = argparse.ArgumentParser()

     parser.add_argument("fileName", type = str, help= "Name of the input SAM fi\
le")

     args = parser.parse_args()
     fileName = args.fileName

     file = open(fileName, 'r')
     linkedContig = {}

     #extracts the gMin and gMax
     G = nx.Graph()
     G1 = nx.Graph()
     G2 = nx.Graph() 
     G3 = nx.Graph()
     G4 = nx.Graph()
     G5 = nx.Graph()
     G6 = nx.Graph()
     G7 = nx.Graph()
     G8 = nx.Graph()
     graphList = [G1, G2, G3, G4, G5, G6,G7,G8]
     lessFive = []
     lessTen = []
     less20 = []
     less30 = []
     less40 = []
     less50 = []
     less60 = []
     great60 = []


     for line in file:
          rowList = line.split("\t")
     
          numSup = int(rowList[4])
          contig1 = int(rowList[0])
          contig2 = int(rowList[1])
          weight = int(rowList[2]) + int(rowList[3]) / 2

          if numSup <= 5:
               G1.add_edge(rowList[0],rowList[1], weight  = weight)
               lessFive.append(G.add_edge(rowList[0],rowList[1]))
          elif numSup > 5 and numSup <= 10:
               G2.add_edge(rowList[0],rowList[1], weight  = weight)
               lessTen.append(G.add_edge(rowList[0],rowList[1]))
          elif numSup > 10 and numSup <= 20:
               G3.add_edge(rowList[0],rowList[1], weight  = weight)
               less20.append(G.add_edge(rowList[0],rowList[1]))      
          elif numSup > 20 and numSup <= 30:
               G4.add_edge(rowList[0],rowList[1], weight  = weight)
               less30.append(G.add_edge(rowList[0],rowList[1]))
          elif numSup > 30 and numSup <= 40:
               
               G5.add_edge(rowList[0],rowList[1], weight  = weight)
               less40.append(G.add_edge(rowList[0],rowList[1]))
          elif numSup > 40 and numSup <= 50:
               G6.add_edge(rowList[0],rowList[1], weight  = weight)
               less50.append(G.add_edge(rowList[0],rowList[1]))
          elif numSup > 50 and numSup <= 60:
               G7.add_edge(rowList[0],rowList[1], weight  = weight)
               less60.append(G.add_edge(rowList[0],rowList[1]))
          elif numSup > 60:
               G8.add_edge(rowList[0],rowList[1], weight  = weight)
               great60.append(G.add_edge(rowList[0],rowList[1]))
     all = [lessFive, lessTen, less20, less30, less40 ,less50, less60, great60]

     pos = nx.spring_layout(G)
     nx.draw_networkx_nodes(G, pos, node_size = 2, node_color = 'r')
     colorList = ['#C0C0C0','k','m','y','c','g','k','r']
     
     for j in range(len(all)):
          nx.draw_networkx_edges(graphList[j], pos, edge_color = colorList[j] )
     

     print "Number of Nodes: " + str(len(G.nodes()))
     print "Number of Connected Components: " + str(nx.number_connected_components(G))
                                     
     plt.savefig("graphTotal.png")

     plt.clf()

#     print len(G1.edges())
#     print G1.edges()
#     print len(G2.edges())
#     print G2.edges()
#     print len(G3.edges())
#     print G3.edges()
#     print len(G4.edges())
#     print G4.edges()
#     print len(G5.edges())
#     print G5.edges()
#     print len(G6.edges())
#     print G6.edges()
#     print len(G7.edges())
#     print G7.edges()
#     print len(G8.edges())
#     print G8.edges()
#     print len(G.edges())
#     print G.edges()
main()
                    
