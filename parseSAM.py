import sys
import os
def main():
    
    fileName = sys.argv[1]

    if (os.path.isfile(fileName) == False):
         sys.exit(fileName + " doesn't not exist")

    ext = os.path.splitext(fileName)[-1].lower()

    if (ext != ".sam"):
         sys.exit(fileName + " is not a SAM file.")

    masterList = []
    readFile = open(fileName, 'r')
    allReads = []
    numReads = 0
    print "Reading SAM file"
    for line in readFile:

        # Trim the header
        if line.startswith('@'):
            continue
        #Ignores everything but the reads

        else:
            rowList = line.split()
            numReads = numReads + 1
            allReads.append([rowList[2], rowList[0], rowList[0][:-2\
]])
            # adds reads to list, but only contig, read, and fragID
    print str(numReads) + "reads total"

    readFile.close()
    allReads = sorted(allReads, key = lambda x: int(x[2][5:]))
    # sort by fragment ID
    
    print "Done Sorting"

    numPartMap = 0
    numWholeFrag = 0
    
    listFrag = []
        
    for i in range(len(allReads)):
        if (i+1) <= len(allReads) and i%2 == 0:
            if allReads[i][0] != '*' and  allReads[i+1][0] != '*':
                # only adds the fragments that have both reads mapped to a contig
                
                listFrag.append(allReads[i])
                listFrag.append(allReads[i+1])
                
                numWholeFrag = numWholeFrag + 1
            else:
                numPartMap = numPartMap + 1

        
    
    print str(numPartMap) + "number of partially mapped fragments"
    print str(numWholeFrag) + "number of fully mapped reads"

    linkedContigs = open('linkedContigs.txt', 'w')

    for i in range(len(listFrag)):
        if (i+1) <= len(listFrag) and i%2 == 0:
            if listFrag[i][0] != listFrag[i+1][0]:
                linkedContigs.write("\t".join([listFrag[i][0],listFrag[i+1][0],listFrag[i+1][2]]))
                linkedContigs.write("\t".join("\n"))
                
                # find all fragments that bridge more than one contig

    linkedContigs.close()


main()
