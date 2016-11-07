import os
import JackTokenizer as jt
import CompilationEngineFinal as ce 
import SymbolTable as ST
import VMWriter
import sys 

input=sys.argv[1]
fileList=[]
if os.path.isdir(input):
    if input.endswith('/'):
        input=input[:-1]
    os.chdir(input)
    for file in os.listdir('.'):
        if file.endswith('.jack'):
            fileList.append(file)
elif os.path.isfile(input):
    fileList=[input]
else:
    raise Exception("Input should be either a file name or a directory name!")

for file in fileList:
    outFile=file.split('/')[-1].split('.')[0]+'.vm' 
    tokenizer=jt.JackTokenizer(file)
    table = ST.SymbolTable()
    vm = VMWriter.VMWriter(outFile)
    compiler=ce.CompilationEngine(tokenizer, table, vm)
    compiler.CompileClass()
