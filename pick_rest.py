#!/usr/bin/python
import subprocess
import sys


m = sys.argv[1]
f = sys.argv[2]
p = sys.argv[3]
#a1 = subprocess.Popen(["ls", f], stdout=subprocess.PIPE)
#(x1, y) = a1.communicate()
#print x1.split("\n")

#path1, err = (subprocess.Popen(["pwd"], stdout=subprocess.PIPE)).communicate()
#print path1

a2 = open(m).readlines()
gene_list = [base.split("\t")[7] for base in a2[1:]]
#print len(gene_db), len(set(gene_db))
gene_db = list(set(gene_list))
#print gene_db

def pick_mts(x):
    a3 = open(f).readlines()
    other_list = []
    for each in a3:
        for every in gene_db:
            if every in each:
                other_list.append(each)
    return other_list

#ofiles = x1.strip().split("\n")
#for each in ofiles:
#    print each
y = pick_mts(f.strip())
if len(y) > 0:
    open(p+"_rGmts", "w+").writelines("".join(y))
