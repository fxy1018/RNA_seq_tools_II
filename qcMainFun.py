'''
Created on Jul 14, 2017

@author: XFan
'''
from rna_seq_tools.FileDealer import *
from rna_seq_tools.QualityController import *
import os
import multiprocessing
import sys


def fastqc(expNum, f):
    data_root = '/home/ubuntu/RNA_Seq/'
    fastqc_root = '/home/ubuntu/qcTest'
    
    data_path = os.path.join(data_root, expNum, f)
    qcResult_path = os.path.join(fastqc_root, expNum )
    qcControl = QualityController()
    qcControl.FastQC(data_path, qcResult_path)

def fastqcTrimmed(expNum, trimmedSeqFiles):
    #view quality of trimmed seq data 
    data_root = '/home/ubuntu/RNA_Seq/'
    fastqc_root = '/home/ubuntu/qcTest'
    
    for i in trimmedSeqFiles:
        data_path = os.path.join(data_root, expNum,"trimmed", i)
        qcResult_path = os.path.join(fastqc_root, expNum, "trimmed")
        qcControl = QualityController()
        qcControl.FastQC(data_path, qcResult_path)

def getFastqcReport(expNum):
    #view quality of original seq data 
    data_root = '/home/ubuntu/RNA_Seq/'
    fastqc_root = '/home/ubuntu/qcTest'
    seqFiles = getSeqFiles(data_root, expNum)
    fastqcReport(fastqc_root, expNum, seqFiles) 

def trimAdpator(expNum, file):
    # trim adpator 
    outroot = os.path.join("/home/ubuntu/RNA_Seq", expNum, "trimmed")
    encoding = "33"
    infile = os.path.join("/home/ubuntu/RNA_Seq", expNum, file)
    trimQC = SingleEndQualityController()
    trimQC.TrimmomaticAdaptor(outroot, encoding, infile)

def trimLowScore(expNum, file):
    # trim low score base 
    outroot = os.path.join("/home/ubuntu/RNA_Seq", expNum, "trimmed")
    encoding = "33"
    infile = os.path.join("/home/ubuntu/RNA_Seq", expNum, file)
    trimQC = SingleEndQualityController()
    trimQC.TrimmomaticLowScore(outroot, encoding, infile)

def trimLowScoreAdpator(expNum, file):
    # trim low Score and adaptor
    outroot = os.path.join("/home/ubuntu/RNA_Seq", expNum, "trimmed")
    encoding = "33"
    infile = os.path.join("/home/ubuntu/RNA_Seq", expNum, file)
    trimQC = SingleEndQualityController()
    trimQC.TrimmomaticLowScoreAdaptor(outroot, encoding, infile)



def filterrRNA(expNum, f):
    #to filter out rRNA from raw reads
    qc = QualityController()
    ref_root = "/home/ubuntu/RNA_Seq/reference/rRNA"
    refs = ["rfam_5s_id98.fasta", "rfam_5.8s_id98.fasta", "silva_euk_28s_id98.fasta", "silva_euk_18s_id95.fasta"]
    refObjs = []
    for r in refs:
        file = FileObj(ref_root, r)
        refObjs.append(file)
      
    index_root = "/home/ubuntu/RNA_Seq/reference/rRNA/sortmeRNA_index"
    indexs = ["rfam_5s_id98_db", "rfam_5.8s_id98_db", "silva_euk_28s_id98_db", "silva_euk_18s_id95_db"]
    indexObjs = []
    
    for i in indexs:
        file = FileObj(index_root, i)
        indexObjs.append(file)
    
    path = os.path.join("/home/ubuntu/RNA_Seq", expNum, "trimmed")
    readObj = FileObj(path, f)
    qc.sortmerna(refObjs, indexObjs, readObj)
 
def processFun(expNum, fs):
    for f in fs:
        fastqc(expNum, f)
        #trimLowScore(expNum,f)
        #filterrRNA(expNum, f)

if __name__ == "__main__" :
    
    expNum = sys.argv[1]
    n = int(sys.argv[2])
     
    #view quality of original seq data 
    data_root = '/home/ubuntu/RNA_Seq/'
    fastqc_root = '/home/ubuntu/qcTest'
    files = getSeqFiles(data_root, expNum)
     
    #trimmed files  
    #files = os.listdir("/home/ubuntu/RNA_Seq/" + expNum + "/trimmed")
    
    file_list = {}
    for i in range(n):
        file_list[i] = []
    count = 0
    for f in files:
        if ".fastq.gz" in f:
            if count < n-1:
                file_list[count].append(f)
                count += 1
            else:
                file_list[count].append(f)
                count = 0
    for k in file_list:
        p = multiprocessing.Process(target = processFun, args=(expNum, file_list[k]))    
        p.start()
     
    
    