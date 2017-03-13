import re
#import ply.lex as lex
def loadSymbolTable():
	
	symbolTable["keyword"] = keyword
	symbolTable["dataType"] = dataType
	symbolTable["preDefRoutine"] = preDefRoutine

def validLexeme(string):
	
	res = False
	if(string in keyword):
		#print("key " + string + "\n")
		res = "keyword"
	elif(string in dataType):
		#print("dataType " + string + "\n")
		res = "dataType"
	elif(string in preDefRoutine):
		res = "preDefRoutine"
	elif(re.match(identifier, string)):
		#print("id " + string + "\n")
		res = "identifier"
	elif(re.match(punctuator, string)):
		#print("punc " + string)
		res = "punctuator"
	elif(re.match(number, string)):
		res = "number"
	elif(re.match(aritmeticOperator, string)):
		res = "arithmeticOperator"
	elif(re.match(assignmentOperator, string)):
		res = "assignmentOperator"
	elif(string in relationalOperator):
		res = "relationalOperator"
	elif(string in logicalOperator):
		res = "logicalOperator"
	elif(string == "#"):
		res = "hashOperator"
	elif(string == ".h"):
		res = "headerExtension"
	return res
	
def lexer():
	global lb
	global fp
	
	lexeme = prg[lb:fp]
	
	while(re.match(spaces, lexeme)):
		#print("x " + lexeme + "\n")
		lb = lb + 1
		fp = fp + 1
		lexeme = prg[lb:fp]
	
	#if(re.match(spaces, prg[
	#print("lexeme: " + lexeme + " type: " + str(type(lexeme)) + "\n");
	res = validLexeme(lexeme)
	while((not res) and (fp <= len(prg))):
		#print("lexeme1: " + lexeme + "\n")
		fp = fp + 1
		lexeme = prg[lb:fp]
		res = validLexeme(lexeme)
	
	#print(lexeme + "\n")
	tokenType = res
	res = validLexeme(lexeme)
	while((res) and (fp <= len(prg))):
		#print("lexeme2: " + lexeme + "\n")
		fp = fp + 1
		lexeme = prg[lb:fp]
		tokenType = res
		res = validLexeme(lexeme)
	
	lexeme = prg[lb:fp - 1]
	lb = fp - 1
	
	if((tokenType != False) and (tokenType not in symbolTable)):
		symbolTable[tokenType] = list()
		
	if((tokenType != False) and lexeme not in symbolTable[tokenType]):
		symbolTable[tokenType].append(lexeme.strip())
	
	#print("TOKEN: " + str(lexeme) + " TYPE: " + str(tokenType) + "\n");
	#print(str(lb) + " " + str(fp) + "\n")
	#print(str(len(prg)))
	return dict({tokenType:lexeme})

def parse_start():
	status = program()
	
	print("SUCCESSFUL PARSING\n") if(status == 0) else print("FAILED PARSING\n")
	
def program():

	status = preProcessorDirective()
	
	if(status == 0):
		status = externDeclaration()
		
		if(status == 0):
			status = mainFunction()
	
	return status

def preProcessorDirective():

	status = 0
	token = lexer()
	
	token_type = list(token.keys())[0]
	token_value = list(token.values())[0]
	
	if(token_type == "hashOperator"):
		
		token = lexer()
		token_type = list(token.keys())[0]
		token_value = list(token.values())[0]
		
		if(token_type == "keyword" and token_value == "include"):
				
			token = lexer()
			token_type = list(token.keys())[0]
			token_value = list(token.values())[0]
			
			if(token_type == "relationalOperator" and token_value == "<"):
				
				token = lexer()
				token_type = list(token.keys())[0]
				token_value = list(token.values())[0]
				
				if(token_type == "identifier"):
					
					token = lexer()
					token_type = list(token.keys())[0]
					token_value = list(token.values())[0]
					
					
					if(token_type == "headerExtension"):
					
						token = lexer()
						token_type = list(token.keys())[0]
						token_value = list(token.values())[0]	
					
						if(token_type == "relationalOperator" and token_value == ">"):
					
								status = preProcessorDirective()
								#print(str(status) + " after return\n")
							
						else:
							print("Syntax error: expected '>' but received " + str(token_value) + "\n")
							status = 1
					else:
						print("Syntax error: expected 'Header Extension' but received " + str(token_value) + "\n")
						status = 1
						
				else:
					print("Syntax error: expected 'Identifer' but received " + str(token_value) + "\n")
					status = 1
			else:	
				print("Syntax error: expected '<' but received " + str(token_value) + "\n")
				status = 1
				
		elif(token_type == "keyword" and token_value == "define"):
			
			
			token = lexer()
			token_type = list(token.keys())[0]
			token_value = list(token.values())[0]
			
			if(token_type == "identifier"):
				
				variableName = token_value
				token = lexer()
				token_type = list(token.keys())[0]
				token_value = list(token.values())[0]
				
				if(token_type == "number"):
					
					variableValue = int(token_value.strip())
					symbolTable[variableName] = variableValue
					status = preProcessorDirective()
					
					
				else:
					print("Syntax error: expected 'Number' but received " + str(token_value) + "\n")
					status = 1
			else:
				print("Syntax error: expected 'Identifier' but received " + str(token_value) + "\n")
				status = 1
					
		else:
			print("Syntax error: expected 'Keyword include/define' but received " + str(token_value) + "\n")
			status = 1
	else:
		#RESET POINTERS SINCE A WRONG TOKEN WAS OBTAINED
		global lb, fp
		lb = lb - len(token_value)
		fp = fp - len(token_value)
		
	return status
	#print("Token key: " + str((token_type) + " values: " + str(token_value) + "\n"))	

