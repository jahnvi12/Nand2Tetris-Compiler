import os
import JackTokenizer as jt
import CompilationEngine as ce 
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
    compiler=ce.CompilationEngine(outFile,tokenizer)
    compiler.compileClass()