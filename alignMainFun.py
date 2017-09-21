'''
Created on Jul 21, 2017

@author: XFan
'''


from rna_seq_tools.FileDealer import *
from rna_seq_tools.Aligner import *
import os
import multiprocessing
import sys
from numpy import integer

def starAlign(expNum, seq_file):
    aligner = Aligners()
    index_dir = "/data/cofactor_genomics/reference/hg38/STAR_index"
    gtf = FileObj("/data/cofactor_genomics/reference/annotation", "Homo_sapiens.GRCh38.89.gtf")
    path = os.path.join('/data/cofactor_genomics/', expNum, 'rRNA_filtered')
    readObj = FileObj(path, seq_file)
    base_file = seq_file.strip("_non_rRNA.fastq.gz")
    dir_name = base_file + "_aligned"
    out_path = os.path.join("/data/cofactor_genomics/", expNum, "alignment/genome/", dir_name)
    out_dir = FileObj(out_path, base_file)
    print(readObj.path)
    print(out_dir.path)
    aligner.STAR(index_dir, readObj, gtf, out_dir)
 
def processFun(expNum,fs):
    for f in fs:
        starAlign(expNum, f)

if __name__ == "__main__":
    # get args from commind line, first arg is experiment number
    # and the second args is number of process
    expNum = sys.argv[1]
    n = int(sys.argv[2])
     
    files = os.listdir("/home/ubuntu/RNA_Seq/" + expNum + "/rRNA_filtered")
    
    file_list = {}
    for i in range(n):
        file_list[i] = []
    
    count = 0
    for f in files:
        if "_non_rRNA.fastq.gz" in f:
            if count < n-1:
                file_list[count].append(f)
                count += 1
            else:
                file_list[count].append(f)
    
    for k in file_list:
        p = multiprocessing.Process(target=processFun, args = (expNum, file_list[k]))
        p.start()

    
            
    

 