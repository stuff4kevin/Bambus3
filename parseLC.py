import operator
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
          otherPair = rowList[1]+"+"+rowList[0]
          min = rowList[3]+"."+rowList[2]+"."+"min"
          max = rowList[4]+"."+rowList[2]+"."+"max"
          if pairing not in linkedContig or otherPair not in linkedContig:
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
               while c <= len(combineFirst[thing])-1:
                    if c == len(combineFirst[thing]) -1 or combineFirst[thing][c].split(".")[-1] == "max":
                         
                         agreeCover = tuple(agreeCover)
                         
                         if agreeCover != ():
                              groupCover[thing].append(agreeCover)
                         
                         agreeCover = []
                         c =c+ 1
                    elif combineFirst[thing][c].split(".")[-1] == "min":
                         agreeCover.append(combineFirst[thing][c])
                         
                         c=c+ 1



          groupCover[thing] = set(groupCover[thing])
     final = []
     for stuff in groupCover:
          gclist = list(groupCover[stuff])
     
          for item in gclist:
               gapList = []
               fragList = []
               for x in item:
                    index = sortedSE[stuff][0].index(x) 
                    gapList.append((sortedSE[stuff][0][index].split(".")[0],sortedSE[stuff][1][index].split(".")[0])), 
                    fragList.append(sortedSE[stuff][0][index].split(".")[1])
               final.append([stuff.split("+")[0], stuff.split("+")[1], gapList[-1][0], gapList[0][-1], str(len(gapList)),(sorted(fragList, key = lambda x: int(x[5:]))), (gapList)])
     final = sorted(final, key = lambda x: int(x[0]))
     final = sorted(final, key = lambda x: int(x[4]), reverse = True)
     lastPrint = []

     for l in range(len(final)):
          if l == 0:
               lastPrint.append(final[l])
          else:
               listL = set(final[l][5])
               listOri = set(lastPrint[-1][5]) 
#               print listL
 #              print listOri
#               print type(listL)
 #              print type(listOri)
         #print  listOri.issuperset(listL) 
               if listOri.issuperset(listL) == False:
                    lastPrint.append(final[l])

     lastPrint= sorted(lastPrint, key = lambda z: int(z[0]))
     forRealLast = []

     for u in range(len(lastPrint)):

          if u == 0:
               forRealLast.append(lastPrint[u])
          else:
               listU = lastPrint[u][5]

               listPrev = forRealLast[-1][5]

               if set(listPrev).issuperset(set(listU)) == False:
                    forRealLast.append(lastPrint[u])

     forRealLast = sorted(forRealLast, key = lambda t: int(t[0]))
     for doit in forRealLast:
          print '\t'.join(str(w) for w in doit)
          
main()
