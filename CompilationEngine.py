

class CompilationEngine(object):

	def __init__(self,inputfile):
		self.outfile=open(inputfile[:inputfile.find('T.xml')]+'.xml','w')
		self.infile=open(inputfile,'r')
		self.linelist=self.infile.readlines()
		self.type=['int','char','boolean']

		self.function=['constructor','function','method']
		for r in self.linelist:
			if(r.strip()=='' or r.strip()=='<tokens>' or r.strip()=='</tokens>'): self.linelist.remove(r)
			pass
		self.lno=0
		self.presentline=self.linelist[self.lno].strip()
		x=self.CompileClass()
		if(x==1):
			#self.outfile.truncate()
			self.close()
			print ("\n\nParser exited with errors\n")
		else: 
			self.close()
			print ('\n\nParsing Successful\n\n')

		pass


	def gettag(self):
		line = self.presentline
		return line[line.find('<')+1:line.find('>')].strip()

	def getlineno(self):
		line=self.presentline
		line=line[line.find('<',2):]
		if(line==line[line.find(',')+1:]): return -1
		return line[line.find(',')+1:]
	def getinfo(self):
		line=self.presentline
		ln=(line[line.find('>')+1:])
		return ln[:ln.find('<')].strip()

	def getnextline(self):
		self.lno=self.lno+1
		if(self.lno==len(self.linelist)): 
			print ('End of File')
			
			return -1
		else: 
			self.presentline=self.linelist[self.lno].strip()
			return 1

	def CompileClass(self):
		if(self.getinfo() != 'class'):
			print  ('No class in given file: lineno:'+' '+str(self.getlineno()))
		else: 
			self.outfile.write('<class>\n')
			self.outfile.write('<keyword> class </keyword>\n')


		if(self.getnextline()==-1):
			return 1

		if(self.gettag() != 'identifier'):
			print ('No class in given file: lineno:'+' '+str(self.getlineno()))
		else: self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getnextline()==-1):
			return 1

		if(self.getinfo() != '{'):
			print ('Missing { in line'+str(self.getlineno()))
		else:
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')

		if(self.getnextline()==-1):
			return 1

		while(self.getinfo() in ['static','field']):
			if(self.CompileClassVarDec()==1): return 1

		while(self.getinfo() in self.function):
			if(self.CompileSubroutine()==1): return 1

		if(self.getinfo() != '{'):
			print ('Missing { in line'+str(self.getlineno()))
		else:
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')

		self.outfile.write(' </class>\n')
		return 0
		pass



	def isidentifier(self,token):
		if(self.gettag()=='identifier'):
			return 1
		else:
			return 0



	def CompileClassVarDec(self):
		self.outfile.write(' <classVarDec>\n')
		if(not (self.getinfo() in ['static','field'])):
			print ('No type present in line '+str(self.getlineno()))
		else:
			self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')

		if(self.getnextline()==-1):
			return 1

		if(not(self.getinfo() in self.type) or not self.isidentifier(self.getinfo())):
			print ('No type present in line '+str(self.getlineno()))
		else:
			if(self.getinfo() in self.type):
				self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
			elif(self.gettag() == 'identifier'):
				self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getnextline()==-1):
			return 1

		if(not self.isidentifier(self.getinfo())):
			print ('Wrong Identifier in line '+str(self.getlineno()))
		else:
			self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getnextline()==-1):
			return 1

		while(self.getinfo()==','):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
			if(self.getnextline()==-1):
				return 1
			if(not self.isidentifier(self.getinfo())):
				print ('Wrong Identifier in line '+str(self.getlineno()))
			else:
				self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

			if(self.getnextline()==-1):
				return 1

		if(self.getinfo() != ';'):
			print ('Missing ; in line'+str(self.getlineno()))
		else:
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')

		if(self.getnextline()==-1):
			return 1

		self.outfile.write(' </classVarDec>\n')
		return 0

		pass




	def CompileSubroutine(self):
		self.outfile.write('<subroutineDec>\n')
		if(self.getinfo() in self.function):
			self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
		else:
			print ('No function type present in line '+str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1

		if(self.getinfo() in self.type or self.getinfo() == 'void'):
			self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
		else: 
			if(not self.isidentifier(self.getinfo())):
				print ('Wrong Identifier in line '+str(self.getlineno()))
			else:
				self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getnextline()==-1):
			return 1

		if(not self.isidentifier(self.getinfo())):
			print ('Wrong Identifier in line '+str(self.getlineno()))
		else:
			self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getnextline()==-1):
			return 1


		if(self.getinfo() != '('):
			print ('Missing ( in line'+str(self.getlineno()))
		else:
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')

		if(self.getnextline()==-1):
			return 1

		if(self.getinfo in self.type or self.gettag()=='identifier'):

			if(self.CompileParameterList()==1): return 1



		if(self.getinfo() != ')'):
			print ('Missing ) in line'+str(self.getlineno()))
		else:
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		self.outfile.write(' </subroutineDec>\n')

		if(self.getnextline()==-1):
			return 1

		self.outfile.write('<subroutineBody>\n')

		if(self.getinfo() != '{'):
			print ('Missing { in line'+str(self.getlineno()))
		else:
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')

		if(self.getnextline()==-1):
			return 1

		while(self.getinfo() == 'var'):
			if(self.CompileVarDec()==1): return 1

	
		if(self.CompileStatements()==1): return 1

		if(self.getinfo() != '}'):
			print ('Missing } in line'+str(self.getlineno()))
		else:
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		self.outfile.write(' </subroutineBody>\n')

		if(self.getnextline()==-1):
			return 1

		self.outfile.write(' </subroutineDec>\n')
		return 0
		pass

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

			if(self.getnextline()==-1):
				return 1

			if(not self.isidentifier(self.getinfo())):
				print ('Wrong Identifier in line '+str(self.getlineno()))
			else:
				self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

			if(self.getnextline()==-1):
				return 1

			while(sel.getinfo()==','):
				self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')

				if(self.getnextline()==-1):
					return 1

				if(self.getinfo() in self.type):
					self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
				else: 
					if(not self.isidentifier(self.getinfo())):
						print ('Wrong Identifier in line '+str(self.getlineno()))
					else:
						self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

				if(self.getnextline()==-1):
					return 1

				if(not self.isidentifier(self.getinfo())):
					print ('Wrong Identifier in line '+str(self.getlineno()))
				else:
					self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

				if(self.getnextline()==-1):
					return 1

		else:
			print ('Wrong symbol in line'+str(self.getlineno()))

			if(self.getnextline()==-1): return 1

		self.outfile.write(' </parameterList>\n')
		return 0
		pass




	def CompileVarDec(self):
		self.outfile.write('<VarDec>\n')
		if(self.getinfo() == 'var'):
			self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
		else:
			print ('Missing var in line '+ self.getlineno())

		if(self.getnextline()==-1):
				return 1

		if(self.getinfo() in self.type):
			self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
		else: 
			if(not self.isidentifier(self.getinfo())):
				print ('Wrong Identifier in line '+str(self.getlineno()))
			else:
				self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getnextline()==-1):
				return 1

		if(not self.isidentifier(self.getinfo())):
			print ('Wrong Identifier in line '+str(self.getlineno()))
		else:
			self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getnextline()==-1):
			return 1

		while(self.getinfo()==','):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')

			if(self.getnextline()==-1):
				return 1

			if(self.getinfo() in self.type):
				self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')
			else: 
				if(not self.isidentifier(self.getinfo())):
					print ('Wrong Identifier in line '+str(self.getlineno()))
				else:
					self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

			if(self.getnextline()==-1):
				return 1

			if(not self.isidentifier(self.getinfo())):
				print ('Wrong Identifier in line '+str(self.getlineno()))
			else:
				self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

			if(self.getnextline()==-1):
				return 1

		if(self.getinfo() != ';'):
			print ('Missing ; in line'+str(self.getlineno()))
		else:
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')

		if(self.getnextline()==-1):
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

		if(self.getnextline()==-1):
			return 1

		if(not self.isidentifier(self.getinfo())):
			print ('Wrong Identifier in line '+str(self.getlineno()))
		else:
			self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getnextline()==-1):
			return 1

		if(self.getinfo()=='['):
			self.outfile.write('<symbol> [ </symbol>\n')
			if(self.getnextline()==-1):
				return 1

			self.CompileExpression()

			if(self.getinfo()==']'):
				self.outfile.write('<symbol> ] </symbol>\n')
			else:
				print ('Missing ] in line '+ str(self.getlineno()))

			if(self.getnextline()==-1):
				return 1

		if(self.getinfo()=='='):
			self.outfile.write('<symbol> = </symbol>\n')
		else:
			print ('Missing = in line '+str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1

		self.CompileExpression()

		if(self.getinfo()==';'):
			self.outfile.write('<symbol> ; </symbol>\n')
		else:
			print ('Missing ; in line '+str(self.getlineno()))

		if(self.getnextline()==-1):
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

		if(self.getnextline()==-1):
			return 1

		if(self.getinfo()=='('):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing () in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1

		self.CompileExpression()

		if(self.getinfo()==')'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ) in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1


		if(self.getinfo()=='{'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing { in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1

		self.CompileStatements()

		if(self.getinfo()=='}'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing } in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1

		if(self.getinfo()=='else'):
			self.outfile.write('<keyword> '+self.getinfo()+' </keyword>\n')

			if(self.getnextline()==-1):
				return 1

			if(self.getinfo()=='{'):
				self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
			else:
				print ('Missing { in line '+ str(self.getlineno()))

			if(self.getnextline()==-1):
				return 1

			self.CompileStatements()

			if(self.getinfo()=='}'):
				self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
			else:
				print ('Missing } in line '+ str(self.getlineno()))

			if(self.getnextline()==-1):
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

		if(self.getnextline()==-1):
			return 1

		if(not self.isidentifier(self.getinfo())):
			print ('Wrong Identifier in line '+str(self.getlineno()))
		else:
			self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

		if(self.getnextline()==-1):
			return 1

		if(self.getinfo()=='.'):
			self.outfile.write('<symbol> . </symbol>\n')
			if(self.getnextline()==-1):
				return 1

			if(not self.isidentifier(self.getinfo())):
				print ('Wrong Identifier in line '+str(self.getlineno()))
			else:
				self.outfile.write('<identifier> '+self.getinfo()+' </identifier>\n')

			if(self.getnextline()==-1):
				return 1


		if(self.getinfo()=='('):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ( in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1
		self.outfile.write('<expressionList>\n')
		if(self.isTerm()):
			if(self.CompileExpression()==1): return 1
			while(self.getinfo()==','):
				self.outfile.write('<symbol> , </symbol>\n')

				if(self.getnextline()==-1): return 1

				if(self.CompileExpression()==1): return 1
		self.outfile.write('</expressionList>\n')



		if(self.getinfo()==')'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ) in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1

		if(self.getinfo()==';'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ; in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
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

		if(self.getnextline()==-1):
			return 1

		if(self.getinfo()=='('):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ( in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1

		self.CompileExpression()

		if(self.getinfo()==')'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ) in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1

		if(self.getinfo()=='{'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing { in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1

		self.CompileStatements()

		if(self.getinfo()=='}'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing } in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
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

		if(self.getnextline()==-1):
			return 1

		if(self.isTerm()):
			self.CompileExpression()

		if(self.getinfo()==';'):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
		else:
			print ('Missing ; in line '+ str(self.getlineno()))

		if(self.getnextline()==-1):
			return 1

		self.outfile.write('</ReturnStatement>\n')

		return 0
		pass

	def CompileExpression(self):
		self.outfile.write('<expression>\n')

		self.CompileTerm()

		while(self.getinfo() in ['+','-','*','/','&amp','|','&lt','&gt','=']):
			self.outfile.write('<symbol> '+self.getinfo()+' </symbol>\n')
			if(self.getnextline()==-1):
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

				if(self.getnextline()==-1): return 1

				if(self.CompileExpression()==1): return 1
		self.outfile.write('</expressionList>\n')

		if(self.getnextline()==-1): return 1

		return 0
		pass

	def CompileTerm(self):
		#if(self.getnextline()==-1): return 1
		return 0
		pass

	'''def subroutineDec(self):
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

		cont=self.getnextline()
		if(cont==-1):
			return 1;
		#-----------------------------------------------------------------------------------


		#----------return type of function--------------------------------------------------
		token=self.getinfo(self.presentline)
		if(not ((token in Type) or (token=='void'))):
			print "function declaration missing return type. lineno: {}".format(self.getlineno())
		else:
			self.outfile.write('<keyword> {} </keyword>'.format(token))

		cont=self.getnextline()
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

		cont=self.getnextline()
		if(cont==-1):
			return 1;
		#-----------------------------------------------------------------------------------

		#-----------bracket open------------------------------------------------------------
		token=self.getinfo(self.presentline)
		if(token!='('):
			print "function declaration missing opening parentheses. lineno: {}".format(self.getlineno())
		else:
			self.outfile.write('<symbol> ( </symbol>')

		cont=self.getnextline()
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

		cont=self.getnextline()
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

			cont=self.getnextline()
			if(cont==-1):
				return -1;'''





cp=CompilationEngine('test1T.xml')
'''Funtions yet to be defined:
    isTerm()
    CompileTerm()'''
