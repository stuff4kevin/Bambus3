import networkx as nx
import matplotlib.pyplot as plt
import argparse
import sys
import os
import re

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
     
          if numSup <= 5:
               G1.add_edge(rowList[0],rowList[1])
               lessFive.append(G.add_edge(rowList[0],rowList[1]))
          
          elif numSup > 5 and numSup <= 10:
               G2.add_edge(rowList[0],rowList[1])
               lessTen.append(G.add_edge(rowList[0],rowList[1]))
               
          elif numSup > 10 and numSup <= 20:
               G3.add_edge(rowList[0],rowList[1])
               less20.append(G.add_edge(rowList[0],rowList[1]))      
          elif numSup > 20 and numSup <= 30:
               G4.add_edge(rowList[0],rowList[1])
               less30.append(G.add_edge(rowList[0],rowList[1]))
          elif numSup > 30 and numSup <= 40:
               
               G5.add_edge(rowList[0],rowList[1])
               less40.append(G.add_edge(rowList[0],rowList[1]))
          elif numSup > 40 and numSup <= 50:
               G6.add_edge(rowList[0],rowList[1])
               less50.append(G.add_edge(rowList[0],rowList[1]))
          elif numSup > 50 and numSup <= 60:
               G7.add_edge(rowList[0],rowList[1])
               less60.append(G.add_edge(rowList[0],rowList[1]))
          elif numSup > 60:
               G8.add_edge(rowList[0],rowList[1])
               great60.append(G.add_edge(rowList[0],rowList[1]))
     all = [lessFive, lessTen, less20, less30, less40 ,less50, less60, great60]

     print 
     total = 0
     for graphs in all:

          total = total + len(graphs)

     pos = nx.spring_layout(G)
     i = 0
     colorList = ['r','k','c','y','b','m','w','g']
     for j in range(len(all)):
          
         # pos = nx.spring_layout(graphList[i])
          
          nx.draw_networkx_nodes(graphList[i],pos, node_size = 1, node_color = 'r')          
          name = 'G'+str(j+1)
          print name
          nx.draw_networkx_edges(graphList[j], pos, edge_color = colorList[j])
     

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


     nx.draw(G1, pos = nx.spring_layout(G1), nos_size = 20)
     plt.savefig("graph1.png")
     plt.clf()
     nx.draw(G2, pos = nx.spring_layout(G2))
     plt.savefig("graph2.png")
     plt.clf()
     nx.draw(G3, pos = nx.spring_layout(G3))
     plt.savefig("graph3.png")
     plt.clf()
     nx.draw(G4, pos = nx.spring_layout(G4))
     plt.savefig("graph4.png")
     plt.clf()
     nx.draw(G5, pos = nx.spring_layout(G5))
     plt.savefig("graph5.png")
     plt.clf()
     nx.draw(G6, pos = nx.spring_layout(G6))
     plt.savefig("graph6.png")
     plt.clf()
     nx.draw(G7, pos = nx.spring_layout(G7))
     plt.savefig("graph7.png")
     plt.clf()
     nx.draw(G8, pos = nx.spring_layout(G8))
     plt.savefig("graph8.png")

main()
                    
