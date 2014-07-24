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
     colorList = ['r','g','b','c','m','k','y']
     pos = {}
     i = 1
     for line in file:
          rowList = line.split("\t")
          if rowList[4] < 2:
               G.add_edge(rowList[0],rowList[1], edge_color = 'r')
          elif rowList[4] > 2 and rowList[4] < 5:
               G.add_edge(rowList[0],rowList[1], edge_color = 'g')
          elif rowList[4] > 5 and rowList[4] < 10:
               G.add_edge(rowList[0],rowList[1], edge_color = 'b')
          elif rowList[4] > 5 and rowList[4] < 10:
               G.add_edge(rowList[0],rowList[1], edge_color = 'c')
          elif rowList[4] > 10 and rowList[4] < 20:
               G.add_edge(rowList[0],rowList[1], edge_color = 'm')
          elif  rowList[4] > 20 and rowList[4] < 50:
               G.add_edge(rowList[0],rowList[1], edge_color = 'y')
          elif  rowList[4] > 50 :
               G.add_edge(rowList[0],rowList[1], edge_color = 'k')
               
               
               
     nx.draw_spring(G) 
     
     plt.savefig("graph.pdf", dpi=1000)
main()
                    
