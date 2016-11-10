#VM Writer

class VMWriter(object):

        def __init__(self, outfile):
            self.vm = open(outfile, "w+")

        def writePush(self, segment, index):
            if segment == "field":
                self.vm.write('push this %d\n' %(index)) 
            else:
                self.vm.write('push %s %d\n' %(segment, index)) 

        def writePop(self, segment, index):
            if segment == "field":
                self.vm.write('pop this %d\n' %(index)) 
            else:
                self.vm.write('pop %s %d\n' %(segment, index)) 

        def writeArithmetic(self, command):
            self.vm.write(command.lower()+'\n')

        def writeLabel(self, label):
            self.vm.write ('label %s\n' %(label)) 

        def writeGoto(self, label):
            self.vm.write('goto '+label+'\n')

        def writeIf(self, label):
            self.vm.write('if-goto '+label+'\n')

        def writeCall(self, name, nArgs):
            self.vm.write('call %s %d\n' %(name, nArgs)) 

        def writeFunction(self, name, nLocals):
            self.vm.write('function %s %d\n' %(name, nLocals)) 

        def writeReturn(self):
            self.vm.write('return\n')

        def close(self):
            self.vm.close()
            '''
            v = VMWriter('vmcode.txt')
            v.writePush('local', 0)
            v.writePop('argument', 0)
            v.writeArithmetic('ADD')
            v.writeLabel('LOOP')
            v.writeGoto('LOOP')
            v.writeIf('END')
            v.writeCall('foo', 2)
            v.writeFunction('bar', 1)
            v.writeReturn()
            v.close()
            '''
