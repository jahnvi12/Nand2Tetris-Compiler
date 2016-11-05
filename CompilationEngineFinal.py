

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
			raise Exception('Illegal function kind: %s',%kind)
		
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

'''		
	def CompileParameterList(self):
		self.outfile.write('<parameterList>\n')
		if(self.getinfo() in self.type or self.gettag()=='identifier'):
			if(self.getinfo() in self.type):
				self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
			else: 
				if(not self.isidentifier(self.getinfo())):
					print ('Wrong Identifier in line '+str(self.getlineno()))
				else:
					self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

			if(self.getNextToken()==-1):
				return 1

			if(not self.isidentifier(self.getinfo())):
				print ('Wrong Identifier in line '+str(self.getlineno()))
			else:
				self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

			if(self.getNextToken()==-1):
				return 1

			while(sel.getinfo()==','):
				self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')

				if(self.getNextToken()==-1):
					return 1

				if(self.getinfo() in self.type):
					self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
				else: 
					if(not self.isidentifier(self.getinfo())):
						print ('Wrong Identifier in line '+str(self.getlineno()))
					else:
						self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

				if(self.getNextToken()==-1):
					return 1

				if(not self.isidentifier(self.getinfo())):
					print ('Wrong Identifier in line '+str(self.getlineno()))
				else:
					self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

				if(self.getNextToken()==-1):
					return 1

		else:
			print ('Wrong symbol in line'+str(self.getlineno()))

			if(self.getNextToken()==-1): return 1

		self.outfile.write(' </parameterList>\n')
		return 0
		pass




	def CompileVarDec(self):
		self.outfile.write('<VarDec>\n')
		if(self.getinfo() == 'var'):
			self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
		else:
			print ('Missing var in line '+ self.getlineno())

		if(self.getNextToken()==-1):
				return 1

		if(self.getinfo() in self.type):
			self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
		else: 
			if(not self.isidentifier(self.getinfo())):
				print ('Wrong Identifier in line '+str(self.getlineno()))
			else:
				self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getNextToken()==-1):
				return 1

		if(not self.isidentifier(self.getinfo())):
			print ('Wrong Identifier in line '+str(self.getlineno()))
		else:
			self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getNextToken()==-1):
			return 1

		while(self.getinfo()==','):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')

			if(self.getNextToken()==-1):
				return 1

			if(self.getinfo() in self.type):
				self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
			else: 
				if(not self.isidentifier(self.getinfo())):
					print ('Wrong Identifier in line '+str(self.getlineno()))
				else:
					self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

			if(self.getNextToken()==-1):
				return 1

			if(not self.isidentifier(self.getinfo())):
				print ('Wrong Identifier in line '+str(self.getlineno()))
			else:
				self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

			if(self.getNextToken()==-1):
				return 1

		if(self.getinfo() != ';'):
			print ('Missing ; in line'+str(self.getlineno()))
		else:
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')

		if(self.getNextToken()==-1):
			return 1

		self.outfile.write('</VarDec>\n')
		return 0
		pass

	def CompileStatements(self):
		while(self.getinfo() in ['let','if','while','do','return']):
			if(self.getinfo()=='let'): 
				if(self.CompileLet()==1): return 1
			elif (self.getinfo()=='if'): 
				if(self.CompileIf()==1): return 1
			elif (self.getinfo()=='while'): 
				if(self.CompileWhile()==1): return 1
			elif (self.getinfo()=='do'): 
				if(self.CompileDo()==1): return 1
			elif (self.getinfo()=='return'): 
				if(self.CompileReturn()==1): return 1

		return 0
		pass


	def CompileLet(self):
		self.outfile.write('<letStatement>\n')
		if(self.getinfo()=='let'):
			self.outfile.write('<keyword> let </keyword>\n')
		else:
			print ('Missing let in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		if(not self.isidentifier(self.getinfo())):
			print ('Wrong Identifier in line '+str(self.getlineno()))
		else:
			self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getNextToken()==-1):
			return 1

		if(self.getinfo()=='['):
			self.outfile.write('<symbol> [ </symbol>\n')
			if(self.getNextToken()==-1):
				return 1

			self.CompileExpression()

			if(self.getinfo()==']'):
				self.outfile.write('<symbol> ] </symbol>\n')
			else:
				print ('Missing ] in line '+ str(self.getlineno()))

			if(self.getNextToken()==-1):
				return 1

		if(self.getinfo()=='='):
			self.outfile.write('<symbol> = </symbol>\n')
		else:
			print ('Missing = in line '+str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		self.CompileExpression()

		if(self.getinfo()==';'):
			self.outfile.write('<symbol> ; </symbol>\n')
		else:
			print ('Missing ; in line '+str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		self.outfile.write('</letStatement>\n')
		return 0
		pass

	def CompileIf(self):

		self.outfile.write('<ifStatement>\n')
		if(self.getinfo()=='if'):
			self.outfile.write('<keyword> if </keyword>\n')
		else:
			print ('Missing if in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		if(self.getinfo()=='('):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing () in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		self.CompileExpression()

		if(self.getinfo()==')'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ) in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1


		if(self.getinfo()=='{'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing { in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		self.CompileStatements()

		if(self.getinfo()=='}'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing } in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		if(self.getinfo()=='else'):
			self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')

			if(self.getNextToken()==-1):
				return 1

			if(self.getinfo()=='{'):
				self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
			else:
				print ('Missing { in line '+ str(self.getlineno()))

			if(self.getNextToken()==-1):
				return 1

			self.CompileStatements()

			if(self.getinfo()=='}'):
				self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
			else:
				print ('Missing } in line '+ str(self.getlineno()))

			if(self.getNextToken()==-1):
				return 1

		self.outfile.write('</ifStatement>\n')
		return 0
		pass

	def CompileDo(self):
		self.outfile.write('<doStatement>\n')

		if(self.getinfo()=='do'):
			self.outfile.write('<keyword> do </keyword>\n')
		else:
			print ('Missing do in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		if(not self.isidentifier(self.getinfo())):
			print ('Wrong Identifier in line '+str(self.getlineno()))
		else:
			self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getNextToken()==-1):
			return 1

		if(self.getinfo()=='.'):
			self.outfile.write('<symbol> . </symbol>\n')
			if(self.getNextToken()==-1):
				return 1

			if(not self.isidentifier(self.getinfo())):
				print ('Wrong Identifier in line '+str(self.getlineno()))
			else:
				self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

			if(self.getNextToken()==-1):
				return 1


		if(self.getinfo()=='('):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ( in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1
		self.outfile.write('<expressionList>\n')
		if(self.isTerm()):
			if(self.CompileExpression()==1): return 1
			while(self.getinfo()==','):
				self.outfile.write('<symbol> , </symbol>\n')

				if(self.getNextToken()==-1): return 1

				if(self.CompileExpression()==1): return 1
		self.outfile.write('</expressionList>\n')



		if(self.getinfo()==')'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ) in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		if(self.getinfo()==';'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ; in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		self.outfile.write('</doStatement>\n')
		return 0
		pass



	def CompileWhile(self):
		self.outfile.write('<whileStatement>\n')

		if(self.getinfo()=='while'):
			self.outfile.write('<keyword> while </keyword>\n')
		else:
			print ('Missing if in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		if(self.getinfo()=='('):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ( in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		self.CompileExpression()

		if(self.getinfo()==')'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ) in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		if(self.getinfo()=='{'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing { in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		self.CompileStatements()

		if(self.getinfo()=='}'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing } in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		self.outfile.write('</whileStatement>\n')
		return 0
		pass

	def CompileReturn(self):
		self.outfile.write('<ReturnStatement>\n')

		if(self.getinfo()=='return'):
			self.outfile.write('<keyword> return </keyword>\n')
		else:
			print ('Missing return in line '+str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		if(self.isTerm()):
			self.CompileExpression()

		if(self.getinfo()==';'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ; in line '+ str(self.getlineno()))

		if(self.getNextToken()==-1):
			return 1

		self.outfile.write('</ReturnStatement>\n')

		return 0
		pass

	def CompileExpression(self):
		self.outfile.write('<expression>\n')

		self.CompileTerm()

		while(self.getinfo() in ['+','-','*','/','&amp','|','&lt','&gt','=']):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
			if(self.getNextToken()==-1):
				return 1
			self.CompileTerm()

		self.outfile.write('</expression>\n')
		return 0
		pass



	def close(self):
		self.outfile.close()

	def CompileExpressionList(self):
		self.outfile.write('<expressionList>\n')
		if(self.isTerm()):
			if(self.CompileExpression()==1): return 1
			while(self.getinfo()==','):
				self.outfile.write('<symbol> , </symbol>\n')

				if(self.getNextToken()==-1): return 1

				if(self.CompileExpression()==1): return 1
		self.outfile.write('</expressionList>\n')

		if(self.getNextToken()==-1): return 1

		return 0
		pass

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

