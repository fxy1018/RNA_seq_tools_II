'''
Created on Jul 24, 2017

@author: XFan

'''

from rna_seq_tools.Quantifier import *
from rna_seq_tools.FileDealer import *
import multiprocessing
import os


def countFun(b, gtfFile):
    q = Quantifier()
    name = b.fileName.strip("Aligned.out.bam.gz")
    name += "_count.txt"
    outFile = FileObj(directory="/home/xfan/htseqTest/", name=name)
    q.countRead(b, gtfFile, outFile)

def processFun(fs, gtfFile):
    for b in fs:
        countFun(b, gtfFile)

if __name__ == "__main__":
    exp  = "IWP0003JJ"
    dirs = os.listdir("/data/cofactor_genomics/IWP0003JJ/alignment/genome/")
    
    bamroot = "/data/cofactor_genomics/IWP0005JJ/alignment/genome/"
    bamFiles = []
    
    gtfFile = FileObj(directory="/data/cofactor_genomics/reference/annotation/", name = "Homo_sapiens.GRCh38.89.gtf")
    
    for d in dirs:
        path = bamroot + d
        f = d.rstrip("_aligned")
        fileName = f + "edAligned.out.bam.gz"
        fileObj = FileObj(path, fileName)
        bamFiles.append(fileObj)
 
    file_list = {0:[],1:[],2:[]}
    count = 0
    for b in bamFiles:
        if count <2:
            file_list[count].append(b)
        else:
            file_list[count].append(b)
            count = 0
    
    for fs in file_list:
        p = multiprocessing.Process(target = processFun, args = (file_list[fs], gtfFile))
        p.start()


