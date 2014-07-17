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
     
     counter = 0
     #extracts the gMin and gMac 
     for line in file:
          counter = counter +1
          rowList = line.split()
          pairing = rowList[0]+"+"+rowList[1]
          if pairing not in linkedContig:
               linkedContig[pairing] = set([(rowList[3], rowList[4])])
          else:
               linkedContig[pairing].add((rowList[3], rowList[4]))

     sortedSE = {}
     combineFirst = {}
     
     for element in linkedContig:
          # labels start and ends and by set
          gMin = [ x[0]+".s" for x in list(linkedContig[element])]
          gMax = [ y[1]+".e" for y in list(linkedContig[element])]
     
          for i in range(len(gMin)):
               # labels each link
               gMin[i] = gMin[i]+"."+str(i+1)
               gMax[i] = gMax[i]+"."+str(i+1)
          
          gMin = sorted(gMin, key = lambda x: int(x.split(".")[0]))
          gMax = sorted(gMax, key = lambda x: int(x.split(".")[0]))
          
          # sorts by the actually gap value
          combineFirst[element] = sorted(gMin+gMax, key = lambda x: int(x.split(".")[0]))
          sortedSE[element] = [gMin, gMax]
     groupCover = {}
     for element in combineFirst:
 #         print element
          groupCover[element] = set([])
          for i in range(len(combineFirst[element])):

               agreeCover = []
               
               c = i
               while  c < len(combineFirst[element])-1:
                   # print "len is " + str(len(combineFirst[element])-1)
    #                print "c is " + str(c)
    #               if c == len(combineFirst[element]) or combineFirst[element][c].split(".")[-1] == agreeCover[0].split(".")[-1]:
     #                    agreeCover.append(combineFirst[element][c])
      #                   groupCover[element].append(agreeCover)
               #          print agreeCover
       #                  agreeCover = [combineFirst[element][c+1]]
        #                 c = c+ 1
                    
                         
         #           if combineFirst[element][c].split(".")[-1] != agreeCover[0].split(".")[-1]:
          #               agreeCover.append(combineFirst[element][c])
           #              c = c+ 1
                    
                    if combineFirst[element][c].split(".")[-2] == 's':
                         agreeCover.append(combineFirst[element][c])
                         c=c+ 1
                    if  combineFirst[element][c].split(".")[-2] == 'e':
                         
                         agreeCover = tuple(agreeCover)
                         if agreeCover != ():
                              groupCover[element].add(agreeCover)
                         
                         agreeCover = []
                         c =c+ 1
                         
#                    groupCover[element] = list(groupCover[element])
     newFile = open('combineFirst', 'w')
     for element in combineFirst:
 #         newFile.write("\t".join(element))      
  #        newFile.write("\t".join(combineFirst[element]))
   #       newFile.write("\n")
          

          gclist = list(groupCover[element])
     
          for item in gclist:
               newList = []
               for x in item:
                    #item is a tuple
                    index = sortedSE[element][0].index(x) 
                    newList.append((sortedSE[element][0][index].split(".")[0],sortedSE[element][1][index].split(".")[0])), 
          print element.split("+")[0] + "\t" + element.split("+")[1] + "\t " + newList[-1][0] + "\t" + newList[0][-1] + "\t" + str(len(newList)) + "\t" + str(newList)
main()
