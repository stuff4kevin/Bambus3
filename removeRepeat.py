import argparse
import sys
import os
import ast

def main():

     parser = argparse.ArgumentParser()

     parser.add_argument("fileName", type = str)

     args = parser.parse_args()
     fileName = args.fileName
     temp = []
     file = open(fileName, 'r')

     for line in file:

          rowList = line.split("\t")
          
          temp.append(rowList)


     finalList = []
     for u in range(len(temp)):

         if u == 0:
              finalList.append(temp[u])
         else:
#              print temp[u][5]
              listU = temp[u][5].split(") (")             
              listPrev = finalList[-1][5].split(") (")

              newListU = []
              newListPr = []
              for item in listU:
                   newListU.append(item)
                   
              for items in listPrev:
                   newListPr.append(items)
  #                 print newListU
   #                print newListPr     
              if set(newListPr).issuperset(set(newListU)) == False:
    #               print False
                   finalList.append(temp[u])
              elif set(newListPr).issubset(set(newListU)) == True:
     #              print True
                   finalList.pop()
                   finalList.append(temp[u])
             
     for element in finalList:
          print "\t".join(str(w) for w in element),
         
main()
