vmcode={'=':'eq','+':'add','-':'sub','&':'and','|':'or','~':'not','<':'lt','>':'gt'}

class CompilationEngine(object):

    def __init__(self, tokenizer, table, vm, inpname, functable):
        self.tokenizer=tokenizer
        self.table=table
        self.vm=vm
        self.labelSuffix=0
        self.classname = inpname
        self.functable = functable
        self.type=['int','char','boolean']
        self.function=['constructor','function','method']
        self.getNextToken()

    def peek(self):
        return self.tokenizer.tokenList[0]

    def gettag(self):
        return self.tokenizer.tokenType()

    def getinfo(self):
        return self.tokenizer.token

    def getNextToken(self):
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        else:
            raise Exception("Too less tokens to parse after %s"% self.getinfo())


    def CompileClass(self):
        #print "Compiling class..."
        if(self.getinfo() != 'class'):
            raise Exception('No class in given file: Invalid token \'%s\''%(self.getinfo()))
        self.getNextToken()

        if(self.gettag() != 'IDENTIFIER'):
            raise Exception('Invalid class name: %s'%(self.getinfo()))

        className=self.getinfo()
        self.table.Define(className,className,'class')

        self.getNextToken()

        if(self.getinfo() != '{'):
            raise Exception('Missing { : Invalid token: %s'%(self.getinfo()))

        self.getNextToken()

        while(self.getinfo() in ['static','field']):
            self.CompileClassVarDec()

        while(self.getinfo() in self.function):
            self.CompileSubroutine(className)

        if(self.getinfo() != '}'):
            raise Exception('Missing } : Invalid token: %s'%(self.getinfo()))

    def CompileClassVarDec(self):
        kind=self.getinfo()
        if not kind in ['static','field']:
            raise Exception('Invalid variable kind: %s'%(self.getinfo()))

        self.getNextToken()
        typ=self.getinfo()
        if typ not in self.type:
            #if not self.table.KindOf(typ)=='class':
            if not self.gettag() == "IDENTIFIER":
                raise Exception("Invalid variable type : %s"%typ)

        self.getNextToken()
        varName=self.getinfo()
        if not self.gettag()=='IDENTIFIER':
            raise Exception("Illegal identifier: %s"%varName)

        self.table.Define(varName,typ,kind)

        self.getNextToken()

        while self.getinfo()==',':
            self.getNextToken()
            varName=self.getinfo()
            if not self.gettag()=='IDENTIFIER':
                raise Exception("Illegal identifier: %s"%varName)
            self.table.Define(varName,typ,kind)
            self.getNextToken()

        if self.getinfo() != ';':
            raise Exception('; Missing!!')

        self.getNextToken()

    def CompileSubroutine(self,className):
        #print "Compiling Subroutine..."
        kind = self.getinfo()
        if kind not in self.function:
            raise Exception('Illegal function kind: %s' %kind)

        self.getNextToken()

        typ=self.getinfo()
        if typ not in self.type and not typ=='void':
            if not self.table.KindOf(typ)=='class':
                raise Exception("Invalid return type : %s"%typ)
            elif kind == 'constructor':
                if typ != className:
                    raise Exception("Return type of constructor has to be class name!")

        self.getNextToken()

        name=self.getinfo()
        self.functable.removeundecfn(self.classname, name)
        self.functable.adddecfn(self.classname, name)

        if not self.gettag()=='IDENTIFIER':
            raise Exception("Illegal identifier for function name: %s"%name)

        self.table.Define(name, className, kind)
        self.table.startSubroutine()
        self.getNextToken()

        if self.getinfo() != '(':
            raise Exception("Missing ( for function : %s"%name)
        self.getNextToken()
        self.CompileParameterList(kind)

        if self.getinfo() != ')':
            raise Exception("Missing ) for function : %s"%name)

        self.getNextToken()

        if self.getinfo() != '{':
            raise Exception("Missing { for function : %s"%name)

        self.getNextToken()
        #print self.getinfo()

        while(self.getinfo() == 'var'):
            self.CompileVarDec()

        self.vm.writeFunction(className+'.'+name,self.table.VarCount('local'))

        if kind=='constructor':
            ###check formula to calculate size of object--->
            size=self.table.VarCount('field')
            self.vm.writePush('constant',size)
            self.vm.writeCall('Memory.alloc',1) 
            self.vm.writePop('pointer',0)
            if kind=='method':
                self.vm.writePush('argument',0) 
                self.vm.writePop('pointer',0) 

        #print self.getinfo()
        self.CompileStatements()
        #self.getNextToken()

        if self.getinfo() != '}':
            raise Exception("Missing } for function : %s"%name)

        self.getNextToken()


    def CompileParameterList(self,routine):
        #print self.getinfo()
        kind = 'argument'
        if routine == 'method':
            self.table.Define('this', None, kind)

        if self.getinfo()==')':
            return

        typ=self.getinfo()

        if typ not in self.type:
            if not self.gettag() == "IDENTIFIER":
                raise Exception("Invalid argument type of: %s"%(self.getinfo()))

        self.getNextToken()

        if not self.gettag() == "IDENTIFIER":
            raise Exception("Invalid argument name of: %s"%(self.getinfo()))

        self.table.Define(self.getinfo(), typ, kind)

        self.getNextToken()

        while not self.getinfo() == ')':
            if self.getinfo() != ',':
                raise Exception("Missing , before %s"%(self.getinfo()))
            self.getNextToken()
            typ=self.getinfo()
            if typ not in self.type:
                if not self.gettag() == "IDENTIFIER":
                    raise Exception("Invalid argument type of: %s"%(self.peek()))

            self.getNextToken()
            if not self.gettag() == "IDENTIFIER":
                raise Exception("Invalid argument name of: %s"%(self.getinfo()))

            self.table.Define(self.getinfo(), typ, kind)
            self.getNextToken()

    def CompileVarDec(self):
        #print "Compiling Variable Declaration Statement..."
        if self.getinfo() != 'var':
            raise Exception("Illegal type %s"%(self.getinfo()))

        self.getNextToken()   

        typ=self.getinfo()
        if typ not in self.type:
            if not self.gettag() == "IDENTIFIER":
                raise Exception("Invalid type : %s"%(self.getinfo()))

        self.getNextToken()
        varName=self.getinfo()
        if not self.gettag() == "IDENTIFIER":
            raise Exception("Invalid varname : %s"%(self.getinfo()))
        self.table.Define(varName, typ, 'local')
        self.getNextToken()

        while not self.getinfo() == ';':
            if self.getinfo() !=',':
                raise Exception(", or ; expected in variable declaration")
            self.getNextToken()
            varName = self.getinfo()

            self.table.Define(varName, typ, 'local') 
            self.getNextToken()       

        self.getNextToken()       
        #print self.getinfo()

    def CompileStatements(self):
        while(self.getinfo() in ['let','if','while','do','return']):
            if(self.getinfo()=='let'): 
                self.CompileLet()
            elif (self.getinfo()=='if'): 
                self.CompileIf()
            elif (self.getinfo()=='while'): 
                self.CompileWhile()
            elif (self.getinfo()=='do'): 
                self.CompileDo()
            elif (self.getinfo()=='return'): 
                self.CompileReturn()

    def CompileLet(self):
        #print "Compiling Let Statement..."
        self.getNextToken()

        token=self.getinfo()

        if not self.gettag() == "IDENTIFIER":
            raise Exception('Wrong variable name %s in let' %(self.getinfo()))

        segment = self.table.KindOf(token)
        index= self.table.IndexOf(token)
        self.getNextToken()

        if self.getinfo() == '[' :
            self.getNextToken()
            self.CompileExpression()

            if(self.getinfo()!=']'):
                raise Exception('Missing ] in let')


            self.vm.writePush(segment,index)
            self.vm.writeArithmetic('add')

            self.getNextToken()
            if not self.getinfo() == '=' :
                raise Exception('Missing = in let ')

            self.getNextToken()
            self.CompileExpression()
            self.vm.writePop('temp',0)
            self.vm.writePop('pointer',1)
            self.vm.writePush('temp',0)
            self.vm.writePop('that',0)

        else:
            if not self.getinfo() == '=' :
                raise Exception('Missing = in let ')

            self.getNextToken()
            self.CompileExpression()
            self.vm.writePop(segment, index)

        if not self.getinfo() == ';' :
            raise Exception('Missing ; in let statement')

        self.getNextToken()
        #print self.getinfo()

    def CompileIf(self):
        #print "Compiling If Statement..."
        self.getNextToken()

        if not self.getinfo() == '(' :
            raise Exception('Missing ( in if condition ')

        self.getNextToken()
        self.CompileExpression()

        if not self.getinfo() == ')' :
            raise Exception('Missing ) in if condition ')


        true='IF_TRUE'+str(self.labelSuffix)
        false='IF_FALSE'+str(self.labelSuffix)
        end='END'+str(self.labelSuffix)
        self.labelSuffix=self.labelSuffix+1
        self.vm.writeIf(true)
        self.vm.writeGoto(false)
        self.vm.writeLabel(true)

        self.getNextToken()

        if not self.getinfo() == '{' :
            raise Exception('Missing { in if body ')

        self.getNextToken()
        self.CompileStatements()

        if not self.getinfo() == '}' :
            raise Exception('Missing } in if body ')

        self.getNextToken()

        if self.getinfo() == 'else':
            self.vm.writeGoto(end)
        self.vm.writeLabel(false)
        if self.getinfo() == 'else':
            self.getNextToken()
            if not self.getinfo() == '{' :
                raise Exception('Missing { in else body ')

            self.getNextToken()
            self.CompileStatements()

            if not self.getinfo() == '}' :
                raise Exception('Missing } in else body ')

            self.getNextToken()
            self.vm.writeLabel(end)



    def CompileDo(self):
        self.getNextToken()
        self.CompileTerm()

        self.vm.writePop('temp',0)		

        if self.getinfo() !=';' :
            raise Exception("Missing ; in do statement")

        self.getNextToken()


    def CompileWhile(self):
        #print "Compiling while loop..."
        loop='LOOP'+str(self.labelSuffix)
        end='END'+str(self.labelSuffix)
        self.labelSuffix=self.labelSuffix+1

        self.vm.writeLabel(loop)

        self.getNextToken()

        if not self.getinfo() == '(' :
            raise Exception('Missing ( in while loop condition')

        self.getNextToken()
        self.CompileExpression()

        if not self.getinfo() == ')' :
            raise Exception('Missing ) in while loop condition')

        self.vm.writeArithmetic('not') 
        self.vm.writeIf(end)

        self.getNextToken()

        if not self.getinfo() == '{' :
            raise Exception('Missing { in while loop body')

        self.getNextToken()
        self.CompileStatements()

        if not self.getinfo() == '}' :
            raise Exception('Missing } in while loop body')

        self.vm.writeGoto(loop)
        self.vm.writeLabel(end)

        self.getNextToken()

    def CompileReturn(self):
        self.getNextToken()

        if self.getinfo()!=';' :
            self.CompileExpression()

        else:
            self.vm.writePush('constant',0)

        if self.getinfo()!=';' :
            raise Exception('Missing ; in return statement ')
        self.vm.writeReturn()

        self.getNextToken()

    def CompileExpression(self):
        if self.getinfo == '(':
            self.getNextToken()
            self.CompileExpression()
            if self.getNextToken() != ')':
                raise Exception('Missing ) in expression')

        else:
            self.CompileTerm()

        while(self.getinfo() in '+-*/&|<>='):
            token=self.getinfo()
            self.getNextToken()
            self.CompileTerm()
            if token == '/':
                self.vm.writeCall('Math.divide',2)
            elif token == '*':
                self.vm.writeCall('Math.multiply',2)
            else:
                self.vm.writeArithmetic(vmcode[token])

    def CompileExpressionList(self):
        if self.getinfo()==')':
            return 0
        nargs=1
        self.CompileExpression()

        while not self.getinfo() == ')': 
            if self.getinfo()!=',':
                raise Exception("Missing , in expression list")
            self.getNextToken()
            nargs=nargs+1
            self.CompileExpression()
        return nargs

    def CompileTerm(self):
        #self.outfile.write("locha ithe 2\n\n");

        #specs:
        #in case eof is encountere mid execution, returns -1.
        #else returns something else. same value as getnextline()
        #incase somewhere error is there, then that particular term is not printed.
        #the presentline is expected to hold the token from which the analysis is to start.
        token_tag = self.gettag()
        token = self.getinfo()

        #print self.getinfo()
        if token_tag == "INT_CONST":
            self.vm.writePush('constant', self.tokenizer.intVal())

        elif token_tag == 'STRING_CONST':
            self.vm.writePush('constant', len(token))          
            self.vm.writeCall('String.new', 1)               
            for char in token:
                self.vm.writePush('constant', ord(char))   
                self.vm.writeCall('String.appendChar', 2)            

        elif token_tag == 'KEYWORD':
            if token in ['false','null']:
                self.vm.writePush('constant', 0)
            elif token == 'true':
                self.vm.writePush('constant', 0)
                self.vm.writeArithmetic('not')
            elif token == 'this':
                self.vm.writePush('pointer', 0)             
            else:
                raise Exception('Unrecognized keyword: %s' %token)

        elif token_tag == 'SYMBOL':
            if token == '(':
                self.getNextToken()
                self.CompileExpression()
                if self.getinfo() != ')':
                    raise Exception("Missing ) in expression")

            elif token in ['-','~']:
                self.getNextToken()
                self.CompileTerm()
                if token == '-':
                    self.vm.writeArithmetic('neg')
                else:
                    self.vm.writeArithmetic('not')
                return
            else:
                raise Exception('Unrecognized symbol: %s' %token)

        elif token_tag == 'IDENTIFIER':
            nargs = 0
            name = token
            kind = self.table.KindOf(name)

            index = self.table.IndexOf(name)
            flag = 0
            for (a, b) in self.functable.decfnlist:
                if b == self.getinfo():
                    flag = 1
            if self.peek == '(' and not flag:
                self.functable.addundecfn(self.classname, self.getinfo())
            token = self.peek()
            if token == '(':
                #print token + ', ' + self.getinfo()
                self.vm.writePush('pointer',0) 
                self.getNextToken()
                self.getNextToken()
                #print self.getinfo()
                nargs= self.CompileExpressionList()+1

                if not self.getinfo() == ')' :
                    raise Exception("Missing ) in function call for %s" % name)
                className = self.classname
                self.vm.writeCall(className+'.'+name, nargs)

            elif token == '.':
                nargs=0    
                self.getNextToken()
                self.getNextToken()
                function = self.getinfo()
                flag = 0
                for (a, b) in self.functable.decfnlist:
                    if b == self.getinfo():
                        flag = 1
                if not flag:
                    if kind in ('field','local','static'): 
                        self.functable.addundecfn(self.table.TypeOf(name), self.getinfo())
                    else:
                        self.functable.addundecfn(name, self.getinfo())

                # Check if used for object or class
                if kind in ('field','local','static'): 
                    self.vm.writePush(kind,index)
                    nargs=1
                self.getNextToken()
                if not self.getinfo() == '(':
                    raise Exception("Missing ( in function call for %s" % function)
                self.getNextToken()

                nargs+=self.CompileExpressionList()
                if not self.getinfo() == ')':
                    raise Exception("Missing ) in function call for %s" % function)

                token_tag = self.table.TypeOf(name)

                if token_tag == None: 
                    token_tag = name 
                self.vm.writeCall('%s.%s' %(token_tag,function), nargs)    

            elif token == '[':
                type = self.table.TypeOf(self.getinfo())
                if type != "Array" and type != "String":
                    raise Exception("Accessing %s variable %s like Array element"%(type, name))
                self.getNextToken()
                self.getNextToken()
                self.CompileExpression()
                if not self.getinfo() == ']':
                    raise Exception("Missing ] in array element %s" % name)
                self.vm.writePush(kind,index)
                self.vm.writeArithmetic('add')  
                self.vm.writePop('pointer',1)
                self.vm.writePush('that',0)
            else:
                self.vm.writePush(kind,index)
        else:
            raise Exception('Illegal Token: %s' %(token))
        self.getNextToken()

