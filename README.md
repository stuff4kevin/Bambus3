Bambus3
=======
programs:
Just run the bash.sh
parseSAM is for the initial sam file
parseLC is for the sorted output of parseSAM
finalOutput is an extra steps to remove subsets of concensus fragment groups

outputs:
linkedContigs is in the form : Contig1, contig1, fragment, gapMin, gaMax
temp is the sorted for of linkedContigs
contigGapList.txt has the fragments grouped together
temp5 is for reference that helps lead to contigGapList.txt
temp2 is contigGapList.txt sorted
temp3 is a temp2 with repeated groups removed (not entirely sure if this step is needed anymore)
final is all the negative gap Rangs removed (only used for networkx for simplicity)
