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
		symbolTable[tokenType].append(lexeme)
	
	print("TOKEN: " + str(lexeme) + " TYPE: " + str(tokenType) + "\n");
	#print(str(lb) + " " + str(fp) + "\n")
	#print(str(len(prg)))
	return dict({tokenType:lexeme})

prg = open("nocomments.c").read()

lb = 0
fp = 1

symbolTable = dict()
keyword = ["include", "define", "while", "do", "for", "return","main"]
dataType = ["void", "int", "short", "long", "char", "float", "double"]
preDefRoutine = ["printf", "scanf"]
identifier = "^[^\d\W]\w*\Z"
punctuator = "^[()[\]{};.,]$"
aritmeticOperator = "^[-+*]$"
assignmentOperator = "^=$"
relationalOperator = ["<", ">", "<=", ">=", "==", "!="]
logicalOperator = ["&&", "||", "!"]
number = "^\d+$"
spaces = "[' ''\n''\t']"

loadSymbolTable()

while lb!=len(prg):
	lexer()

print(symbolTable)
















		
	