def externDeclaration():
	
	
	status = 0
	token = lexer()
	token_type = list(token.keys())[0]
	token_value = list(token.values())[0]

	if(token_type == "keyword" and token_value == "extern"):

		status = declarationStatement()
		if(status == 0):
		
			token = lexer()
			token_type = list(token.keys())[0]
			token_value = list(token.values())[0].strip()

			if(not (token_type == "punctuator" and token_value == ";")):
				print("Syntax error: expected 'Punctuator Semicolon' but received " + str(token_value) + "\n")
				status = 1
	else:
		#RESET POINTERS SINCE A WRONG TOKEN WAS OBTAINED
		global lb, fp
		lb = lb - len(token_value)
		fp = fp - len(token_value)	
	return status

def declarationStatement():
	
	status = 0
	token = lexer()
	token_type = list(token.keys())[0]
	token_value = list(token.values())[0]

	if(token_type == 'dataType'):
		
		dataType = token_value.strip()
		status = variable(dataType)
		
	else:
		print("Syntax error: expected 'Data Type' but received " + str(token_value) + "\n")
		status = 1
	
	return status
	
def optionalDeclarationStatement():
	
	#print("IN OPTDECL")
	status = 0
	token = lexer()
	token_type = list(token.keys())[0]
	token_value = list(token.values())[0]
	#print("before reset: " + str(token_value))

	if(token_type == 'dataType'):
	
		dataType = token_value.strip()
		status = variable(dataType)
		
	else:
	
		#RESET POINTERS SINCE A WRONG TOKEN WAS OBTAINED
		#print("resetting")
		global lb, fp
		lb = lb - len(token_value)
		fp = fp - len(token_value)
		status = 2
		"""
		if(token_value != "do"):
			token = lexer()
			token_type = list(token.keys())[0]
			token_value = list(token.values())[0]
		"""
		#print("after reset: " + str(token_value))
	return status
	
	
def variable(dataType):

	status = 0
	token = lexer()
	token_type = list(token.keys())[0]
	token_value = list(token.values())[0]
	
	if(token_type == 'identifier'):
		
		#print("received identifier, " + str(token_value))
		variableName = token_value.strip()
		
		if(dataType not in externalVariables):
			externalVariables[dataType] = list()
		
		if(variableName not in externalVariables[dataType]):
			externalVariables[dataType].append(variableName)
		
		#externalVariables.append([variableName, dataType])
		status = variableDash(dataType)
	else:
		print("Syntax error: expected 'Identifier' but received " + str(token_value) + "\n")
		status = 1
	
	return status

def variableDash(dataType):

	status = 0
	token = lexer()
	token_type = list(token.keys())[0]
	token_value = list(token.values())[0]
	
	if(token_type == 'punctuator' and token_value == ','):
		
		token = lexer()
		token_type = list(token.keys())[0]
		token_value = list(token.values())[0]
	
		if(token_type == 'identifier'):
			
			variableName = token_value.strip()
			if(dataType not in externalVariables):
				externalVariables[dataType] = list()
		
			if(variableName not in externalVariables[dataType]):
				externalVariables[dataType].append(variableName)
			#externalVariables.append([variableName, dataType])
			variableDash(dataType)
		
		else:
			print("Syntax error: expected 'Identifier' but received " + str(token_value) + "\n")
			status = 1
	else:
		#RESET POINTERS SINCE A WRONG TOKEN WAS OBTAINED
		global lb, fp
		#print(token_value)
		#print(str(lb) + " " + str(fp))
		lb = lb - len(token_value)
		fp = fp - len(token_value)
		#print(str(lb) + " " + str(fp))

	return status
	
