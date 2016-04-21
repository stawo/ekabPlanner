from pyparsing import *
from itertools import *
import os

#~ Local libraries
from syntax.syntax import Syntax

class Variable:
	
	def __init__(self, name):
		
		if not isinstance(name, str):
			raise Exception("A variable name must be provided as a string.")
		
		syntax = Syntax()
		
		if name == syntax.ndnsVariable and not isinstance(self, NDNSVariable):
			raise Exception("A variable can't be named using the symbol reserverd for non-distinguished non-shared variables \"" + syntax.ndnsVariable + "\".")
			
		self.__name = name
	
	def __eq__(self, other):
		
		if isinstance(other, Variable) and str(other) == str(self):
			return True
		
		return False
	
	def __ne__(self, other):
		
		if isinstance(other, Variable) and str(other) == str(self):
			return False
		
		return True
	
	def __hash__(self):
		return hash(str(type(self)) + self.__name)
	
	def __repr__(self):
		
		return "?" + self.__name
		
	def toSQL(self):
		return self.__name
	
class NDNSVariable(Variable):
	
	def __init__(self):
		syntax = Syntax()
		self.__name = syntax.ndnsVariable
		Variable.__init__(self, syntax.ndnsVariable)
	
	#~ def __eq__(self, other):
		#~ if self is other:
			#~ return True
		
		#~ return False
	
	#~ def __ne__(self, other):
		#~ if self is other:
			#~ return False
		
		#~ return True
	
	#~ def __hash__(self):
		#~ return hash(str(type(self)) + self.__name)
	
	
class Constant:
	
	def __init__(self, name):
		
		if not isinstance(name, str):
			raise Exception("A concept name must be provided as a string.")
			
		self.__name = name
	
	def __eq__(self, other):
		
		if isinstance(other, Constant) and str(other) == self.__name:
			return True
		
		return False
		
	def __hash__(self):
		return hash(str(type(self)) + self.__name)
	
	def __repr__(self):
		return self.__name
		
	def toSQL(self):
		return self.__name
	
