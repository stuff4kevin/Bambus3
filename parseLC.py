import argparse
import sys
import os

def main():
     # argpase is a python package for accepting and interpreting arguments
     # and toogle through options
     parser = argparse.ArgumentParser()
     parser.add_argument("fileName", type = str, help= "Name of parseSAM output, usually linkedContigs.txt")
     args = parser.parse_args()
     fileName = args.fileName

     file = open(fileName, 'r')
     linkedContig = {}

     #extracts the gMin and gMax into a dictionary by bridging contigs
     for line in file:
               
          rowList = line.split()
          pairing = rowList[0]+"+"+rowList[1]
          otherPair = rowList[1]+"+"+rowList[0]
          min = rowList[3]+"."+rowList[2]+"."+"min"
          max = rowList[4]+"."+rowList[2]+"."+"max"

          if pairing not in linkedContig and otherPair not in linkedContig:
               linkedContig[pairing] = [(min,max)]

          elif pairing not in linkedContig and otherPair in linkedContig:
               linkedContig[otherPair].append((min,max))
          
          elif pairing in linkedContig:
               linkedContig[pairing].append((min,max))
          


     sortedSE = {}
     combineFirst = {}
     for element in linkedContig:
          # seperates the gMin/Max and recombines them, sorting by value from least to greatest
          gMin = [ x[0] for x in linkedContig[element]]
          gMax = [ y[1] for y in linkedContig[element]]
          combineFirst[element] = sorted(gMin+gMax, key = lambda x: int(x.split(".")[0]))

          # for later reference, easily call back gMin with gMax
          sortedSE[element] = [gMin, gMax]
          # In the bash script, the printed lines are pipe this into temp5 for reference later
          print element
          print len(combineFirst[element])
          print combineFirst[element]

     # groups together the fragments that agree on a gap range
     # Each contig can have multiples
     groupCover = {}
     for thing in combineFirst:
          groupCover[thing] = []
          i = 0
          
          while i < len(combineFirst[thing]):
               agreeCover = []
               c = i
               listOfMin = []

               while c < len(combineFirst[thing]):
                    # if the current step is a min, add it to the list of agreeingFragment and note which fragment is it
                    if combineFirst[thing][c].split(".")[-1] == "min":
                         agreeCover.append(combineFirst[thing][c])
                         listOfMin.append(int(combineFirst[thing][c].split(".")[1][5:]))
                         c=c+ 1

                    # For every min, there is a max. Whena max with an agreeing min, that set is completed and added to groupCover
                    # another set is prepared and the search continues with the next min
                    # Maxs are consider for ending a set
                    elif combineFirst[thing][c].split(".")[-1] == "max" and int(combineFirst[thing][c].split(".")[1][5:]) in listOfMin: 
                         if len(agreeCover) != 0:
                              groupCover[thing].append(tuple((agreeCover)))
                              listOfMin = []
                              agreeCover = []
          
                         i = c
                         break

                    # Since the max are not considered in what is an agree set, thy are skipped over
                    elif combineFirst[thing][c].split(".")[-1] == "max" and int(combineFirst[thing][c].split(".")[1][5:]) not in listOfMin:
                         c = c+ 1

                    # In case the list reacts the end without fulfilling the above conditions, a current set is finalized
                    elif c == len(combineFirst[thing])-1:
                         if len(agreeCover) != 0:
                              groupCover[thing].append(tuple((agreeCover)))
                              agreeCover = []
                         c =c+ 1
                    i = i + 1
          groupCover[thing] = set(groupCover[thing])

     # Below is just a setup for a readable layout in the final output of parseLC
     final = []
     for stuff in groupCover:          
          gclist = list(groupCover[stuff])

          for item in gclist:
               
               gapList = []
               fragList = []
               for x in item:
                    index = sortedSE[stuff][0].index(x) 
                    gapList.append([str(sortedSE[stuff][0][index]),str(sortedSE[stuff][1][index])]) 
                    fragList.append(sortedSE[stuff][0][index].split(".")[1])
                    
               fragList = sorted(fragList, key = lambda x: int(x[5:]))

               newList = []
               for pairs in gapList:
                    tempString = "(" + ",".join(pairs) + ")"
                    newList.append(tempString)
               final.append((stuff.split("+")[0], stuff.split("+")[1], gapList[-1][0].split(".")[0], gapList[0][-1].split(".")[0], len(gapList), " ".join(newList)))

     final = set(final)
     tempWriter = open('contigGapList.txt', 'w')
     for printLine in final:
          tempWriter.write("\t".join(str(e) for e in printLine))
          tempWriter.write("\t".join("\n"))

     tempWriter.close()
main()