def mainFunction():
	status = 0
	token = lexer()
	token_type = list(token.keys())[0]
	token_value = list(token.values())[0]
	
	if(token_type == "dataType" and token_value == "int"):
		
		status = mainDash()
		
	else:
		print("Syntax error: expected 'Return Type Integer' but received " + str(token_value) + "\n")
		status = 1
	
	return status
	
	
def mainDash():

	status = 0
	token = lexer()
	token_type = list(token.keys())[0]
	token_value = list(token.values())[0].strip()
	
	#print(str(token_type) + " " + str(token_value))
	
	if(token_type == "identifier" and token_value == "main"):
	
		token = lexer()
		token_type = list(token.keys())[0]
		token_value = list(token.values())[0].strip()
		
		if(token_type == "punctuator" and token_value == "("):
		
			token = lexer()
			token_type = list(token.keys())[0]
			token_value = list(token.values())[0].strip()
			
			if(token_type == "punctuator" and token_value == ")"):
			
				token = lexer()
				token_type = list(token.keys())[0]
				token_value = list(token.values())[0].strip()
				
				if(token_type == "punctuator" and token_value == "{"):
				
					status = statements()
					
					if(status == 0):
						
						token = lexer()
						token_type = list(token.keys())[0]
						token_value = list(token.values())[0].strip()
						#print(token_value + str(len(token_value)))
						if(not(token_type == "punctuator" and token_value == "}")):
							print("Syntax error: expected 'Punctuator1 close curly bracket' but received " + str(token_value) + "\n")
							status = 1
				else:
					print("Syntax error: expected 'Punctuator open curly bracket' but received " + str(token_value) + "\n")
					status = 1
						
				
			
			elif(token_type == "dataType" and token_value == "int"):
			
				token = lexer()
				token_type = list(token.keys())[0]
				token_value = list(token.values())[0].strip()
				
				if(token_type == "identifier" and token_value == "argc"):
				
					token = lexer()
					token_type = list(token.keys())[0].strip()
					token_value = list(token.values())[0].strip()
					
					if(token_type == "punctuator" and token_value == ","):
				
						token = lexer()
						token_type = list(token.keys())[0]
						token_value = list(token.values())[0].strip()
						
						if(token_type == "dataType" and token_value == "char"):
				
							token = lexer()
							token_type = list(token.keys())[0]
							token_value = list(token.values())[0].strip()
							
							if(token_type == "arithmeticOperator" and token_value == "*"):
				
								token = lexer()
								token_type = list(token.keys())[0]
								token_value = list(token.values())[0]	.strip()
								
								if(token_type == "identifier" and token_value == "argv"):
				
									token = lexer()
									token_type = list(token.keys())[0]
									token_value = list(token.values())[0].strip()
									
									if(token_type == "punctuator" and token_value == "["):
				
										token = lexer()
										token_type = list(token.keys())[0]
										token_value = list(token.values())[0].strip()
										
										if(token_type == "punctuator" and token_value == "]"):
				
											token = lexer()
											token_type = list(token.keys())[0]
											token_value = list(token.values())[0].strip()
											
											if(token_type == "punctuator" and token_value == ")"):
				
												token = lexer()
												token_type = list(token.keys())[0]
												token_value = list(token.values())[0].strip()
											
												if(token_type == "punctuator" and token_value == "{"):
				
													status = statements()
					
													if(status == 0):
						
														token = lexer()
														token_type = list(token.keys())[0]
														token_value = list(token.values())[0].strip()
				
														if(not(token_type == "punctuator" and token_value == "}")):
															print("Syntax error: expected 'Punctuator2 close curly bracket' ", end = "")
															print("but received " + str(token_value) + "\n")
															status = 1
												else:
													print("Syntax error: expected 'Punctuator open curly bracket'  ", end = "")
													print("but received " + str(token_value) + "\n")
													status = 1
											
											else:
												print("Syntax error: expected 'Punctuator close round bracket' but received ", end = "")
												print(str(token_value) + "\n")
												status = 1
											
										else:
											print("Syntax error: expected 'Punctuator close square bracket' but received ", end = "")
											print(str(token_value) + "\n")
											status = 1
									else:
										print("Syntax error: expected 'Punctuator open square bracket' but received ", end = "")
										print(str(token_value) + "\n")
										status = 1
									
								else:
									print("Syntax error: expected 'Identifier argv' but received " + str(token_value) + "\n")
									status = 1
									
							else:
								print("Syntax error: expected 'Pointer operator *' but received " + str(token_value) + "\n")
								status = 1
							
						else:
							print("Syntax error: expected 'Data type character' but received " + str(token_value) + "\n")
							status = 1
						
					else:
						print("Syntax error: expected 'Punctuator comma' but received " + str(token_value) + "\n")
						status = 1	
				
				else:
					print("Syntax error: expected 'Identifier argc' but received " + str(token_value) + "\n")
					status = 1
				
			
			else:
				print("Syntax error: expected 'Punctuator close round bracket' but received " + str(token_value) + "\n")
				status = 1
				
		else:
			print("Syntax error: expected 'Punctuator open round bracket' but received " + str(token_value) + "\n")
			status = 1
	
	else:
		print("Syntax error: expected 'Identifier main' but received " + str(token_value) + "\n")
		status = 1
		
	return status
	