class QueryAtom:
	#~ A QueryAtom could be:
		#~ - (Concept ?x)
		#~ - (Role ?x ?y)
		#~ - (neq ?x ?y)  (only if inequalities are allowed)
	
	def __init__(self, atomToParse, conceptList, roleList, individualList, inequalitiesAllowed=False):
		self.__term = None
		self.__termType = None # It says what type of term is used: a concept ("concept"), a role ("role"), an inequality ("inequality")
		self.__var1 = None
		self.__var2 = None
		self.__freeVars = set()
		
		#~ Check the input
		self.__checkInput(atomToParse, conceptList, roleList, individualList, inequalitiesAllowed)
		
		self.__inequalitiesAllowed = inequalitiesAllowed
		
		#~ Parse the input
		self.__parseQuery(atomToParse, conceptList, roleList, individualList, inequalitiesAllowed=self.__inequalitiesAllowed)
		
	def __checkInput(self, atomToParse, conceptList, roleList, individualList, inequalitiesAllowed):
		
		if not isinstance(inequalitiesAllowed, bool):
			raise Exception("The parameter inequalitiesAllowed must be Boolean.")
		
		if not isinstance(atomToParse, (ParseResults, tuple, list)):
			#~ Formato non valido
			raise Exception("The provided atom is not in a valid format (should be ParseResults, or tuple, or list): " + str(type(atomToParse)))
		
		#~ The list must contain the term plus maximum two vars/constants.
		if len(atomToParse) <= 1 or len(atomToParse) > 3:
			raise Exception("The query atom must contain the term plus maximum two vars/constants.\nAtom provided: " + \
							str(atomToParse) + "\nType: " + str(type(atomToParse)))
		
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
		
	def __parseQuery(self, atomToParse, conceptList, roleList, individualList, inequalitiesAllowed):
		
		syntax = Syntax()
		
		parserTerm = StringStart() + (syntax.allowed_word^Literal(syntax.neq)) + StringEnd()
		parserVar = (StringStart() + syntax.variable + StringEnd()).leaveWhitespace()
		
		#~ Save the name of the term
		#~ I save it even if it is "neq"
		self.__term = str(parserTerm.parseString(atomToParse[0])[0])
		
		if self.__term == syntax.neq:
			#~ - (neq ?x ?y)  (only if inequalities are allowed)
			
			if not inequalitiesAllowed :
				raise Exception("The CQ can't contain inequalities. Set the option \"inequalitiesAllowed\" to True.")
			
			#~ It must have 3 elements:
			if len(atomToParse) != 3:
				raise Exception("An inequality must have 3 elements \"(neq var1 var2)\"")
			
			#~ Save the type of atom
			self.__termType = "inequality"
			
			#~ Check if the second element atomToParse[1] is a variable
			if isinstance(atomToParse[1], Variable):
				self.__var1 = atomToParse[1]
				self.__freeVars.add(self.__var1)
			
			elif str(atomToParse[1])[0] == "?":
				self.__var1 = Variable(str(parserVar.parseString(atomToParse[1])[0]))
				self.__freeVars.add(self.__var1)
			else:
				raise Exception("An inequality must be about two variables. The term \""+ str(atomToParse[1]) + "\" is not one.")
			
			#~ Check if the third element atomToParse[1] is a variable
			if isinstance(atomToParse[2], Variable):
				self.__var2 = atomToParse[2]
				self.__freeVars.add(self.__var2)
			
			elif str(atomToParse[2])[0] == "?":
				self.__var2 = Variable(str(parserVar.parseString(atomToParse[2])[0]))
				self.__freeVars.add(self.__var2)
			else:
				raise Exception("An inequality must be about two variables. The term \""+ str(atomToParse[2]) + "\" is not one.")
			
			#~ The variables have to be different from each other, we don't
			#~ accept an inequality of the type (neq ?x ?x).
			#~ If this is the case, we raise an Exception.
			if self.__var1 == self.__var2:
				raise Exception("The variables provided in the inequality statement are the same. Please adjust/remove the atom: (neq ?" + self.__var1 + " ?" + self.__var2 + ")")
			
		else:
			#~ Check how many elements there are
			if len(atomToParse) == 2:
				#~ - (Concept ?x)
				self.__termType = "concept"
				
				if not self.__term in conceptList:
					raise Exception("The term used in the Query Atom is not a valid concept.\n" + str(atomToParse))
				
				#~ Check if the second element atomToParse[1] is a variable
				if isinstance(atomToParse[1], Variable):
					self.__var1 = atomToParse[1]
					self.__freeVars.add(self.__var1)
				
				elif isinstance(atomToParse[1], Constant):
					self.__var1 = atomToParse[1]
					
					if not str(self.__var1) in individualList:
						raise Exception("The term " + str(self.__var1) + " used in the Query Atom is not a valid individual.\n" + str(atomToParse))
					
				elif str(atomToParse[1])[0] == "?":
					self.__var1 = Variable(str(parserVar.parseString(atomToParse[1])[0]))
					self.__freeVars.add(self.__var1)
				else:
					
					self.__var1 = Constant(str(parserTerm.parseString(atomToParse[1])[0]))
					
					if not str(self.__var1) in individualList:
						raise Exception("The term " + str(self.__var1) + " used in the Query Atom is not a valid individual.\n" + str(atomToParse))
					
			else:
				#~ - (Role ?x ?y)
				self.__termType = "role"
				
				if not self.__term in roleList:
					raise Exception("The term " + self.__term + " used in the Query Atom is not a valid role.\n" + str(atomToParse))
				
				#~ Check if the second element atomToParse[1] is a variable
				if isinstance(atomToParse[1], Variable):
					self.__var1 = atomToParse[1]
					self.__freeVars.add(self.__var1)
				
				elif isinstance(atomToParse[1], Constant):
					self.__var1 = atomToParse[1]
					
					if not str(self.__var1) in individualList:
						raise Exception("The term " + str(self.__var1) + " used in the Query Atom is not a valid individual.\n" + str(atomToParse))
					
				elif str(atomToParse[1])[0] == "?":
					self.__var1 = Variable(str(parserVar.parseString(atomToParse[1])[0]))
					self.__freeVars.add(self.__var1)
				else:
					self.__var1 = Constant(str(parserTerm.parseString(atomToParse[1])[0]))
					
					if not str(self.__var1) in individualList:
						raise Exception("The term " + str(self.__var1) + " used in the Query Atom is not a valid individual.\n" + str(atomToParse))
					
				#~ Check if the third element atomToParse[1] is a variable
				if isinstance(atomToParse[2], Variable):
					self.__var2 = atomToParse[2]
					self.__freeVars.add(self.__var2)
				
				elif isinstance(atomToParse[2], Constant):
					self.__var2 = atomToParse[2]
					
					if not str(self.__var2) in individualList:
						raise Exception("The term " + str(self.__var2) + " used in the Query Atom is not a valid individual.\n" + str(atomToParse))
					
				elif str(atomToParse[2])[0] == "?":
					self.__var2 = Variable(str(parserVar.parseString(atomToParse[2])[0]))
					self.__freeVars.add(self.__var2)
				else:
					self.__var2 = Constant(str(parserTerm.parseString(atomToParse[2])[0]))
					
					if not str(self.__var2) in individualList:
						raise Exception("The term " + str(self.__var2) + " used in the Query Atom is not a valid individual.\n" + str(atomToParse))
					
	def term(self):
		return 	self.__term
	
	def atomType(self):
		return self.__termType
	
	def var1(self):
		return self.__var1
	
	def var2(self):
		return self.__var2
	
	def freeVars(self):
		return self.__freeVars
	
	def __eq__(self, other):
		#~ A query atom is equal to another if they use the same term and the same variables/constants in the same position.
		
		if not isinstance(other, QueryAtom): return False
		if self.__term != other.term(): return False
		if self.__var1 != other.var1(): return False
		if self.__var2 != other.var2(): return False
		
		return True
		
	
	def __ne__(self, other):
		#~ A query atom is equal to another if they use the same term and the same variables/constants in the same position.
		
		if not isinstance(other, QueryAtom): return True
		if self.__term != other.term(): return True
		if self.__var1 != other.var1(): return True
		if self.__var2 != other.var2(): return True
		
		return False
	
	def __hash__(self):
		
		return hash(str(type(self)) + str(self.__term) + str(self.__termType) + \
					str(hash(self.__var1)) + str(type(self.__var1)) + \
					str(hash(self.__var2)) + str(type(self.__var2)))
		
	def __repr__(self):
		atomString =  "(" + self.__term + " " + str(self.__var1)
		
		if not self.__var2 is None:
			atomString += " " + str(self.__var2)
			
		atomString += ")"
		
		return atomString
	
	def toDL(self):
		
		atomString = ""
		
		if self.__termType == "inequality":
			atomString = "( " + str(self.__var1) + " \\neq " + str(self.__var2) + ")"
			
		else:
			atomString =  self.__term + "(" + str(self.__var1)
			
			if not self.__var2 is None:
				atomString += " " + str(self.__var2)
			
			atomString += ")"
		
		return atomString
	
	def toADL(self, indentLevel = 0):
		
		if not isinstance(indentLevel, int) or indentLevel < 0:
			raise Exception("The parameter indentLevel must be a positive integer.")
		
		def __indent(indentLevel):
			syntax = Syntax()
			
			return syntax.indent*indentLevel
		
		atomString =  __indent(indentLevel) + "(" + self.__term + " " + str(self.__var1)
		
		if not self.__var2 is None:
			atomString += " " + str(self.__var2)
			
		atomString += ")\n"
		
		return atomString
	
