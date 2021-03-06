from pyparsing import *
from itertools import *
import os

#~ Local libraries
from syntax.syntax import Syntax
from queries.cq import Variable
from queries.ucq import UCQ

class ECQ:
	#~ The string expressions used to build an ECQ can be:
		#~ - "(not ECQ)"
		#~ - "(exists (vars) ECQ)"
		#~ - "(and ECQ ... ECQ)"
		#~ - "(mko-eq var1 var2)"
		#~ - "(mko UCQ)"
	#~ The equivalent expressed as a list (or tuple) are:
		#~ - ["not", ECQ]
		#~ - ["exists", [vars], ECQ]
		#~ - ["and", ECQ, ... , ECQ]
		#~ - ["mko-eq", var1, var2]
		#~ - ["mko", UCQ]
	
	def __init__(self, queryToParse, conceptList, roleList, individualList):
		self.__ecqs = set()
		self.__ucq = None
		self.__freeVars = set()
		self.__existentialVars = set()
		self.__equalityVar1 = None # First of the two vars comprising the equality assertion of the type "(mko-eq ?x ?y)"
		self.__equalityVar2 = None # Second of the two vars comprising the equality assertion of the type "(mko-eq ?x ?y)"
		self.__negated = False
		
		#~ Check the input
		self.__checkInput(queryToParse, conceptList, roleList, individualList)
		
		#~ Parse the input
		self.__parseQuery(queryToParse, conceptList, roleList, individualList)
		
		
	
	def __checkInput(self, queryToParse, conceptList, roleList, individualList):
		
		if not isinstance(queryToParse, (str, ParseResults, tuple, list)):
			#~ Formato non valido
			raise Exception("The provided CQ is not in a valid format: " + str(type(queryToParse)) + "\n" + str(queryToParse))
		
		#~ conceptList, roleList, and individualList, if not None, must be lists of strings
		if not (isinstance(conceptList, (list, tuple, set)) and \
			all(isinstance(concept, str) for concept in conceptList)):
			raise Exception("The concept list provided is not valid. It must be a list of strings.")
		
		if not (isinstance(roleList, (list, tuple, set)) and \
			all(isinstance(role, str) for role in roleList)):
			raise Exception("The role list provided is not valid. It must be a list of strings.")
		
		if not (isinstance(individualList, (list, tuple, set)) and \
			all(isinstance(individual, str) for individual in individualList)):
			raise Exception("The individual list provided is not valid. It must be a list of strings.")
		
		
	def __parseQuery(self, queryToParse, conceptList, roleList, individualList):
		
		syntax = Syntax()
		
		#~ If queryToParse is a string, we parse it by considering the parenthesis that close every expression
		#~ and analyse the resulting pyparsing.ParseResults.
		#~ If queryToParse is already a pyparsing.ParseResults, then we analise it directly.
		result = None
		if isinstance(queryToParse, str):
			parser = StringStart() + nestedExpr() + StringEnd()
			
			result = parser.parseString(queryToParse)
			
			#~ We consider only the first element of result, since, if it is a valid list,
			#~ then result is a nested list, and thus result[0] is the actual list we
			#~ are interested in.
			result = result[0]
			
		elif isinstance(queryToParse, (ParseResults, tuple, list)):
			result = queryToParse
		
		#~ The expressions used to build an ECQ can be:
			#~ - "(not ECQ)"
			#~ - "(exists (vars) ECQ)"
			#~ - "(and ECQ list)"
			#~ - (mko-eq var1 var2)
			#~ - (mko UCQ)
		#~ We check the first element (result[0]), 
		#~ which has to be a special word identifying which type of expression is used
		if result[0] == "not":
			#~ The expression must be "(not ECQ)", thus result must contain exactly 2 elements
			if len(result) != 2:
				raise Exception("The expression \"(not ECQ )\" must contain only one ECQ.")
			
			self.__ecqs.add(ECQ(result[1], conceptList, roleList, individualList))
			
			#~ Set the current ECQ as negated
			self.__negated = True
			
		elif result[0] == "exists":
			#~ The element result[1] must contain the existential variables,
			#~ while result[2] the inner ECQ.
			#~ result must contain exactly 3 elements
			if len(result) != 3:
				raise Exception("The expression \"(exists (Vars) (ECQ) )\" must contain only a set of existential variables and one ECQ.")
			
			self.__ecqs.add(ECQ(result[2], conceptList, roleList, individualList)) # Add the ECQ
			
			#~ Check that variables are syntactically valid (i.e. "?"+ a valid string)
			#~ and add them to self.__existentialVars
			varName = (StringStart() + syntax.variable.setResultsName("varName") + StringEnd()).leaveWhitespace()
			for varString in result[1]:
				var = Variable(varName.parseString(varString)[0])
				#~ Check that var is a free variable in the inner ECQ, otherwise raise an Exception
				for ecq in self.__ecqs:
					if not (var in ecq.freeVars()):
						raise Exception("The variable " + str(var) + " does not appear in the inner ECQ.")
						
				self.__existentialVars.add(var)
			
			
		elif result[0] == "and":
			#~ The list must contain "and" plus at least two inner ECQs,
			#~ starting from element result[1].
			if len(result) <= 2:
				raise Exception("The expression \"(and ... )\" must contain at least 2 internal ECQs.")
			
			for counter in range(1,len(result)):
				self.__ecqs.add(ECQ(result[counter], conceptList, roleList, individualList))
			
			#~ Check that all the inner ECQs have the same free variables
			#~ for check in combinations(self.__ecqs, 2):
				#~ print(check)
				#~ if check[0].freeVars() != check[1].freeVars():
					#~ raise Exception("The ECQs have different free variables in them!\n"+str(check[0])+"\n"+str(check[1]))
			
		elif result[0] == "mko-eq":
			
			print(queryToParse)
			print(result)
			
			#~ This represent an equality assertion. It must contain exactly 2 variable
			#~ (thus, considering 'mko-eq', the lenght can't be more than 3).
			if len(result) != 3:
				raise Exception("An equality assertion must contain exactly 2 variables. " + str(len(result[1:])) + " provided instead: " + str(result[1:]))
			
			#~ Check that variables are syntactically valid (i.e. "?"+ a valid string)
			#~ and add them to self.__existentialVars
			
			
			varName = (StringStart() + syntax.variable.setResultsName("varName") + StringEnd()).leaveWhitespace()
			
			print(varName.parseString(result[1]))
			
			self.__equalityVar1 = Variable(varName.parseString(result[1])[0])
			self.__equalityVar2 = Variable(varName.parseString(result[2])[0])
			
			#~ The variables have to be different from each other, we don't
			#~ accept an equality of the type (= ?x ?x).
			#~ If this is the case, we raise an Exception.
			if self.__equalityVar1 == self.__equalityVar2:
				raise Exception("The variables provided in the equality statement are the same. Please adjust/remove the atom: (= ?" + \
						str(result[1]) + " ?" + str(result[2]) + ")")
			
		elif result[0] == "mko":
			#~ This represent an UCQ inside a minimal knowledge operator.
			#~ An UCQ must be contained between parenthesis ( ), like:
			#~ (mko (...))
			#~ even if the UCQ is a single atom, so result is like:
			#~ ['mko', [...]]
			#~ thus result can't contain more than two elements.
			if len(result)>2:
				raise Exception("A minimal knowledge operator axiom should contain only an UCQ between parenthesys \"()\".")
				
			self.__ucq = UCQ(result[1], conceptList, roleList, individualList)
			
		else:
			raise Exception("No valid word found: " + str(result[0]))
		
		#~ Find the freeVars of the current ECQ.
		#~ To do so, we collect all the free vars appearing in the inner ECQs,
		#~ or in the UCQ, and remove the one that are set as existential
		#~ in the current ECQ.
		#~ If the current ECQ is an equality, we consider the variables involved
		#~ as free variables.
		for ecq in self.__ecqs:
			self.__freeVars.update(ecq.freeVars())
		
		if not self.__ucq is None:
			self.__freeVars.update(self.__ucq.freeVars())
		
		if isinstance(self.__equalityVar1, Variable):
			self.__freeVars.add(self.__equalityVar1)
		if isinstance(self.__equalityVar2, Variable):
			self.__freeVars.add(self.__equalityVar2)
		
		self.__freeVars = self.__freeVars.difference(self.__existentialVars)
		
		
	def freeVars(self):
		#~ Return the free vars appearing in the current ECQ.
		return self.__freeVars
	
	def existentialVars(self):
		#~ Return the existential vars appearing in the current ECQ.
		return self.__existentialVars
	
	def equalityVar1(self):
		#~ Return __equalityVar1
		return self.__equalityVar1
	
	def equalityVar2(self):
		#~ Return __equalityVar2
		return self.__equalityVar2
		
	def terms(self):
		#~ Returns the terms used in the atoms of the ECQ
		terms = set()
		
		for ecq in self.__ecqs:
			terms.update(ecq.terms())
		
		terms.update(self.__ucq.terms())
		
		return terms
	
	def concepts(self):
		#~ Returns the concepts used in the atoms
		concepts = set()
		
		for ecq in self.__ecqs:
			concepts.update(ecq.concepts())
		
		if not self.__ucq is None:
			concepts.update(self.__ucq.concepts())
		
		return concepts
	
	def roles(self):
		#~ Returns the roles used in the atoms
		roles = set()
		
		for ecq in self.__ecqs:
			roles.update(ecq.roles())
		
		if not self.__ucq is None:
			roles.update(self.__ucq.roles())
		
		return roles
	
	def isNegated(self):
		return self.__negated
	
	def ecqs(self):
		return self.__ecqs
		
	def ucq(self):
		return self.__ucq
		
	def __repr__(self):
		
		ecqStr = ""
		if self.__negated:
			
			ecqStr = "(not"
			for ecq in self.__ecqs:
				ecqStr += " " + str(ecq)
			ecqStr += " )"
			
		elif len(self.__existentialVars ) > 0:
			ecqStr = "(exists ("
			for var in self.__existentialVars:
				ecqStr += " " + str(var)
			ecqStr += " ) "
			for ecq in self.__ecqs:
				ecqStr += " " + str(ecq)
			ecqStr += " )"
			
		elif len(self.__ecqs ) > 0:
			ecqStr = "(and"
			for ecq in self.__ecqs:
				ecqStr += " " + str(ecq)
			ecqStr += " )"
			
		elif not self.__ucq is None:
			ecqStr += "(mko " + str(self.__ucq) + " )"
		
		elif isinstance(self.__equalityVar1, Variable) and isinstance(self.__equalityVar2, Variable):
			ecqStr = "(mko-eq " + str(self.__equalityVar1) + " " + str(self.__equalityVar2) + " )"
			
		return ecqStr
		
	def toDL(self):
		
		ecqStr = ""
		if self.__negated:
			
			ecqStr = "not"
			for ecq in self.__ecqs:
				ecqStr += " " + ecq.toDL()
			ecqStr += " "
			
		elif len(self.__existentialVars ) > 0:
			
			ecqStr = "exists "
			for var in self.__existentialVars:
				ecqStr += str(var) + ","
			ecqStr = ecqStr[:-1] + "."
			for ecq in self.__ecqs:
				ecqStr += " " + ecq.toDL()
			ecqStr += " "
			
		elif len(self.__ecqs ) > 0:
			ecqStr = "("
			for ecq in self.__ecqs:
				ecqStr += " " + ecq.toDL() + " and "
			ecqStr = ecqStr[:-5] + " )"
			
		elif not self.__ucq is None:
			ecqStr += "[ " + self.__ucq.toDL() + " ]"
		
		elif isinstance(self.__equalityVar1, Variable) and isinstance(self.__equalityVar2, Variable):
			ecqStr = "[ " + str(self.__equalityVar1) + " = " + str(self.__equalityVar2) + " ]"
			
		return ecqStr
	
	def toADL(self, indentLevel = 0):
		
		if not isinstance(indentLevel, int) or indentLevel < 0:
			raise Exception("The parameter indentLevel must be a positive integer.")
		
		def __indent(indentLevel):
			syntax = Syntax()
			
			return syntax.indent*indentLevel
		
		ecqStr = ""
		if self.__negated:
			
			ecqStr = __indent(indentLevel) + "(not\n"
			for ecq in self.__ecqs:
				ecqStr += ecq.toADL(indentLevel+1)
			ecqStr += __indent(indentLevel) + ")\n"
		
		elif len(self.__existentialVars ) > 0:
			ecqStr = __indent(indentLevel) + "(exists ("
			for var in self.__existentialVars:
				ecqStr += " " + str(var)
			ecqStr += " )\n"
			for ecq in self.__ecqs:
				ecqStr += ecq.toADL(indentLevel+1)
			ecqStr += __indent(indentLevel) + ")\n"
			
		elif len(self.__ecqs ) > 0:
			ecqStr = __indent(indentLevel) + "(and\n"
			for ecq in self.__ecqs:
				ecqStr += ecq.toADL(indentLevel+1)
			ecqStr += __indent(indentLevel) + ")\n"
			
		elif not self.__ucq is None:
			ecqStr += self.__ucq.toADL(indentLevel)
		
		elif isinstance(self.__equalityVar1, Variable) and isinstance(self.__equalityVar2, Variable):
			ecqStr = __indent(indentLevel) + "(=" + str(self.__equalityVar1) + " " + str(self.__equalityVar2) + " )\n"
			
		return ecqStr
	
	def toSQL(self, indentLevel = 0, state = 0, additionalVarsEqualities = {}, substitutions = {}):
		#~ additionalVarsEqualities represent a dictionary in which are stored additional
		#~ WHERE statements for variables appearing in the query (among the free variables).
		#~ Such statements are used to link a query which appears inside another, and
		#~ which results affect the external ones (e.g. in the case of NOT(ecq)).
		#~ Example of an entry of additionalVarsEqualities:
			#~ additionalVarsEqualities["x"] = "externalTable.column
			
		#~ substitutions is a dictionary containing additional WHERE statements
		#~ for variables appearing in the query.
		#~ Such statements are used to ground the values that a variable can assume,
		#~ and usually comes from the execution of a condition-action rule, which
		#~ returns some results, and the action's parameters must be grounded with them.
		
		if not isinstance(indentLevel, int) or indentLevel < 0:
			raise Exception("The parameter indentLevel must be a positive integer.")
		
		if not isinstance(state, int) or state < 0:
			raise Exception("The parameter state must be a positive integer.")
		
		if not isinstance(additionalVarsEqualities, dict):
			raise Exception("The parameter additionalVarsEqualities must be a dictionary.")
		
		def __indent(indentLevel):
			syntax = Syntax()
			
			return syntax.indent*indentLevel
		
		ecqString = ""
		if self.__negated:
			#~ The negation of an ECQ is translated by considering all possible
			#~ combinations of individuals for the free variables of the ECQ,
			#~ and removing the combinations that appear in the inner ECQ for the
			#~ same variables.
			#~ We achieve this by using NOT EXISTS and pushing in the inner ECQ
			#~ some additional equalities (through the dictionary additionalVarsEqualities)
			#~ in order to link the external and internalj queries.
			
			#~ If the inner ECQ is again a negation, than we remove both of them,
			#~ as it wouldn't affect the results.
			for ecq in self.__ecqs:
				if ecq.isNegated():
					for innerEcq in ecq.ecqs():
						return innerEcq.toSQL(indentLevel, state = state, substitutions = substitutions)
						
			#~ If there are no free variables, then we have a boolean query,
			#~ and this means that the internal ECQ is boolean as well.
			#~ To return the negated result, we use the formula
			#~ IF(innerECQs.booleanValue = 1, 0, 1) as booleanValue
			if len(self.__freeVars) == 0:
				ecqString = __indent(indentLevel) + "SELECT IF(innerECQ.booleanValue = 1, 0, 1) AS booleanValue\n"
				ecqString += __indent(indentLevel) + "FROM (\n"
				ecqString += "".join([ecq.toSQL(indentLevel+1, state = state) for ecq in self.__ecqs])
				ecqString += "\n" + __indent(indentLevel) + ") innerECQ\n"
			
			else:
				#~ Define, for each free variable that appears in the query, 
				#~ a link to the table _domain.
				#~ As these links will also be used to create the dictionary
				#~ additionalVarsEqualities to be passed in the inner ECQ, we must
				#~ create a unique naming of the tables (if we have two nested negations
				#~ both using the same names for the tables, it could pose a problem).
				#~ We achieve this by using the nesting level.
				
				#~ We need this both the SELECT statement (we use aliases for the
				#~ variables, e.g. SELECT _domain.individual as x) and FROM (as we
				#~ need a different _domain table for each variable).
				counter = 0
				newAdditionalVarsEqualities = {}
				aliases = {}
				for variable in self.__freeVars:
					aliases[variable.toSQL()] = "dom{0}_{1}".format(str(counter),str(indentLevel))
					newAdditionalVarsEqualities[variable.toSQL()] = aliases[variable.toSQL()] + ".individual"
					counter += 1
					
				ecqString = __indent(indentLevel) + "SELECT " + \
							(",\n"+__indent(indentLevel+1)).join(["{0}.individual AS {1}".format(aliases[var], var) for var in aliases.keys()]) + "\n" + \
							__indent(indentLevel) + "FROM " + \
							(",\n"+__indent(indentLevel+1)).join(["_domain {0}".format(aliases[var]) for var in aliases.keys()]) + "\n" + \
							__indent(indentLevel) + "WHERE NOT EXISTS (\n" + \
							"".join([innerECQ.toSQL(indentLevel+1, state = state, additionalVarsEqualities=newAdditionalVarsEqualities) for innerECQ in self.__ecqs]) + "\n" + \
							__indent(indentLevel) + ")\n"
				
				#~ We add the statements from additionalVarsEqualities
				for var in additionalVarsEqualities.keys():
					ecqString += __indent(indentLevel) + "AND {0} = {1}\n".format(newAdditionalVarsEqualities[var], additionalVarsEqualities[var])
				
				#~ We add the substitutions
				for var in substitutions.keys():
					ecqString += __indent(indentLevel) + "AND {0} = {1}\n".format(aliases[var], substitutions[var])
				
				return ecqString
				
				
		
		elif len(self.__existentialVars ) > 0:
			#~ An ECQ that uses some existential variables can be translated
			#~ in the following way:
				#~ SELECT innerECQ.freeVariables
				#~ FROM ( inner ECQ tranlsated to SQL) innerECQ
			#~ If there are no free variables, then we have a boolean query
			#~ and we simply count whether the internal ECQ returns any result.
			
			if len(self.__freeVars) == 0:
				ecqString = __indent(indentLevel) + "SELECT COUNT(*) > 0 AS booleanValue\n"
				ecqString += __indent(indentLevel) + "FROM (\n"
				ecqString += "".join([ecq.toSQL(indentLevel+1, state = state) for ecq in self.__ecqs])
				ecqString += "\n" + __indent(indentLevel) + ") innerECQs\n"
			else:
				#~ First, we generate the aliases for each variable.
				#~ We need this in case there are elements in additionalVarsEqualities
				alias = {}
				for var in self.__freeVars:
					alias[var.toSQL()] = "innerECQ." + var.toSQL()
				
				ecqString = __indent(indentLevel) + "SELECT " + ",".join(["{0} AS {1}".format(alias[var], var) for var in alias.keys()]) + "\n"
				ecqString += __indent(indentLevel) + "FROM (\n"
				ecqString += "".join([ecq.toSQL(indentLevel+1, state = state) for ecq in self.__ecqs])
				ecqString += "\n" + __indent(indentLevel) + ") innerECQs\n"
				
				#~ We add the statements from additionalVarsEqualities and substitutions
				if len(additionalVarsEqualities) > 0 or len(substitutions) > 0:
					ecqString += __indent(indentLevel) + "WHERE " + \
							(__indent(indentLevel) + "AND ").join(["{0} = {1}\n".format(alias[var], additionalVarsEqualities[var]) for var in additionalVarsEqualities.keys()]) + \
							(__indent(indentLevel) + "AND ").join(["{0} = {1}\n".format(alias[var], substitutions[var]) for var in substitutions.keys()])
				
		elif len(self.__ecqs ) > 0:
			#~ Conjunction of ECQs is done by translating the first ECQ to SQL, and
			#~ reuqiring its results to exist in the result set of the other ECQs.
			#~ To achieve this, we use EXISTS
			
			#~ If the ECQ is boolean (thus len(self.__freeVars) == 0),
			#~ we need to create a special SQL query.
			#~ All the ECQs in self.__ecqs are boolean, and their translations
			#~ yeald SQL queries that return either 1 or 0 (to be interpreted as
			#~ boolean values). If at least one ECQ returns 1 (True), then the
			#~ whole ECQ must return 1, 0 otherwise.
			#~ To do this we encapsulate the internal ECQs in a nested query,
			#~ while the external one takes care of checking if the nested one
			#~ contains at least one 1. Example:
			#~ SELECT COUNT(*) > 0 AS booleanValue
			#~ FROM ( inner ECQs SQL query) innerECQs
			#~ WHERE innerECQs.booleanValue = 1
			if len(self.__freeVars) == 0:
				ecqString = __indent(indentLevel) + "SELECT COUNT(*) > 0 AS booleanValue\n"
				ecqString += __indent(indentLevel) + "FROM (\n"
				ecqString += str("\n\n" + __indent(indentLevel+1) + "UNION\n\n").join([ecq.toSQL(indentLevel+1, state = state) for ecq in self.__ecqs])
				ecqString += "\n" + __indent(indentLevel) + ") innerECQs\n"
				ecqString += "\n" + __indent(indentLevel) + "WHERE innerECQs.booleanValue = 1\n"
				
			else:
				ecqString = str("\n\n" + __indent(indentLevel) + "INTERSECT\n\n").join([ecq.toSQL(indentLevel, state = state, additionalVarsEqualities=additionalVarsEqualities) for ecq in self.__ecqs])
			
				#~ As these links will also be used to create the dictionary
				#~ additionalVarsEqualities to be passed in the inner ECQ, we must
				#~ create a unique naming of the tables (if we have two nested negations
				#~ both using the same names for the tables, it could pose a problem).
				#~ We achieve this by using the nesting level.
				
				#~ We need this both the SELECT statement (we use aliases for the
				#~ variables, e.g. SELECT _domain.individual as x) and FROM (as we
				#~ need a different _domain table for each variable).
				counter = 0
				newAdditionalVarsEqualities = {}
				aliases = {}
				for variable in self.__freeVars:
					aliases[variable.toSQL()] = "dom{0}_{1}".format(str(counter),str(indentLevel))
					newAdditionalVarsEqualities[variable.toSQL()] = aliases[variable.toSQL()] + ".individual"
					counter += 1
				
				whereStatements = set()
				whereStatements.update(["EXISTS (\n" + \
									innerECQ.toSQL(indentLevel+1, state = state, additionalVarsEqualities=newAdditionalVarsEqualities) + \
									"\n" + __indent(indentLevel) + ")" for innerECQ in self.__ecqs])
				
				ecqString = __indent(indentLevel) + "SELECT " + \
							(",\n"+__indent(indentLevel+1)).join(["{0}.individual AS {1}".format(aliases[var], var) for var in aliases.keys()]) + "\n" + \
							__indent(indentLevel) + "FROM " + \
							(",\n"+__indent(indentLevel+1)).join(["_domain {0}".format(aliases[var]) for var in aliases.keys()]) + "\n" + \
							__indent(indentLevel) + "WHERE " + ("\n" + __indent(indentLevel) + "AND ").join(whereStatements)
				
				#~ We add the statements from additionalVarsEqualities
				#~ for var in additionalVarsEqualities.keys():
					#~ ecqString += __indent(indentLevel) + "AND {0} = {1}\n".format(newAdditionalVarsEqualities[var], additionalVarsEqualities[var])
				
				#~ We add the statements from additionalVarsEqualities and substitutions
				if len(additionalVarsEqualities) > 0 or len(substitutions) > 0:
					ecqString += __indent(indentLevel) + "AND " + \
							(__indent(indentLevel) + "AND ").join(["{0} = {1}\n".format(newAdditionalVarsEqualities[var], additionalVarsEqualities[var]) for var in additionalVarsEqualities.keys()]) + \
							(__indent(indentLevel) + "AND ").join(["{0} = {1}\n".format(newAdditionalVarsEqualities[var], substitutions[var]) for var in substitutions.keys()])
				
				return ecqString
				
			#~ return ecqString
			
		elif not self.__ucq is None:
			ecqString = __indent(indentLevel) + "SELECT " + \
						(",\n"+__indent(indentLevel+1)).join(["innerUCQ.{0} AS {1}".format(var.toSQL(),var.toSQL()) for var in self.__freeVars]) + "\n" + \
						__indent(indentLevel) + "FROM (\n" + \
						self.__ucq.toSQL(indentLevel = indentLevel+1, state = state) + \
						"\n" + __indent(indentLevel) + ") innerUCQ"
			
			#~ We add the statements from additionalVarsEqualities
			#~ if len(additionalVarsEqualities) > 0:
				#~ ecqString += __indent(indentLevel) + "WHERE " + \
							#~ (__indent(indentLevel) + "AND ").join(["innerUCQ.{0} = {1}\n".format(var, additionalVarsEqualities[var]) for var in additionalVarsEqualities.keys()])
			
			#~ We add the statements from additionalVarsEqualities and substitutions
			if len(additionalVarsEqualities) > 0 or len(substitutions) > 0:
				ecqString += __indent(indentLevel) + "WHERE " + \
						(__indent(indentLevel) + "AND ").join(["{0} = {1}\n".format(var, additionalVarsEqualities[var]) for var in additionalVarsEqualities.keys()]) + \
						(__indent(indentLevel) + "AND ").join(["{0} = {1}\n".format(var, substitutions[var]) for var in substitutions.keys()])
			
		elif isinstance(self.__equalityVar1, Variable) and isinstance(self.__equalityVar2, Variable):
			ecqString = __indent(indentLevel) + "SELECT dom1.individual AS {0},\n".format(self.__equalityVar1.toSQL()) + \
						__indent(indentLevel+1) + "dom2.individual as {0}\n".format(self.__equalityVar2.toSQL()) + \
						__indent(indentLevel) + "FROM _domain dom1, _domain dom2\n" + \
						__indent(indentLevel) + "WHERE dom1.individual = dom2.individual"
			
			if len(additionalVarsEqualities) > 0:
				#~ We add the statements from additionalVarsEqualities
				#~ Since the inequality only contains two variables, then additionalVarsEqualities
				#~ can contain only two keys.
				if len(additionalVarsEqualities) != 2:
					raise Exception("Something is wrong. The dictionary additionalVarsEqualities does not contain 2 values, but {0}.\n".format(len(additionalVarsEqualities)) + \
									"This is not possible since it is passed to the equality: {0}".format(self.toDL()))
				
				ecqString += "\n" + __indent(indentLevel) + "AND dom1.individual = {0}\n".format(additionalVarsEqualities[self.__equalityVar1.toSQL()])
				ecqString += __indent(indentLevel) + "AND dom2.individual = {0}\n".format(additionalVarsEqualities[self.__equalityVar2.toSQL()])
			
			#~ We add the statements from substitutions
			if len(substitutions) > 0:
				ecqString += "\n" + __indent(indentLevel) + "AND dom1.individual = {0}\n".format(substitutions[self.__equalityVar1.toSQL()])
				ecqString += __indent(indentLevel) + "AND dom2.individual = {0}\n".format(substitutions[self.__equalityVar2.toSQL()])
				
		return ecqString
	