def statements():
	
	
	#print("top of statements\n")
	status = 0
	
	status = optionalDeclarationStatement()
	
	if(status == 0):
		print("decl success")
		status = statements()
	else:
		status = initializationStatement()
		if(status == 0):	
			print("init success")
			status = statements()
		else:
			
			status = assignmentStatement()
			if(status == 0):
				print("assgn success")
				status = statements()
			else:
				
				status = 0
				token = lexer()
				token_type = list(token.keys())[0]
				token_value = list(token.values())[0]
				#print("IN statements: " + token_value)
				if(token_type == "keyword" and token_value == "do"):
		
					token = lexer()
					token_type = list(token.keys())[0]
					token_value = list(token.values())[0].strip()
					
					if(token_type == "punctuator" and token_value == "{"):
					
						#status = statements()
						
						#print("status: " + str(status))
						if(status == 0):
					
							token = lexer()
							token_type = list(token.keys())[0]
							token_value = list(token.values())[0].strip()
							#print(token_value)
							if(token_type == "punctuator" and token_value == "}"):
					
								token = lexer()
								token_type = list(token.keys())[0]
								token_value = list(token.values())[0].strip()
		
								if(token_type == "keyword" and token_value == "while"):
					
									token = lexer()
									token_type = list(token.keys())[0]
									token_value = list(token.values())[0].strip()
		
									if(token_type == "punctuator" and token_value == "("):
							
										status = condition()
								
										if(status == 0):
					
											token = lexer()
											token_type = list(token.keys())[0]
											token_value = list(token.values())[0].strip()
		
											if(token_type == "punctuator" and token_value == ")"):
					
												token = lexer()
												token_type = list(token.keys())[0]
												token_value = list(token.values())[0].strip()
		
												if(token_type == "punctuator" and token_value == ";"):
													#print("in statements: " + token_value + "\n")
													status = statements()
					
												else:
													print("Syntax error: expected 'Punctuator semicolon' ", end = "")
													print("but received " + str(token_value) + "\n")
													status = 1
					
											else:
												print("Syntax error: expected 'Punctuator close round bracket' ", end = "")
												print("but received " + str(token_value) + "\n")
												status = 1
					
									else:
										print("Syntax error: expected 'Punctuator open round bracket' ", end = "") 
										print("but received " + str(token_value) + "\n")
										status = 1
					
								else:
									print("Syntax error: expected 'Keyword while' but received " + str(token_value) + "\n")
									status = 1
					
							else:
								print("Syntax error: expected 'Punctuator10 close curly bracket' but received " + str(token_value) + "\n")
								status = 1
				
					else:
						print("Syntax error: expected 'Punctuator open curly bracket' but received " + str(token_value) + "\n")
						status = 1
		
				else:
		
					#RESET POINTERS SINCE A WRONG TOKEN WAS OBTAINED
					global lb, fp
					#print(token_value)
					#print(str(lb) + " " + str(fp))
					lb = lb - len(token_value)
					fp = fp - len(token_value)
	
	return status

def initializationStatement():

	status = 1
	
	return status
	
def assignmentStatement():

	status = 1
	
	return status

def condition():

	status = 0
	
	return status

prg = open("nocomments.c").read()

lb = 0
fp = 1

symbolTable = dict()
externalVariables = dict()
keyword = ["include", "define", "while", "do", "for", "return", "extern"]
dataType = ["void", "int", "short", "long", "char", "float", "double"]
preDefRoutine = ["printf", "scanf"]
#headerFile = ["stdio.h", "stdlib.h", "math.h", "string.h"]
identifier = "^[^\d\W]\w*\Z"
punctuator = "^[()[\]{};.,]$"
aritmeticOperator = "^[-+*]$"
assignmentOperator = "^=$"
relationalOperator = ["<", ">", "<=", ">=", "==", "!="]
logicalOperator = ["&&", "||", "!"]
number = "^\d+$"
spaces = "[' ''\n''\t']"

loadSymbolTable()
parse_start()
"""
while lb!=len(prg):
	lexer()
"""
#print(symbolTable)
#print(externalVariables)
"""
PARSER ERROR CODES:

0-SUCCESS
1-FAILURE
"""














		
	