class CQ:
	#~ A CQ, instead, could be one of the following expressions:
		#~ - (and QueryAtom QueryAtom ...)
		#~ - (exists (Vars) (and QueryAtom QueryAtom ...))
		#~ - (exists (Vars) (QueryAtom))
		#~ - (QueryAtom)
	
	def __init__(self, queryToParse, conceptList, roleList, individualList, inequalitiesAllowed=False):			
		self.__atoms = set()
		self.__freeVars = set()
		self.__existentialVars = set()
		self.__inequalitiesAllowed = False
		
		#~ Check the input
		self.__checkInput(queryToParse, conceptList, roleList, individualList, inequalitiesAllowed)
		
		self.__inequalitiesAllowed = inequalitiesAllowed
		
		#~ Parse the input
		self.__parseQuery(queryToParse, conceptList, roleList, individualList, inequalitiesAllowed=self.__inequalitiesAllowed)
		
		
	
	def __checkInput(self, queryToParse, conceptList, roleList, individualList, inequalitiesAllowed):
		
		if not isinstance(inequalitiesAllowed, bool):
			raise Exception("The parameter inequalitiesAllowed must be Boolean.")
		
		if not isinstance(queryToParse, (str, ParseResults, tuple, list, dict)):
			#~ Formato non valido
			raise Exception("The provided CQ is not in a valid format: " + str(type(queryToParse)) + "\n" + str(queryToParse))
		
		#~ If queryToParse is a dict, it can contain the following keywords:
		#~ queryAtoms: a list,set,tuple of QueryAtom
		#~ existentialVars: a list,set,tuple of Variable, NSNDVariable
		if isinstance(queryToParse, dict):
			if not set(queryToParse.keys()).issubset({"queryAtoms","existentialVars"}) or \
				not "queryAtoms" in queryToParse.keys() or \
				not isinstance(queryToParse["queryAtoms"], (list, tuple,set)) or \
				not all(isinstance(queryAtom, QueryAtom) for queryAtom in queryToParse["queryAtoms"]):
				raise Exception("The query provided as a dictionary is not well formed:\n" + str(queryToParse))
			
			if "existentialVars" in queryToParse.keys() and \
				(not isinstance(queryToParse["existentialVars"], (list, tuple,set)) or \
				not all(isinstance(var, Variable) for var in queryToParse["existentialVars"])):
				raise Exception("The query provided as a dictionary is not well formed:\n" + str(queryToParse))
		
		#~ conceptList, roleList, and individualList, if not None, must be lists of strings
		if not (isinstance(conceptList, (list, tuple, set)) and \
			all(isinstance(concept, str) for concept in conceptList)):
			raise Exception("The concept list provided is not valid. It must be a list of strings.")
		
		if not (isinstance(roleList, (list, tuple, set)) and \
			all(isinstance(role, str) for role in roleList)):
			raise Exception("The role list provided is not valid. It must be a list of strings.")
		
		
	def __parseQuery(self, queryToParse, conceptList, roleList, individualList, inequalitiesAllowed):
		
		#~ If queryToParse is a dict, it can contain the following keywords:
		#~ queryAtoms: a list,set,tuple of QueryAtom
		#~ existentialVars: a list,set,tuple of Variable, NSNDVariable
		if isinstance(queryToParse, dict):
			#~ Add the query atoms to self.__atoms
			self.__atoms.update(queryToParse["queryAtoms"])
			
			#~ If the dict contains the key "existentialVars", then we add them to self.__existentialVars
			if "existentialVars" in queryToParse.keys():
				self.__existentialVars.update(queryToParse["existentialVars"])
			
		else:		
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
			
			#~ elif isinstance(queryToParse, CQ):
				#~ return queryToParse
			
			#~ if isinstance(result[0], QueryAtom):
				
			if result[0] == syntax.exists:
				
				#~ If the first keyword is "exists", then the CQ has some existential
				#~ variables. We store them, and process the internal CQ (saved in result[2])
				#~ which could be a CQ, or simply an atomic query.
				
				#~ The element result[1] must contain the existential variables,
				#~ while result[2] the inner CQ.
				#~ result must contain exactly 3 elements
				if len(result) != 3 or not isinstance(result[1], (ParseResults, tuple, list)) or not isinstance(result[2], (ParseResults, tuple, list)):
					raise Exception("The expression \"(exists (Vars) (CQ) )\" must contain only a set of existential variables and one CQ.")
					
				#~ Check that variables are syntactically valid (i.e. "?"+ a valid string)
				#~ and add them to self.__existentialVars
				varName = (StringStart() + syntax.variable.setResultsName("varName") + StringEnd()).leaveWhitespace()
				for varString in result[1]:
					self.__existentialVars.add(Variable(varName.parseString(varString)[0]))
				
				if result[2][0] == syntax.queryAnd:
					#~ The CQ is given as a conjunction of atoms.
					#~ There must be at least 2 atoms in the list, thus 
					#~ result must contain more than 3 elements
					if len(result[2]) < 3:
						raise Exception("The expression \"(and CQ CQ ... )\" must contain at least 2 CQs.")
					
					for atom in result[2][1:]:
						self.__atoms.add(QueryAtom(atom, conceptList, roleList, individualList, inequalitiesAllowed=self.__inequalitiesAllowed))
				
				else:
					#~ No specific keyword is used, thus it must be a single query atom
					self.__atoms.add(QueryAtom(result[2], conceptList, roleList, individualList, inequalitiesAllowed=self.__inequalitiesAllowed))	
					
			elif result[0] == syntax.queryAnd:
				#~ The CQ is given as a conjunction of atoms.
				#~ There must be at least 2 atoms in the list, thus 
				#~ result must contain more than 3 elements
				if len(result) < 3:
					raise Exception("The expression \"(and CQ CQ ... )\" must contain at least 2 CQs.")
				
				for atom in result[1:]:
					self.__atoms.add(QueryAtom(atom, conceptList, roleList, individualList, inequalitiesAllowed=self.__inequalitiesAllowed))
					
			else:
				#~ No specific keyword is used, thus it must be a single query atom
				self.__atoms.add(QueryAtom(result, conceptList, roleList, individualList, inequalitiesAllowed=self.__inequalitiesAllowed))
				
		
		#~ Check that each atom of the CQ has the same free variables
		#~ for (atom1, atom2) in combinations(self.__atoms,2):
			#~ if (atom1.freeVars()).difference(self.__existentialVars) != (atom2.freeVars()).difference(self.__existentialVars):
				#~ raise Exception("The following CQ contains atoms whose free variables are not the same.\n" + str(self))
				
		#~ Find the freeVars of the current CQ.
		#~ To do so, we collect all the free vars in the atoms,
		#~ and remove the one that are set as existential in the current CQ.
		for atom in self.__atoms:
			self.__freeVars.update(atom.freeVars())
		
		#~ Check that variables marked as existential are free variables
		#~ in the inner atoms, otherwise raise an Exception.
		if not self.__existentialVars.issubset(self.__freeVars):
			raise Exception("The existential variable(s) " + str(self.__existentialVars.difference(self.__freeVars)) + " do(es) not appear in any inner query atom.")
		
		self.__freeVars = self.__freeVars.difference(self.__existentialVars) # remove the variables that are set as existential in the current CQ.
		
	def __eq__(self, other):
		#~ A CQ is equal to another if they use the same query atoms and have the same existential variables.
		
		if not isinstance(other, CQ): return False
		if self.__existentialVars != other.existentialVars(): return False
		if self.__atoms != other.queryAtoms(): return False
		
		return True
		
	def __ne__(self, other):
		#~ A CQ is equal to another if they use the same query atoms and have the same existential variables.
		
		if not isinstance(other, CQ): return True
		if self.__existentialVars != other.existentialVars(): return True
		if self.__atoms != other.queryAtoms():  return True
		
		return False
	
	def __hash__(self):
		
		hashString = ""
		#~ Add the hash representation of each atom
		for atom in self.__atoms:
			hashString += (str(hash(atom)))
		
		#~ Add the hash representation of each existential var. It could be that nothing is added
		for existentialVar in self.__existentialVars:
			hashString += str(hash(existentialVar))
			
		return hash(str(type(self)) + hashString)
		
	def freeVars(self):
		return self.__freeVars
	
	def existentialVars(self):
		return self.__existentialVars
	
	def queryAtoms(self):
		return self.__atoms
		
	def terms(self):
		#~ Returns the terms used in the atoms
		terms = set()
		
		for atom in self.__atoms:
			terms.add(atom.term())
		
		return terms
	
	def concepts(self):
		#~ Returns the concepts used in the atoms
		concepts = set()
		
		for atom in self.__atoms:
			if atom.atomType() == "concept":
				concepts.add(atom.term())
		
		return concepts
	
	def roles(self):
		#~ Returns the roles used in the atoms
		roles = set()
		
		for atom in self.__atoms:
			if atom.atomType() == "role":
				roles.add(atom.term())
		
		return roles
	
	def __repr__(self):
		cqString = ""
		
		if len(self.__existentialVars) > 0:
			cqString = "(exists ( " + \
						" ".join([str(var) for var in self.__existentialVars]) + \
						" ) "
			
			if len(self.__atoms) > 1:
				cqString += "(and " + " ".join([str(atom) for atom in self.__atoms]) + " )"
			else:
				cqString += " ".join([str(atom) for atom in self.__atoms])
				
			cqString += " )"
		
		else:
			#~ There are no existential vars to add
			if len(self.__atoms) > 1:
				cqString += "(and " + " ".join([str(atom) for atom in self.__atoms]) + " )"
			else:
				cqString += " ".join([str(atom) for atom in self.__atoms])
		
		return cqString
		
	def toDL(self):
		cqString = ""
		
		if len(self.__existentialVars) > 0:
			cqString = "exists " + ",".join([str(var) for var in self.__existentialVars]) + ". "
			
			if len(self.__atoms) == 1:
				for atom in self.__atoms:
					cqString += atom.toDL()
			elif len(self.__atoms) > 1:
				cqString += "( " + " and ".join([atom.toDL() for atom in self.__atoms]) + " )"
			
			cqString += " "
		
		else:
			#~ There are no existential vars to add
			if len(self.__atoms) == 1:
				for atom in self.__atoms:
					cqString += atom.toDL()
			elif len(self.__atoms) > 1:
				cqString += "( " + " and ".join([atom.toDL() for atom in self.__atoms]) + " )"
		
		return cqString
	
	def toADL(self, indentLevel = 0):
		
		if not isinstance(indentLevel, int) or indentLevel < 0:
			raise Exception("The parameter indentLevel must be a positive integer.")
		
		def __indent(indentLevel):
			syntax = Syntax()
			
			return syntax.indent*indentLevel
		
		cqString = ""
		
		if len(self.__existentialVars) > 0:
			cqString = __indent(indentLevel) + "(exists (" + " ".join([str(var) for var in self.__existentialVars]) + " )\n"
			
			if len(self.__atoms) == 1:
				for atom in self.__atoms:
					cqString += atom.toADL(indentLevel+1)
			elif len(self.__atoms) > 1:
				cqString += __indent(indentLevel+1) + "(and\n"
				for atom in self.__atoms:
					cqString += atom.toADL(indentLevel+2)
				cqString += __indent(indentLevel+1) + ")\n"
			
			cqString += __indent(indentLevel) + ")\n"
		
		else:
			#~ There are no existential vars to add
			if len(self.__atoms) == 1:
				for atom in self.__atoms:
					cqString += atom.toADL(indentLevel)
			elif len(self.__atoms) > 1:
				cqString += __indent(indentLevel) + "(and\n"
				for atom in self.__atoms:
					cqString += atom.toADL(indentLevel+1)
				cqString += __indent(indentLevel) + ")\n"
		
		return cqString
	
	def toSQL(self, indentLevel = 0, state = 0, additionalVarsEqualities = {}, substitutions = {}):
		
		#~ DA METTERE A POSTO DESCRIZIONE
		#~ -------------------
		#~ -------------------
		#~ -------------------
		#~ -------------------
		#~ -------------------
		#~ -------------------
		#~ -------------------
		#~ -------------------
		#~ -------------------
		#~ -------------------
		#~ -------------------
		#~ -------------------
		
		"""
		Example of CQ translated to SQL
		(student, address) . \exists (student2, course) .
			attends(student, course) and gender(student, 'male') and
			attends(student2, course) and
			gender(student2, 'female') and lives(student, address)


		select l.dom as student, l.ran as address
		from attends a1, gender g1,
			  attends a2, gender g2,
			  lives l
		where a1.dom=g1.dom
		and   a2.dom=g2.dom
		and   l.dom=g1.dom
		and   a1.ran=a2.ran
		and   g1.ran='male'
		and   g2.ran='female';
		"""
		
		
		if not isinstance(indentLevel, int) or indentLevel < 0:
			raise Exception("The parameter indentLevel must be a positive integer.")
		
		if not isinstance(state, int) or state < 0:
			raise Exception("The parameter state must be a positive integer.")
		
		if not isinstance(additionalVarsEqualities, dict):
			raise Exception("The parameter additionalVarsEqualities must be a dictionary.")
		
		def __indent(indentLevel):
			syntax = Syntax()
			
			return syntax.indent*indentLevel
		
		syntax = Syntax()
		
		#~ Create a copy of the query atoms list and add an alias for each of them.
		#~ To create an alias, we just add a counter at the end of the name.
		#~ The terms used in the query atoms represent a table in the DB.
		#~ We do not consider inequalities.
		queryAtomsAliases = dict()
		counter = 0
		for atom in self.__atoms:
			if atom.atomType() != "inequality":
				queryAtomsAliases[(atom.term()+str(counter))] = atom
				
				counter += 1
		
		#~ Define, for each variable that appears in the query (both free and
		#~ existential), to which table and column they are linked.
		#~ We need this both for the SELECT statement (we use aliases for the
		#~ variables, e.g. SELECT term.termDomain as x), and for inequalities
		#~ (e.g. we translate x != y in term1.termDomain != term2.termRange)
		varsStatement = dict()
		for variable in self.__freeVars:
			for alias in queryAtomsAliases.keys():
				
				if variable == queryAtomsAliases[alias].var1():
					#~ The variable appears in the domain of the term of this query atom
					varsStatement[variable.toSQL()] = alias + ".termDomain"
					
					#~ Pass to the next variable
					break
				
				if variable == queryAtomsAliases[alias].var2():
					#~ The variable appears in the domain of the term of this query atom
					varsStatement[variable.toSQL()] = alias + ".termRange"
					
					#~ Pass to the next variable
					break
		
		for variable in self.__existentialVars:
			for alias in queryAtomsAliases.keys():
				
				if variable == queryAtomsAliases[alias].var1():
					#~ The variable appears in the domain of the term of this query atom
					varsStatement[variable.toSQL()] = alias + ".termDomain"
					
					#~ Pass to the next variable
					break
				
				if variable == queryAtomsAliases[alias].var2():
					#~ The variable appears in the domain of the term of this query atom
					varsStatement[variable.toSQL()] = alias + ".termRange"
					
					#~ Pass to the next variable
					break
		
		#~ Definition of the SELECT section of the SQL query
		if len(self.__freeVars) > 0:
			#~ The query contains free variables, thus the SELECT section
			#~ of the SQL query is composed by all the variables appearing
			#~ as aliases of the respective tables and columns
			sqlSelect = __indent(indentLevel) + "SELECT DISTINCT " + \
						str(",\n" + __indent(indentLevel+1)).join([(varsStatement[var.toSQL()] + " AS " + var.toSQL()) for var in self.__freeVars])
		else:
			#~ The query is boolean, thus there are no free variables.
			#~ To represent this in SQL, we make the SQL query
			#~ return either 1 or 0, depending if there are results or not.
			#~ To achieve this, we use the function COUNT(*) > 0, and
			#~ give it the alias of "booleanValue"
			sqlSelect = __indent(indentLevel) + "SELECT DISTINCT COUNT(*) > 0 AS booleanValue"
			
		#~ The FROM section of the SQL query is composed by all the 
		#~ query atoms terms and their aliases, i.e.:
		#~ FROM Term1 Alias1,
		#~ 		Term1 Alias2,
		#~ 		Term2 Alias3,
		#~ 		...
		sqlFrom = __indent(indentLevel) + "FROM " + \
					str(",\n" + __indent(indentLevel+1)).join([(str(queryAtomsAliases[alias].term()) + " " + str(alias)) for alias in queryAtomsAliases.keys()])
		
		
		#~ The WHERE and AND section of the SQL query is done by:
		#~ - checking whether each combination of query atoms (we do not
		#~   consider couples of the same atoms) share one of the variables.
		#~   In such a case we generate a properly built equality.
		#~ - checking whenever an atom uses a constant.
		#~   We generate a properly built equality.
		#~ - generate equalities regarding the state of the eKab that
		#~   we want to get the results from.
		#~ - generate equalities for the variables that appear in the
		#~   substitutions.
		whereStatements = set()
		for var in substitutions.keys():
			if var in varsStatement.keys():
				#~ Add the statement regarding the var assuming a specific value expressed in the substitution
				whereStatements.add("{0} = '{1}'".format(varsStatement[var],substitutions[var]))
				
		for alias in queryAtomsAliases.keys():
			#~ Add the statement regarding the state for each term
			whereStatements.add(str(alias + ".state = " + str(state)))
		
		for var in additionalVarsEqualities.keys():
			#~ The equality regards a variable (e.g., a parameter of an action)
			#~ that appears in two SQL queries (one external, and one internal)
			#~ and has to be linked in these queries through the aliases used for
			#~ that variable in the queries.
			whereStatements.add("{0} = {1}".format(varsStatement[var], str(additionalVarsEqualities[var])) )
		
		for (alias1, alias2) in combinations(queryAtomsAliases.keys(),2):
			#~ Check if the first atom uses constants.
			if isinstance(queryAtomsAliases[alias1].var1(), Constant):
				#~ The first position uses a constant.
				#~ We generate the equality:
				#~ Term.termDomain = constant
				whereStatements.add(str("{0}.termDomain = `{1}`".format(alias1,str(queryAtomsAliases[alias1].var1()))))
			if not queryAtomsAliases[alias1].var2() is None and isinstance(queryAtomsAliases[alias1].var2(), Constant):
				#~ The second position uses a constant.
				#~ We generate the equality:
				#~ Term.termRange = constant
				whereStatements.add(str("{0}.termRange = `{1}`".format(alias1,str(queryAtomsAliases[alias1].var2()))))
			
			#~ Check if the second atom uses constants.
			if isinstance(queryAtomsAliases[alias2].var1(), Constant):
				#~ The first position uses a constant.
				#~ We generate the equality:
				#~ Term.termDomain = constant
				whereStatements.add(str("{0}.termDomain = `{1}`".format(alias2,str(queryAtomsAliases[alias2].var1()))))
			if not queryAtomsAliases[alias2].var2() is None and isinstance(queryAtomsAliases[alias2].var2(), Constant):
				#~ The second position uses a constant.
				#~ We generate the equality:
				#~ Term.termRange = constant
				whereStatements.add(str("{0}.termRange = `{1}`".format(alias2,str(queryAtomsAliases[alias2].var2()))))
			
			#~ Check if the two terms share some variables
			if isinstance(queryAtomsAliases[alias1].var1(), Variable):
				
				if isinstance(queryAtomsAliases[alias1].var2(), Variable) and queryAtomsAliases[alias1].var1() == queryAtomsAliases[alias1].var2():
					#~ The term 1 uses the same variable in both domain and range
					#~ We generate the equality:
					#~ Term.termDomain = Term.termRange
					whereStatements.add(str(alias1 + ".termDomain = " + alias1 + ".termRange"))
				
				if isinstance(queryAtomsAliases[alias2].var1(), Variable) and queryAtomsAliases[alias1].var1() == queryAtomsAliases[alias2].var1():
					#~ The term 1 uses the same variable as Term 2 for the domain
					#~ We generate the equality:
					#~ Term1.termDomain = Term2.termDomain
					whereStatements.add(str(alias1 + ".termDomain = " + alias2 + ".termDomain"))
				
				if isinstance(queryAtomsAliases[alias2].var2(), Variable) and queryAtomsAliases[alias1].var1() == queryAtomsAliases[alias2].var2():
					#~ The term 1 uses for the domain the same variable as Term 2 uses for the range
					#~ We generate the equality:
					#~ Term1.termDomain = Term2.termRange
					whereStatements.add(str(alias1 + ".termDomain = " + alias2 + ".termRange"))
			
			if isinstance(queryAtomsAliases[alias1].var2(), Variable):
				
				if isinstance(queryAtomsAliases[alias2].var1(), Variable) and queryAtomsAliases[alias1].var2() == queryAtomsAliases[alias2].var1():
					#~ The term 1 uses for the range the same variable as Term 2 uses for the domain
					#~ We generate the equality:
					#~ Term1.termDomain = Term2.termDomain
					whereStatements.add(str(alias1 + ".termRange = " + alias2 + ".termDomain"))
				
				if isinstance(queryAtomsAliases[alias2].var2(), Variable) and queryAtomsAliases[alias1].var2() == queryAtomsAliases[alias2].var2():
					#~ The term 1 uses the same variable as Term 2 for the range
					#~ We generate the equality:
					#~ Term1.termDomain = Term2.termRange
					whereStatements.add(str(alias1 + ".termRange = " + alias2 + ".termRange"))
			
			if isinstance(queryAtomsAliases[alias2].var1(), Variable):
				
				if isinstance(queryAtomsAliases[alias2].var2(), Variable) and queryAtomsAliases[alias2].var1() == queryAtomsAliases[alias2].var2():
					#~ The term 2 uses the same variable in both domain and range
					#~ We generate the equality:
					#~ Term.termDomain = Term.termRange
					whereStatements.add(str(alias2 + ".termDomain = " + alias2 + ".termRange"))
				
		#~ Add the inequalities
		for atom in self.__atoms:
			if atom.atomType() == "inequality":
				whereStatements.add(str(varsStatement[atom.var1().toSQL()] + " <> " + varsStatement[atom.var2().toSQL()]))
		
		#~ Create the WHERE statement
		sqlWhere = __indent(indentLevel) + "WHERE " + str("\n" + __indent(indentLevel) + "AND ").join(whereStatements)
		
		
			
		return sqlSelect + "\n" + sqlFrom + "\n" + sqlWhere
