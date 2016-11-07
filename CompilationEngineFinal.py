vmcode={'=':'eq','+':'add','-':'sub','&':'and','|':'or','~':'not','<':'lt','>':'gt'}

class CompilationEngine(object):

        def __init__(self,tokenizer,table,vm):
            self.tokenizer=tokenizer
            self.table=table
            self.vm=vm
            self.labelSuffix=0
            self.type=['int','char','boolean']
            self.function=['constructor','function','method']

        def peek(self):
            return self.tokenizer.tokenList[0]

        def gettag(self):
            return self.peek().tokenType()

        def getinfo(self):
            return self.peek()

        def getNextToken(self):
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
            else:
                raise Exception("Too less tokens to parse!")


        def CompileClass(self):
            if(self.getinfo() != 'class'):
                raise Exception('No class in given file: Invalid token %s'%(self.getinfo()))

                self.getNextToken()

                if(self.gettag() != 'identifier'):
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

        '''	
        def isidentifier(self,token):
            if(self.gettag()=='identifier'):
                return 1
            else:
                return 0
        '''


        def CompileClassVarDec(self):
            kind=self.getinfo()
            if not kind in ['static','field']:
                raise Exception('Invalid variable kind: %s'%(self.getinfo()))

                self.getNextToken()
                typ=self.getinfo()
                if typ not in self.type:
                    if not self.table.KindOf(typ)=='class':
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
            kind=self.getinfo()
            if kind not in self.function:
                raise Exception('Illegal function kind: %s' %kind)

                self.getNextToken()

                typ=self.getinfo()
                if typ not in self.type and not typ=='void':
                    if not self.table.KindOf(typ)=='class':
                        raise Exception("Invalid return type : %s"%typ)
                    elif kind=='constructor':
                        raise Exception("Return type of constructor has to be class name!")

                self.getNextToken()

                name=self.getinfo()

                if not self.gettag()=='IDENTIFIER':
                    raise Exception("Illegal identifier: %s"%name)

                self.table.Define(name,None,kind)
                self.table.startSubroutine()
                self.getNextToken()

                if self.getinfo() != '(':
                    print ('Missing ( in line')
                    self.getNextToken()
                    self.CompileParameterList(kind)

                if self.getinfo() != ')':
                    print ('Missing ) in line')

                self.getNextToken()

                if self.getinfo() != '{':
                    print ('Missing { in line')

                self.getNextToken()

                while(self.getinfo() == 'var'):
                    self.CompileVarDec()

                self.vm.writeFunction(className+'$'+name,self.table.VarCount('local'))

                if kind=='constructor':
                    ###check formula to calculate size of object--->
                    size=self.table.VarCount('field')
                    self.vm.writePush('constant',size)
                    self.vm.writeCall('Memory.alloc',1) 
                    self.vm.writePop('pointer',0)
                    if kind=='method':
                        self.vm.writePush('argument',0) 
                        self.vm.writePop('pointer',0) 

                self.compileStatements()
                self.getNextToken()

                if self.getinfo() != '}':
                    print ('Missing } in line')

                self.getNextToken()


        def CompileParameterList(self,routine):
            kind='argument'
            if routine=='method':
                self.table.Define('this',None,kind)

            if self.getinfo()==')':
                return

            typ=self.getinfo()
            if typ not in self.type:
                if not self.table.KindOf(typ)=='class':
                    raise Exception("Invalid argument type of: %s"%(self.peek()))
                self.getNextToken()
                varName=self.getNextToken('IDENTIFIER',False)
                self.table.Define(varName,typ,kind)
                self.getNextToken()

            while not self.getinfo() == ')':
                if self.getinfo() != ',':
                    raise Exception("Illegal identifier %s"%(self.getinfo()))
                self.getNextToken()
                typ=self.getinfo()
                if typ not in self.type:
                    if not self.table.KindOf(typ)=='class':
                        raise Exception("Invalid argument type of: %s"%(self.peek()))
                    self.getNextToken()
                    varName=self.getNextToken('IDENTIFIER',False)
                    self.table.Define(varName,typ,kind)
                    self.getNextToken()

        def CompileVarDec(self):
            if self.getinfo()!='var':
                raise Exception("Illegal type %s"%(self.getinfo()))

            self.getNextToken()   
            typ=self.getinfo()
            if typ not in self.type:
                if not self.table.KindOf(typ)=='class':
                    raise Exception("Invalid type of: %s"%(self.peek()))                      

            varName=self.getNextToken('IDENTIFIER',False)
            self.table.Define(varName,typ,'local')
            while not self.getinfo() == ';':
                if self.getinfo() !=',':
                    raise Exception("Comma expected")
                self.getNextToken()
                varName = self.getNextToken('IDENTIFIER',False)
                self.table.Define(varName,typ,'local') 
                self.getNextToken()       
                self.getNextToken() 



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
                else:
                    raise Exception('Not a statement: %s' %(self.getinfo()))

        def CompileLet(self):
            if(self.getinfo()!='let'):
                print ('Missing let in line ')

                self.getNextToken()
                token=self.getinfo()
                if not self.isidentifier(self.getinfo()):
                    raise Exception('Wrong Identifier in line '+str(self.getlineno()))

                segment = self.table.KindOf(token)
                index= self.table.IndexOf(token)
                self.getNextToken()

                if(self.getinfo()=='['):
                        self.getNextToken()
                        self.CompileExpression()

                        if(self.getinfo()!=']'):
                            print ('Missing ] in line ')

                        self.getNextToken()
                        self.vm.writePush(segment,index)
                        self.vm.writeArithmetic('add')

                        if(self.getinfo()!='='):
                            raise Exception('Missing = in line ')

                        self.getNextToken()
                        self.CompileExpression()
                        self.vm.writePop('temp',0)
                        self.vm.writePop('pointer',1)
                        self.vm.writePush('temp',0)
                        self.vm.writePop('that',0)
                else:
                    if(self.getinfo()!='='):
                        raise Exception('Missing = in line ')
                    self.getNextToken()
                    self.compileExpression()
                    self.vm.writePop(kind,index)

                if(self.getinfo()!=';'):
                    raise Exception('Missing ; in line '+str(self.getlineno()))

                self.getNextToken()

        def CompileIf(self):
            if(self.getinfo()!='if'):
                raise Exception('Missing if in line ')

                self.getNextToken()

                if(self.getinfo()!='('):
                    raise Exception('Missing () in line ')

                self.getNextToken()
                self.CompileExpression()

                if(self.getinfo()!=')'):
                    raise Exception('Missing ) in line ')
                self.getNextToken()

                true='IF_TRUE'+string(self.labelSuffix)
                false='IF_FALSE'+string(self.labelSuffix)
                end='END'+string(self.labelSuffix)
                self.labelSuffix=self.labelSuffix+1
                self.vm.writeIf(true)
                self.vm.writeGoto(false)
                self.vm.writeLabel(true)

                if(self.getinfo()!='{'):
                    raise Exception('Missing { in line ')

                self.getNextToken()
                self.CompileStatements()

                if(self.getinfo()!='}'):
                    raise Exception('Missing } in line ')

                self.getNextToken()

                if self.getinfo()=='else':
                    self.vm.writeGoto(end)
                    self.vm.writeLabel(false)
                    if self.getinfo()=='else':
                        if(self.getinfo()!='{'):
                            raise Exception('Missing { in line ')

                        self.getNextToken()
                        self.CompileStatements()

                        if(self.getinfo()!='}'):
                            raise Exception('Missing } in line ')

                        self.getNextToken()
                        self.vm.writeLabel(end)



        def CompileDo(self):
            if not self.getinfo()=='do':
                print ('Missing do in line ')

            self.getNextToken()

            self.compileTerm()
            self.vm.writePop('temp',0)		
            if self.getinfo() !=';' :
                raise Exception("Comma Expected")

            self.getNextToken()


        def CompileWhile(self):
                loop='LOOP'+string(self.labelSuffix)
                end='END'+string(self.labelSuffix)
                self.labelSuffix=self.labelSuffix+1

                if(self.getinfo()!='while'):
                    raise Exception('Missing while in line ')

                self.writeLabel(loop)

                self.getNextToken()

                if(self.getinfo()!='('):
                    raise Exception('Missing ( in line ')

                self.getNextToken()
                self.CompileExpression()

                if(self.getinfo()!=')'):
                    raise Exception('Missing ) in line ')

                self.vm.writeArithmetic('not') 
                self.vm.writeIf(end)

                self.getNextToken()

                if(self.getinfo()!='{'):
                    raise Exception('Missing { in line ')

                self.getNextToken()
                self.CompileStatements()

                if(self.getinfo()!='}'):
                    raise Exception('Missing } in line ')
                self.vm.writeGoto(loop)
                self.writeLabel(end)

                self.getNextToken()

        def CompileReturn(self):
            if(self.getinfo()!='return'):
                raise Exception('Missing return in line '+str(self.getlineno()))

                self.getNextToken()

                if(self.getinfo()!=';'):
                    self.CompileExpression()
                else:
                    self.vm.writePush('constant',0)

                if(self.getinfo()!=';'):
                    raise Exception('Missing ; in line ')
                self.vm.writeReturn()

                self.getNextToken()

        def CompileExpression(self):
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
                    raise Exception("Comma expected")
                nargs=nargs+1
                self.compileExpression()
                return nargs

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
