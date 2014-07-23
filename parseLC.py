
import argparse
import sys
import os
import re

def main():

     parser = argparse.ArgumentParser()

     parser.add_argument("fileName", type = str, help= "Name of the input SAM file")

     args = parser.parse_args()
     fileName = args.fileName
     
     file = open(fileName, 'r')
     linkedContig = {}
     
     #extracts the gMin and gMax 
     for line in file:
          
          
          rowList = line.split()
          pairing = rowList[0]+"+"+rowList[1]
          min = rowList[3]+"."+rowList[2]+"."+"min"
          max = rowList[4]+"."+rowList[2]+"."+"max"
          if pairing not in linkedContig:
               linkedContig[pairing] = set([(min,max)])
          else:
               linkedContig[pairing].add((min,max))

     sortedSE = {}
     combineFirst = {}
     
     for element in linkedContig:
          # labels start and ends and by set
          gMin = [ x[0] for x in linkedContig[element]]
          gMax = [ y[1] for y in linkedContig[element]]
          gMin = sorted(gMin, key = lambda x: int(x.split(".")[0]))
          
          gMax = sorted(gMax, key = lambda x: int(x.split(".")[0]))
          
          # sorts by the actually gap value
          combineFirst[element] = sorted(gMin+gMax, key = lambda x: int(x.split(".")[0]))
          sortedSE[element] = [gMin, gMax]
     groupCover = {}
     #counter = 0
     for thing in combineFirst:
          #counter = counter + 1
          groupCover[thing] = []
          for i in range(len(combineFirst[thing])):

               agreeCover = []
               
               c = i
               while  c <= len(combineFirst[thing])-1:
                    if  c == len(combineFirst[thing]) -1 or combineFirst[thing][c].split(".")[-1] == "max":
                         
                         agreeCover = tuple(agreeCover)
                         if agreeCover != ():
                              groupCover[thing].append(agreeCover)
                         
                         agreeCover = []
                         c =c+ 1
                    elif combineFirst[thing][c].split(".")[-1] == "min":
                         agreeCover.append(combineFirst[thing][c])
                         c=c+ 1


          groupCover[thing] = set(groupCover[thing])
     newFile = open('combineFirst', 'w')
     for stuff in combineFirst:
          newFile.write(stuff)  
          newFile.write("\n")
          newFile.write(" ".join(combineFirst[stuff]))
          newFile.write("\n")
          

          gclist = list(groupCover[stuff])
     
          for item in gclist:
               newList = []
               for x in item:
                    #item is a tuple
                    index = sortedSE[stuff][0].index(x) 
                    newList.append((sortedSE[stuff][0][index].split(".")[0],sortedSE[stuff][1][index].split(".")[0])), 
          print stuff.split("+")[0] + "\t" + stuff.split("+")[1] + "\t " + newList[-1][0] + "\t" + newList[0][-1] + "\t" + str(len(newList)) + "\t" + str(newList)
main()
