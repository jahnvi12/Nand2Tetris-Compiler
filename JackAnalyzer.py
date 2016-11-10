import os
import JackTokenizer as jt
import CompilationEngineFinal as ce 
import SymbolTable as ST
import VMWriter
import FuncTable
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

fntable = FuncTable.FuncTable()

for file in fileList:
    inpname = file.split('/')[-1].split('.')[0]
    outFile = inpname + '.vm' 
    tokenizer=jt.JackTokenizer(file)
    table = ST.SymbolTable()
    vm = VMWriter.VMWriter(outFile)
    compiler=ce.CompilationEngine(tokenizer, table, vm, inpname, fntable)
    compiler.CompileClass()

if not fntable.isemptyundec():
    print fntable.undecfnlist
    raise Exception("Undefined function(s) used in program!!!")

