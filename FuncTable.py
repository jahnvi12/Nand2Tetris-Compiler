class FuncTable:
    def __init__(self):
        self.decfnlist=[]
        self.undecfnlist=[]
        self.adddecfn("Math","init")
        self.adddecfn("Math","abs")
        self.adddecfn("Math","multiply")
        self.adddecfn("Math","divide")
        self.adddecfn("Math","min")
        self.adddecfn("Math","max")
        self.adddecfn("Math","sqrt")
        self.adddecfn("String","new")
        self.adddecfn("String","dispose")
        self.adddecfn("String","length")
        self.adddecfn("String","charAt")
        self.adddecfn("String","setCharAt")
        self.adddecfn("String","appendChar")
        self.adddecfn("String","eraseChar")
        self.adddecfn("String","intValue")
        self.adddecfn("String","setInt")
        self.adddecfn("String","backSpace")
        self.adddecfn("String","doubleQuote")
        self.adddecfn("String","newLine")
        self.adddecfn("Array","dispose")
        self.adddecfn("Array","new")
        self.adddecfn("Output","init")
        self.adddecfn("Output","moveCursor")
        self.adddecfn("Output","printChar")
        self.adddecfn("Output","printString")
        self.adddecfn("Output","printInt")
        self.adddecfn("Output","println")
        self.adddecfn("Output","backSpace")
        self.adddecfn("Screen","init")
        self.adddecfn("Screen","clearScreen")
        self.adddecfn("Screen","setColor")
        self.adddecfn("Screen","drawPixel")
        self.adddecfn("Screen","drawLine")
        self.adddecfn("Screen","drawRectangle")
        self.adddecfn("Screen","drawCircle")
        self.adddecfn("Keyboard","init")
        self.adddecfn("Keyboard","keyPressed")
        self.adddecfn("Keyboard","readChar")
        self.adddecfn("Keyboard","readLine")
        self.adddecfn("Keyboard","readInt")
        self.adddecfn("Memory","peek")
        self.adddecfn("Memory","init")
        self.adddecfn("Memory","poke")
        self.adddecfn("Memory","alloc")
        self.adddecfn("Memory","deAlloc")
        self.adddecfn("Sys","init")
        self.adddecfn("Sys","halt")
        self.adddecfn("Sys","error")
        self.adddecfn("Sys","wait")

    def adddecfn(self, fclass, fname):
        self.decfnlist.append((fclass,fname))

    def addundecfn(self, fclass, fname):
        self.undecfnlist.append((fclass,fname))

    def removeundecfn(self,fclass,fname):
        for i in self.undecfnlist:
            if fclass==i[0] and fname==i[1]:
                self.undecfnlist.remove((fclass,fname))

    def isemptyundec(self):
        if len(self.undecfnlist)==0:
            return True
        else:
            return False

    def printlist(self):                        #only for error checking
        print("undecfnlist\n")
        print(self.undecfnlist)
        print("decfnlist\n")
        print(self.decfnlist)

"""
    def adddecfn(self,fclass,fname):
        adds a declared function to list

    def addundecfn(self,fclass,fname):
        adds an unseen function to list

    def removeundecfn(self,fclass,fname):
        removes the unseen function from second table after declaration is seen
"""
