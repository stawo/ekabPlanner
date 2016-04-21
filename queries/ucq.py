from pyparsing import *
from itertools import *
import os

#~ Local libraries
from syntax.syntax import Syntax
from queries.cq import *

class UCQ:
	#~ An UCQ is a set of CQs.
	#~ The expression used to build an UCQ can be:
		#~ - (or CQ CQ ...)
	
	def __init__(self, queryToParse, conceptList, roleList, individualList, inequalitiesAllowed=False):			
		self.__cqs = set()
		self.__freeVars = set()
		self.__inequalitiesAllowed = False
		
		#~ Check the input
		self.__checkInput(queryToParse, conceptList, roleList, individualList, inequalitiesAllowed)
		
		self.__inequalitiesAllowed = inequalitiesAllowed
		
		#~ Parse the input
		self.__parseQuery(queryToParse, conceptList, roleList, individualList, inequalitiesAllowed=self.__inequalitiesAllowed)
		
		
	def __checkInput(self, queryToParse, conceptList, roleList, individualList, inequalitiesAllowed):
		
		if not isinstance(inequalitiesAllowed, bool):
			raise Exception("The parameter inequalitiesAllowed must be Boolean.")
		
		if not isinstance(queryToParse, (str, ParseResults, tuple, list,CQ)):
			#~ Formato non valido
			raise Exception("The provided UCQ is not in a valid format: " + str(type(queryToParse)) + "\n" + str(queryToParse))
		
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
		
		
	def __parseQuery(self, queryToParse, conceptList, roleList, individualList, inequalitiesAllowed):
		
		syntax = Syntax()
		
		result = None
		
		if isinstance(queryToParse, CQ):
			#~ We directly add the CQ to self.__cqs and exit
			self.__cqs.add(queryToParse)
			
			#~ Find the freeVars of the current UCQ.
			#~ To do so, we collect all the free vars appearing in the inner UCQs.
			self.__freeVars.update(queryToParse.freeVars())
				
			return 0
			
		#~ If queryToParse is a string, we parse it by considering the parenthesis that close every expression
		#~ and analyse the resulting pyparsing.ParseResults.
		#~ If queryToParse is already a pyparsing.ParseResults, then we analise it directly.
		elif isinstance(queryToParse, str):
			parser = StringStart() + nestedExpr() + StringEnd()
			
			result = parser.parseString(queryToParse)
			
			#~ We consider only the first element of result, since, if it is a valid list,
			#~ then result is a nested list, and thus result[0] is the actual list we
			#~ are interested in.
			result = result[0]
				
		elif isinstance(queryToParse, (ParseResults, tuple, list)):
			result = queryToParse
		
		
		if result[0] == syntax.queryOr:
			#~ The list must contain "or" plus at least two inner UCQs,
			#~ starting from element result[1].
			if len(result) <= 2:
				raise Exception("The expression \"(or ... )\" must contain at least 2 internal UCQs.")
			
			for cq in result[1:]:
				
				if isinstance(cq, CQ):
					self.__cqs.add(cq)
				else:
					self.__cqs.add(CQ(cq, conceptList, roleList, individualList, inequalitiesAllowed=self.__inequalitiesAllowed))
			
			#~ Check that all the inner UCQs have the same free variables
			for check in combinations(self.__cqs, 2):
				if check[0].freeVars() != check[1].freeVars():
					raise Exception("The UCQs have different free variables in them!\n"+str(check[0])+"\n"+str(check[1]))
		
		else:
			#~ No specific keyword is used, thus it must be a CQ
			if len(result) == 1 and isinstance(result[0],CQ):
				#~ We directly add the CQ to self.__cqs and exit
				self.__cqs.add(result[0])
				
				#~ Find the freeVars of the current UCQ.
				#~ To do so, we collect all the free vars appearing in the inner UCQs.
				self.__freeVars.update(result[0].freeVars())
					
				return 0
			else:
				self.__cqs.add(CQ(result, conceptList, roleList, individualList, inequalitiesAllowed=self.__inequalitiesAllowed))
		
		#~ Find the freeVars of the current UCQ.
		#~ To do so, we collect all the free vars appearing in the inner UCQs.
		for cq in self.__cqs:
			self.__freeVars.update(cq.freeVars())
	
	def freeVars(self):
		return self.__freeVars
	
	def terms(self):
		#~ Returns the terms used in the atoms
		terms = set()
		
		for ucq in self.__cqs:
			terms.update(ucq.terms())
		
		for atom in self.__atoms:
			terms.add(atom.term())
		
		return terms
	
	def concepts(self):
		#~ Returns the concepts used in the atoms
		concepts = set()
		
		for cq in self.__cqs:
			concepts.update(cq.concepts())
		
		return concepts
	
	def roles(self):
		#~ Returns the roles used in the atoms
		roles = set()
		
		for cq in self.__cqs:
			roles.update(cq.roles())
		
		return roles
	
	def cqs(self):
		return self.__cqs
	
	def __repr__(self):
		ucqString = ""
		
		if len(self.__cqs) >= 2:
			ucqString = "(or"
			
			for cq in self.__cqs:
				ucqString += "\n\t" + str(cq)
			
			ucqString += "\n)"
		
		elif len(self.__cqs) == 1:
			for cq in self.__cqs:
				return str(cq)
		
		return ucqString
		
	def toDL(self):
		ucqString = ""
		
		if len(self.__cqs) >= 2:
			ucqString = "("
			
			for cq in self.__cqs:
				ucqString += " " + cq.toDL() + " or "
			
			ucqString = ucqString[:-4] + " )" # remove the trailing " or "
		
		elif len(self.__cqs) == 1:
			for cq in self.__cqs:
				return str(cq)
		
		return ucqString
	
	def toADL(self, indentLevel = 0):
		
		if not isinstance(indentLevel, int) or indentLevel < 0:
			raise Exception("The parameter indentLevel must be a positive integer.")
		
		def __indent(indentLevel):
			syntax = Syntax()
			
			return syntax.indent*indentLevel
		
		ucqString = ""
		
		if len(self.__cqs) >= 2:
			ucqString = __indent(indentLevel) + "(or\n"
			
			for cq in self.__cqs:
				ucqString += cq.toADL(indentLevel+1)
			
			ucqString += __indent(indentLevel) + ")\n"
		
		elif len(self.__cqs) == 1:
			for cq in self.__cqs:
				return cq.toADL(indentLevel)
		
		return ucqString
	
	def toSQL(self, indentLevel = 0, state = 0, additionalVarsEqualities = {}, substitutions = {}):
		
		if not isinstance(indentLevel, int) or indentLevel < 0:
			raise Exception("The parameter indentLevel must be a positive integer.")
		
		if not isinstance(state, int) or state < 0:
			raise Exception("The parameter state must be a positive integer.")
		
		if not isinstance(additionalVarsEqualities, dict):
			raise Exception("The parameter additionalVarsEqualities must be a dictionary.")
		
		def __indent(indentLevel):
			syntax = Syntax()
			
			return syntax.indent*indentLevel
		
		#~ If the UCQ is boolean (thus len(self.__freeVars) == 0),
		#~ we need to create a special SQL query.
		#~ All the CQs in self.__cqs are boolean, and their translations
		#~ yeald SQL queries that return either 1 or 0 (to be interpreted as
		#~ boolean values). If at least one CQ returns 1 (True), then the
		#~ whole UCQ must return 1, 0 otherwise.
		#~ To do this we encapsulate the union of the CQs in a nested query,
		#~ while the external one takes care of checking if the nested one
		#~ contains at least one 1. Example:
		#~ SELECT COUNT(*) > 0 AS booleanValue
		#~ FROM ( inner CQs SQL query with UNION) innerCQs
		#~ WHERE innerCQs.booleanValue = 1
		if len(self.__freeVars) == 0:
			ucqString = __indent(indentLevel) + "SELECT COUNT(*) > 0 AS booleanValue\n"
			ucqString += __indent(indentLevel) + "FROM (\n"
			ucqString += str("\n\n" + __indent(indentLevel+1) + "UNION\n\n").join([cq.toSQL(indentLevel+1, state = state, additionalVarsEqualities=additionalVarsEqualities, substitutions = substitutions) for cq in self.__cqs])
			ucqString += "\n" + __indent(indentLevel) + ") innerCQs\n"
			ucqString += "\n" + __indent(indentLevel) + "WHERE innerCQs.booleanValue = 1\n"
		else:
			ucqString = str("\n\n" + __indent(indentLevel) + "UNION\n\n").join([cq.toSQL(indentLevel, state = state, additionalVarsEqualities=additionalVarsEqualities, substitutions = substitutions) for cq in self.__cqs])
		
		return ucqString
