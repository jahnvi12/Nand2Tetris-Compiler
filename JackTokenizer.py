import re

symbols = r'()[]{},;=.+-*/&|~<>'
comment=r'(?:(\/\*(.|\n)*?\*\/)|(//.*))'
delimiters = r'([\(\)\[\]\{\}\,\;\=\.\+\-\*\/\&\|\~\<\>]|(?:"[^"]*")| *)'
keywords = ('class','constructor','method','function','int','boolean','char','void','var','static','field','let','do','if','else','while','return','true','false','null','this')

class JackTokenizer(object):
	
	def __init__(self, inputFile):
		self.currLine=-1
		self.token=None
		fin=open(inputFile,"r+")
		self.inp=fin.read();
		self.inp = " ".join(re.sub(comment,"",self.inp).split())
		self.tokenList=[token for token in re.split(delimiters,self.inp) if token not in ('', ' ')]

	def advance(self):
		self.token=self.tokenList.pop(0)

	def hasMoreTokens(self):
		if len(self.tokenList)>0:
			return True
		return False

	def tokenType(self):
		if self.token in keywords:
			return 'KEYWORD'
		elif self.token in symbols:
			return 'SYMBOL'
                elif self.token.isdigit():
                    if int(self.token)>=0 and int(self.token)<=32767: 
			return 'INT_CONST'
                    else:
                        raise Exception('Integer constant should be between 0 and 32767, it is %s' % self.token)
		elif re.match(r'(?:"[^"]*")',self.token):
			return 'STRING_CONST'
		elif re.match(r'^[\w\d_]*$',self.token) and not self.token[0].isdigit() and self.token not in keywords:
			return 'IDENTIFIER'
		else:
			raise Exception('Illegal Token: %s'%self.token)

	def keyword(self):
		return self.token

	def symbol(self):
		return self.token

	def identifier(self):
		return self.token

	def intVal(self):
		return int(self.token)

	def stringVal(self):
		return self.token[1:-1]
'''		
j=JackTokenizer('inp.jack')
while(j.hasMoreTokens()):
	j.advance()
	print j.token
	if j.tokenType()=='INT_CONST':
		print j.intVal()
	elif j.tokenType()=='STRING_CONST':
		print j.stringVal()

'''
		


