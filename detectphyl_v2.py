#!/usr/bin/python2.7

import sys
import os

### The input files ###########################
f1 = sys.argv[1] #francesc list of phylogenetic mutations
f2 = sys.argv[2] #annotated others file
f3 = sys.argv[3] #lineage predicted by RDanalyzer
f4 = sys.argv[4] #folder for var prediction
f5 = sys.argv[5] #Prefix for the output file

######### making a dictionary of the phylogenetic mutations ###################
a1 = open(f1).readlines()
a2 = dict(("\t".join((base.strip().split("\t"))[0:3]), base.strip().split("\t")) for base in a1)

####### Function for predicting the lineage as per dictionary created above ################
def lineage(p):
    ln = []
    for each in p:
        b2 = each.strip().split("\t")
        if "\t".join(b2[1:4]) in a2:
            c1 = a2["\t".join(b2[1:4])]
            ln.append("\t".join(c1+b2[9:13]))
    return ln

### Calling the function on the annotated others file ##########
b1 = (open(f2).readlines())[1:]
lin = lineage(b1)
#print lin

names = []
for every in lin:
    c1 = every.split("\t")
    if c1[5].split(".")[0] not in names and c1[5].split(".")[0] != "others":
        names.append(c1[5].split(".")[0])
    elif c1[5].split(".")[0] not in names:
        names.append(c1[5].split(".")[0])

######## Reading the output of RD analyzer ##########
rds = (open(f3).readlines())[8].split("Predicted_lineage:")
RDs = rds[1].lstrip(" ")
#print RDs
#print rds2

######### Making final prediction #############
prediction = ""
if len(names) >= 1:
    prediction +=  f5 + "\t"+ ",".join(names) + "\tRDs:\t" + RDs.replace(")","").replace("(","")
elif len(names) == 0:
    prediction += f5 + "\t-" + "\tRDs:\t" + RDs.replace(")","").replace("(","")

####### Writing the output files ########
a12 = os.listdir(f4)
#print a12
#print len(lin)
if f5+"_predicted" in a12 and len(lin) >= 1:
    amr = [base.strip() for base in open(f4+"/"+f5+"_predicted").readlines()]
    open(f5+"_GenPred","w+").writelines("\n".join([prediction, "phylogenetic_SNPs"]+lin+["","Resistance_confering_mutations"]+amr))
elif len(lin) >= 1:
#    print "yes"
    open(f5+"_GenPred", "w+").writelines("\n".join([prediction,"phylogenetic_SNPs"]+lin +["","Resistance_confering_mutations","None detected!!"]))
else:
    open(f5 + "_GenPred", "w+").writelines(
        "\n".join([prediction, "phylogenetic_SNPs"] + ["None detected!!"] + ["", "Resistance_confering_mutations" , "None detected!!"]))

