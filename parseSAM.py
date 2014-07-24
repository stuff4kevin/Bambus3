import time
import argparse
import sys
import os
import re

def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-s",  default = True, help="input is sam file; default True")

    parser.add_argument("fileName", type = str, help= "Name of the input SAM file")
    
    parser.add_argument("insert", type=int, nargs = '?', action = 'store', help = "user given insert size")
    parser.add_argument("stDev", nargs = '?', action='store', default=10, help = "Standard deviation")

    parser.add_argument("outPutName", type = str, help="name of the output file")
    args = parser.parse_args()
    fileName = args.fileName
    insertSize = args.insert
    sd = args.stDev
    outPut = args.outPutName
    print fileName
    print insertSize
    print sd
    print outPut
    ts = time.ctime()
    print ts
    if (os.path.isfile(fileName) == False):
         sys.exit(fileName + " doesn't not exist")

    ext = os.path.splitext(fileName)[-1].lower()
    if (ext != ".sam"):
         sys.exit(fileName + " is not a SAM file.")

    readFile = open(fileName, 'r')
    allReads = []
    numReads = 0
    ts = time.ctime()
    print ts
    print "Reading SAM file"

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
    ts = time.ctime()
    print ts

    print "extract contigs lengths"
    readFile.seek(0)

    justContig = [ x[0] for x in contig_lengths]
    justLength = [x[1] for x in contig_lengths]
    ts = time.ctime()
    print ts
    for line in readFile:

        # Trim the header
        if line.startswith('@'):
            continue

        else:
            rowList = line.split()
            numReads = numReads + 1
            contigLength = 0
            dir = ""
            if rowList[2] != '*':
                                   
                contigLength = int(contig_lengths[rowList[2]])
                if int(rowList[1]) == 16:
                    #reverse
                    offset = int(rowList[3])
                    dir = "rev"
                elif int(rowList[1]) == 0:
                    offset = contigLength - int(rowList[3])
                    dir = "for"
            elif int(rowList[1]) == 4:
                offset = "remove"

            # contig, offset,read,readLen, and position            
            allReads.append([rowList[2], str(offset), rowList[0], str(len(rowList[9])), rowList[3], rowList[8], dir])
    ts = time.ctime()
    print ts    
    print str(numReads) + " reads total"                      
                        
    allReads = sorted(allReads, key = lambda x: x[2][5:])
    # sort by fragment ID
   # allReadFile = open('allRead.txt', 'w')
    #for element in allReads:
     #   allReadFile.write("\t".join(element))
    #    allReadFile.write("\t".join("\n"))
    #allReadFile.close()
    print "Done Sorting"

    
    numPartMap = 0
    numWholeFrag = 0
    
    listFrag = []
    total = 0    
    numIS = 0
    ts = time.ctime()
    print ts
    #sameContig = open('sameContig.txt','w')
    for i in range(len(allReads)):
        if (i+1) <= len(allReads) and i%2 == 0:

            contig1 = allReads[i][0]
            contig2 = allReads[i+1][0]
            if contig1 == contig2:
     #           sameContig.write("\t".join(allReads[i]))
      #          sameContig.write("\t".join("\n"))
       #         sameContig.write("\t".join(allReads[i+1]))
        #        sameContig.write("\t".join("\n"))
                total = total +abs(int(allReads[i][4])-int(allReads[i+1][4]))+int(allReads[i+1][3])
                numIS = numIS + 1

            if contig1 != '*' and contig2 != '*' and allReads[i][1] != "remove" and allReads[i+1][1] != "remove":
                #only adds the fragments that have both reads mapped to a contig
 
                listFrag.append(allReads[i])
                listFrag.append(allReads[i+1])
                
                numWholeFrag = numWholeFrag + 1

            else:
                numPartMap = numPartMap + 1

    #sameContig.close()
    ts = time.ctime()
    print ts
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
    ts = time.ctime()
    print ts
    numLinkContig = 0
    for i in range(len(listFrag)):
         if (i+1) <= len(listFrag) and i%2 == 0:
             if str(listFrag[i][0]) != str(listFrag[i+1][0]):
                 numLinkContig = numLinkContig + 1               
                 gap = int(avgIS)-int(listFrag[i][1])-int(listFrag[i+1][1])
                 
                 linkedContigs.write("\t".join([listFrag[i][0],listFrag[i+1][0],listFrag[i+1][2][:-2], str(gap -int(sd)*avgIS/100), str(gap + int(sd)*avgIS/100)]))
                 linkedContigs.write("\t".join("\n"))
             
    print str(numLinkContig) + " number of reads bridging contigs"          
    linkedContigs.close()
    ts = time.ctime()
    print ts
main()
