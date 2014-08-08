import time
import argparse
import sys
import os
import re

def main():

    # argparse is a python package for accepting and interpreting arguments
    # and toogling options
    parser = argparse.ArgumentParser()
    parser.add_argument("-s",  default = True, help="input is sam file; default True")
    parser.add_argument("fileName", type = str, help= "Name of the input SAM file")
    parser.add_argument("insert", type=int, nargs = '?', action = 'store', help = "user given insert size")
    parser.add_argument("stDev", nargs = '?', action='store', default=10, help = "Standard deviation")
    parser.add_argument("outPutName", type = str,action = 'store', help="name of the output file")

    args = parser.parse_args()
    fileName = args.fileName
    insertSize = args.insert
    sd = args.stDev
    outPut = args.outPutName
    print fileName
    print insertSize
    print sd
    if outPut == None:
        outPut = "linkedContigs"

    print outPut

    # searches for the imput file and checks if its is a SAM file
    # If not, parseSAM quits
    if (os.path.isfile(fileName) == False):
         sys.exit(fileName + " doesn't not exist")

    ext = os.path.splitext(fileName)[-1].lower()
    if (ext != ".sam"):
         sys.exit(fileName + " is not a SAM file.")

    readFile = open(fileName, 'r')

    # Creates a dictionary of contigs and their lengths. Uses Real expression
    contig_lengths = {}
    pattern = re.compile('SN:(?P<contig>\w+)\s*LN:(?P<length>\d+)')
    justLen = open('justLen.txt', 'w')
    for line in readFile:
        if line.startswith('@SQ'):
            matches = pattern.search(line)

            if len(matches.groups()) == 2:
                contig_lengths[matches.group('contig')]=  matches.group('length')
                justLen.write("\t".join(matches.group('contig') + " " +  matches.group('length')))
                justLen.write("\t".join("\n"))
        else:
            continue
    justLen.close()

    # jump back to the start of the file
    print "extract contigs lengths"
    readFile.seek(0)

    allReads = []
    numReads = 0
    for line in readFile:
        if line.startswith('@'):
            continue

        else:
            rowList = line.split()
            numReads = numReads + 1
            contigLength = 0
            dir = ""

            # reads without a contig are ignored
            # maybe pipe them into a file for reference later
            if rowList[2] != '*':                       
                contigLength = int(contig_lengths[rowList[2]])

                # For now, only worry about if the read is for/rev
                if int(rowList[1]) == 16:
                    # position is the left most base and the start of the contig
                    # offset are the ends of the contig closer to the read
                    offset = int(rowList[3])
                    dir = "rev"
                elif int(rowList[1]) == 0:
                    offset = contigLength - int(rowList[3])
                    dir = "for"
            elif int(rowList[1]) == 4:
                offset = "remove"

            # contig, offset,read,readLen, position            
            allReads.append([rowList[2], str(offset), rowList[0], str(len(rowList[9])), rowList[3], rowList[8], dir])
    print str(numReads) + " reads total"                      
                        
    # by sorting by fragment ID, reads are kept together
    allReads = sorted(allReads, key = lambda x: x[2][5:])
    print "Done Sorting"

    numPartMap = 0
    numWholeFrag = 0    
    listFrag = []
    total = 0    
    numIS = 0


    for i in range(len(allReads)):
        # keeps contigs in pairs
        if (i+1) <= len(allReads) and i%2 == 0:

            contig1 = allReads[i][0]
            contig2 = allReads[i+1][0]
            if contig1 == contig2:
                # If the reads are on the same contig, they are used to 
                # calculate average Insert Size
                # The absolute value of the difference of positions plus the length of read 2
                if allReads[i][6] == "for" and allReads[i+1][6] == "rev":
                    pos1 = allReads[i][4]
                    pos2 = allReads[i+1][4]
                    extraLen = allReads[i+1][3]
                elif allReads[i][6] == "rev" and allReads[i+1][6] == "for":
                    pos2 = allReads[i][4]
                    pos1 = allReads[i+1][4]
                    extraLen = allReads[i][3]
                    temp = allReads[i][4]
                    allReads[i][4] = allReads[i+1][4]
                    allReads[i+1][4] = temp
                total = total +abs(int(pos1)-int(pos2))+int(extraLen)
                
                #counts the number of InsertSize calculated and later used for 
                #average
                numIS = numIS + 1

            if (contig1 != '*' and contig2 != '*') or ( allReads[i][1] != "remove" and allReads[i+1][1] != "remove"):
                #only adds the fragments that have both reads mapped to a contig
                if allReads[i][6] == "for":
                    listFrag.append(allReads[i])
                    listFrag.append(allReads[i+1])
                elif allReads[i][6] == "rev":
                    listFrag.append(allReads[i+1])
                    listFrag.append(allReads[i])

                # Number of Whole Fragments are kept track of
                numWholeFrag = numWholeFrag + 1

            else:
                numPartMap = numPartMap + 1

    if type(insertSize) != int:
        
        print "calculating avgIS"
        print "total is " + str(total)
        print "numIS is " + str(numIS)
        avgIS = total/numIS
        print "avgIS is " + str(avgIS)
    else:
        print "User based IS"
        avgIS = insertSize

        
        
    print str(numPartMap) + " number of partially mapped fragments"
    print str(numWholeFrag) + " number of fully mapped reads"
    
    linkedContigs = open(outPut+'.txt', 'w')
    numLinkContig = 0
    for i in range(len(listFrag)):
        if (i+1) <= len(listFrag) and i%2 == 0:
            if str(listFrag[i][0]) != str(listFrag[i+1][0]):
                numLinkContig = numLinkContig + 1               
                gap = int(avgIS)-int(listFrag[i][1])-int(listFrag[i+1][1])
                
                linkedContigs.write("\t".join([listFrag[i][0],listFrag[i+1][0],listFrag[i+1][2][:-2], str(gap -int(listFrag[i+1][3])-int(sd)*avgIS/100), str(gap -int(listFrag[i+1][3])+ int(sd)*avgIS/100)]))
                linkedContigs.write("\t".join("\n"))
             
    print str(numLinkContig) + " number of reads bridging contigs"          
    linkedContigs.close()
main()
