python parseSAM.py lib1.sam 3 linkedContigs
sort -k1 linkedContigs.txt > temp
python parseLC.py temp > temp2
sort -rk5 temp2 | awk '$5 > 1' | awk '$3 > 0' | awk '$4 > 0' > final.txt
