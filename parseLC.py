B0;136;0cimport argparse
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

     sortedLC = {}
     for element in linkedContig:
          # labels start and ends
          gMin = [ x[0]+".s" for x in list(linkedContig[element])]
          gMax = [ y[1]+".e" for y in list(linkedContig[element])]
          
     
          for i in range(len(gMin)):
               # labels each link
               gMin[i] = gMin[i]+"."+str(i+1)
               gMax[i] = gMax[i]+"."+str(i+1)
          

          # sorts by the actually gap value
          sortMin = sorted(gMin, key = lambda x: int(x.split(".")[0]))
          sortMax = sorted(gMax, key = lambda x: int(x.split(".")[0]))
               
          # Now a dictionary has a list of starts and list of ends
          sortedLC[element] = [sortMin, sortMax]
     
     groupOfCoverage = {}
     for element in sortedLC:
          for i in range(len( sortedLC[element])):
               temp = sortedLC[element]
          
               #should this be here or before the for loop

               coverageLow = temp[0][-1]
          
               coverageHigh = temp[1][i]
          
               #len temp[0] and temp[1] are the same
               agreeGaps = []
               if (i+1) <= len(temp[0]):

                    # _____________           Overlap on the right
                    #       ________________
                    # if s2 is >= s1 / e1 is main, s2 is main


                    #    _____________        overlap on the left
                    #___________
                    # if s2 <= s1 and e2 <= e1 / e2 is main, s1 is main


                    #__________________       complete overlap
                    #     ________
                    # if s2 >= s1 and e2 <= e1 / e2 is main, s2 is main


                    # __________ 
                    #             __________  no overlap >>> new set of agreeing gaps
                    #


                    #
                    #

                    if temp[0][i+1].split"."[0] > temp[0][i].split"."[0]:
                         coverageLow = temp[0][i+1].split"."[0]
                    if temp[1][i+1].split"."[0] > temp[i][i].split"."[0]:
                         coverageHigh = temp[i][i+1].split"."[0]

                    
main()
