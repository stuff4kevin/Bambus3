date +"%T"
python parseSAM.py lib1.sam linkedContigs
date +"%T"
sort -k1,1n -k2,2n -k4,4n linkedContigs.txt > temp
python parseLC.py temp > temp5
date +"%T"
sort  -k1,1n -k2,2n -k5,5nr contigGapList.txt > temp2
python finalOutput.py temp2 > temp3
date +"%T"
sort -rnk5 temp3 | awk '$5 > 1' | awk '$3 > 0' | awk '$4 > 0' > final.txt