'''
def CompileTerm(self):
#if(self.getNextToken()==-1): return 1
return 0
pass

    def subroutineDec(self):
        #DESCRIPTION OF WORKING OF FUNCTION
        #RETURN VALUE:
            #1. in case of file not even having all commands(ie EOF is encountered within this function) function returns 1
            #2. else it returns 0
            self.outfile.write("<subroutinDec>\n")

            #--------reading constructor|method|function--------------------------------------
            token=self.getinfo(self.presentline)
            functionKeys=['constructor', 'function', 'method']
            if(not token in functionKeys):
                print "function declaration missing keyword. lineno: {}".format(self.getlineno())
            else:
                self.outfile.write('<keyword> {} </keyword>'.format(token))

            cont=self.getNextToken()
            if(cont==-1):
                return 1;
            #-----------------------------------------------------------------------------------


            #----------return type of function--------------------------------------------------
            token=self.getinfo(self.presentline)
            if(not ((token in Type) or (token=='void'))):
                print "function declaration missing return type. lineno: {}".format(self.getlineno())
            else:
                self.outfile.write('<keyword> {} </keyword>'.format(token))

            cont=self.getNextToken()
            if(cont==-1):
                return 1;
            #-----------------------------------------------------------------------------------

            #-----------subroutine name---------------------------------------------------------
            token=self.gettag(self.presentline)
            if(token!='identifier'):
                print "function declaration missing name. lineno: {}".format(self.getlineno())
            else:
                subRName=self.getinfo()
                subroutineName.append(subRName)
                self.outfile.write('<identifier> {} </identifier>'.format(subRName))

            cont=self.getNextToken()
            if(cont==-1):
                return 1;
            #-----------------------------------------------------------------------------------

            #-----------bracket open------------------------------------------------------------
            token=self.getinfo(self.presentline)
            if(token!='('):
                print "function declaration missing opening parentheses. lineno: {}".format(self.getlineno())
            else:
                self.outfile.write('<symbol> ( </symbol>')

            cont=self.getNextToken()
            if(cont==-1):
                return 1;
            #-----------------------------------------------------------------------------------

            cont=self.parameterList();
            if(cont==-1):
                return 1;

            #-----------bracket close-----------------------------------------------------------
            token=self.getinfo(self.presentline)
            if(token!=')'):
                print "function declaration missing closing parentheses. lineno: {}".format(self.getlineno())
            else:
                self.outfile.write('<symbol> ) </symbol>')

            cont=self.getNextToken()
            if(cont==-1):
                return 1;
            #-----------------------------------------------------------------------------------

            cont=self.subroutineBody();
            if(cont==-1):
                return 1;

            return 0;
        pass

    def parameterList(self):
        #DESCRIPTION OF WORKING OF FUNCTION
        #RETURN VALUE:
            #1. in case of file not even having all commands(ie EOF is encountered within this function) function returns -1
            #2. else it returns 0.
            self.outfile.write("<parameterList>\n")

            prevTag=')'
            while(1):
                token=self.getinfo(self.presentline)
                token_tag=self.gettag(self.presentline);
                if(token==')'):
                    if(prevTag=='symbol'):
                        print "function declaration expecting more arguments in parameter list. lineno: {}".format(self.getlineno())
                        self.outfile.write("</parameterList>\n")
                        return 0;

                    elif (token==','):
                        if(prevTag=='symbol' or prevTag==')'):
                            print "function declaration expecting more arguments in parameter list. lineno: {}".format(self.getlineno())
                        elif(prevTag=='keyword'):
                            print "function declaration expecting named arguments in parameter list. lineno: {}".format(self.getlineno())
                        else:
                            prevTag='identifier'
                            self.outfile.write("<symbol> , </symbol>");

                    elif(token_tag=='keyword'):
                        if(not token in Type):
                            print "function declaration expecting valid datatype in parameter list. lineno: {}".format(self.getlineno())
                            if(prevTag=='keyword'):
                                print "function declaration expecting identifier name in parameter list. lineno: {}".format(self.getlineno())
                            elif(prevTag=='identifier'):
                                print "function declaration expecting comma seperated arguments in parameter list. lineno: {}".format(self.getlineno())
                            else:
                                prevTag='keyword'
                                self.outfile.write("<keyword> {} </keyword>".format(token));

                        elif(token_tag=='identifier'):
                            if(prevTag=='identifier' or prevTag=='symbol' or prevTag==')'):
                                print "function declaration missing data types in parameter list. lineno: {}".format(self.getlineno())
                            else:
                                prevTag='identifier'
                                self.outfile.write("<{0}> {1} </{0}>".format(token_tag, token));

                    cont=self.getNextToken()
                    if(cont==-1):
                        return -1;





cp=CompilationEngine('test1T.xml')

'''
