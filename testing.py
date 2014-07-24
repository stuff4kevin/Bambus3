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
          numSup = rowList[4]
          contig1 = int(rowList[0])
          contig2 = int(rowList[1])
     
          if numSup < 5:
               G.add_edge(rowList[0],rowList[1])
               lessFive.append(G.add_edge(rowList[0],rowList[1]))
          if numSup >= 5 and rowList[4] < 10:
               G.add_edge(rowList[0],rowList[1])
               lessTen.append(G.add_edge(rowList[0],rowList[1]))
          if numSup >= 10 and rowList[4] < 20:
               G.add_edge(rowList[0],rowList[1])
               less20.append(G.add_edge(rowList[0],rowList[1]))      
          if numSup >= 20 and rowList[4] < 30:
               G.add_edge(rowList[0],rowList[1])
               less30.append(G.add_edge(rowList[0],rowList[1]))
          if numSup >= 30 and rowList[4] < 40:
               G.add_edge(rowList[0],rowList[1])
               less40.append(G.add_edge(rowList[0],rowList[1]))
          if numSup >= 40 and rowList[4] < 50:
               G.add_edge(rowList[0],rowList[1])
               less50.append(G.add_edge(rowList[0],rowList[1]))
          if numSup >= 50 and rowList[4] < 60:
               G.add_edge(rowList[0],rowList[1])
               less60.append(G.add_edge(rowList[0],rowList[1]))
          if numSup >= 60:
               G.add_edge(rowList[0],rowList[1])
               great60.append(G.add_edge(rowList[0],rowList[1]))
     all =  [ lessFive, lessTen, less20, less30, less40 ,less50, less60, great60]

      
     pos = nx.spring_layout(G)
     nx.draw_networkx_nodes(G,pos, node_size = 20)
     i = 0
     colorList = ['w','y','c','g','b','M','r','K']
     for list in all:
                    
          nx.draw_networkx_edges(G, pos, edge_color = colorList[i])
          i = i + 1
     
     plt.savefig("graph.png", dpi=1000)
main()
                    
