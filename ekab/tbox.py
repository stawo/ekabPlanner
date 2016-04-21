from pyparsing import *

#~ Local libraries
from syntax.syntax import Syntax

class Concept:
	
	def __init__(self, name):
		
		if not isinstance(name, str):
			raise Exception("A concept name must be provided as a string.")
			
		self.__name = name
	
	def __repr__(self):
		
		return self.__name
		
	def __eq__(self, other):
		
		if isinstance(other, Concept) and str(other) == self.__name:
			return True
		
		return False
		
	def __hash__(self):
		return hash(self.__name) 

class Role:
	
	def __init__(self, name):
		
		if not isinstance(name, str):
			raise Exception("A role name must be provided as a string.")
			
		self.__name = name
	
	def __repr__(self):
		
		return self.__name
		
	def __eq__(self, other):
		
		if isinstance(other, Role) and str(other) == self.__name:
			return True
		
		return False
		
	def __hash__(self):
		return hash(self.__name)
		
class Axiom:
	
	def __init__(self, axiomToParse, conceptList, roleList):
		#~ The function __init__ takes as input:
			#~ - axiomToParse: the axiom that needs to be parsed.
			#~ - conceptList: a (possibly empty) list (or set, or tuple) of concepts. It is used to validate the assertion.
			#~ - roleList: a (possibly empty) list (or set, or tuple) of roles. It is used to validate the assertion.
			
		self.__leftTerm = None
		self.__leftTermExists = False
		self.__leftTermInverse = False
		self.__rightTerm = None
		self.__rightTermExists = False
		self.__rightTermInverse = False
		self.__disjoint = False
		self.__functionality = False
		
		#~ Check the input
		self.__checkInput(axiomToParse, conceptList, roleList)
		
		#~ Parse the input
		self.__parseAxiom(axiomToParse, conceptList, roleList)
		
		
	
	def __checkInput(self, axiomToParse, conceptList, roleList):
		
		if not isinstance(axiomToParse, (str, ParseResults, tuple, list)):
			#~ Formato non valido
			raise Exception("The provided axiom is not in a valid format: " + str(type(axiomToParse)) + "\n" + str(axiomToParse))
		
		#~ conceptList and roleList, if not None, must be lists of strings
		if not (isinstance(conceptList, (list, tuple, set)) and \
			all(isinstance(concept, str) for concept in conceptList)):
			raise Exception("The concept list provided is not valid. It must be a list of strings.")
		
		if not (isinstance(roleList, (list, tuple, set)) and \
			all(isinstance(role, str) for role in roleList)):
			raise Exception("The role list provided is not valid. It must be a list of strings.")
	
	def __checkConcept(self, term, conceptList):
		#~ Checks if term is a valid concept.
		#~ term must not be a reserved keyword,
		#~ and must be in conceptList
		#~ Returns True if it is valid, False otherwise
		
		if not isinstance(term, str):
			raise Exception("The term passed to the function __checkConcept must be a string: " + str(type(term)))
		
		syntax = Syntax()
		
		#~ The term can't be a reserved keyword
		if term in syntax.keywords:
			return False
			
		if not term in conceptList:
			return False
		
		return True
	
	def __checkRole(self, term, roleList):
		#~ Checks if term is a valid role.
		#~ term must not be a reserved keyword,
		#~ and must be in roleList
		#~ Returns True if it is valid, False otherwise
		
		if not isinstance(term, str):
			raise Exception("The term passed to the function __checkConcept must be a string: " + str(type(term)))
		
		syntax = Syntax()
		
		#~ The term can't be a reserved keyword
		if term in syntax.keywords:
			return False
			
		if not term in roleList:
			return False
		
		return True
		
	def __parseAxiom(self, axiomToParse, conceptList, roleList):
		
		#~ (isA  above     :topC     )
		#~ (isA  above  (not (exists   (inverse next ))   )  )
		#~ (isA  (exists  next ) (not (exists reachable-floor)  )  )
		#~ (isA next (not reachable-floor))
		#~ (funct (inverse next ))
		
		syntax = Syntax()
		
		#~ If axiomToParse is a string, we parse it by considering the parenthesis that close every expression
		#~ and analyse the resulting pyparsing.ParseResults.
		#~ If axiomToParse is already a pyparsing.ParseResults (or a list, or a tuple), then we analise it directly.
		result = None
		if isinstance(axiomToParse, str):
			raise Exception("Sorry, at the moment we can't parse axioms that are passed as a string.\n" + axiomToParse)
		
		elif isinstance(axiomToParse, (ParseResults, tuple, list)):
			result = axiomToParse
			
		if isinstance(result[0], str) and result[0] == syntax.isA:
			#~ We have either a positive or negative axiom, for sure not a functional one
			
			#~ Parse the first term
			if isinstance(result[1], str):
				#~ The first term is either an atomic concept A or atomic role P
				
				if not (self.__checkConcept(result[1], conceptList) or self.__checkRole(result[1], roleList)):
					raise Exception("The term \"" + result[1] + "\" is not valid, it can't be used to build the following axiom:\n" + str(result))
				
				self.__leftTerm = result[1]
			
			elif isinstance(result[1], (ParseResults, tuple, list)):
				
				if isinstance(result[1][0], str) and result[1][0] == syntax.exists:
					
					if isinstance(result[1][1], str):
						#~ It's the term: exists P
						
						if not self.__checkRole(result[1][1], roleList):
							#~ The term is in neither lists
							raise Exception("The term \"" + result[1][1] + "\" used for the following axiom is not a valid role.\n" + str(result))
							
						self.__leftTerm = result[1][1]
						self.__leftTermExists = True
					
					elif isinstance(result[1][1], (ParseResults, tuple, list)) and \
						isinstance(result[1][1][0], str) and result[1][1][0] == syntax.inverse and \
						isinstance(result[1][1][1], str):
						#~ It's the term: exists P^-
						
						if not self.__checkRole(result[1][1][1], roleList):
							#~ The term is in neither lists
							raise Exception("The term \"" + result[1][1][1] + "\" used for the following axiom is not a valid role.\n" + str(result))
							
						
						self.__leftTerm = result[1][1][1]
						self.__leftTermExists = True
						self.__leftTermInverse = True
					
					else:
						#~ Something is wrong.
						raise Exception("The left term of the following axiom was not recognized as a valid one.\n" + str(result))
					
				elif isinstance(result[1][0], str) and result[1][0] == syntax.inverse and \
					isinstance(result[1][1], str):
					#~ It's the term: P^-
					
					if not self.__checkRole(result[1][1], roleList):
						#~ The term is in neither lists
						raise Exception("The term \"" + result[1][1] + "\" used for the following axiom is not a valid role.\n" + str(result))
							
					self.__leftTerm = result[1][1]
					self.__leftTermInverse = True
				
				else:
					#~ Something is wrong.
					raise Exception("The left term of the following axiom was not recognized as a valid one.\n" + str(result))
			
			else:
				#~ Something is wrong.
				raise Exception("The left term of the following axiom was not recognized as a valid one.\n" + str(result))
			
			#~ Parse the second term
			if isinstance(result[2], str):
				#~ The second term is either an atomic concept A or atomic role P
				
				if not (self.__checkConcept(result[2], conceptList) or self.__checkRole(result[2], roleList)):
					raise Exception("The term \"" + result[2] + "\" is not valid, it can't be used to build the following axiom:\n" + str(result))
				
				if self.__checkConcept(self.__leftTerm, conceptList) and self.__checkRole(result[2], roleList):
					raise Exception("The term \"" + result[2] + "\" is a role, while \"" + self.__leftTerm + "\" is a concept.\nIt can't be used to build the following axiom:\n" + str(result))
					
				if not self.__leftTermExists and \
					self.__checkRole(self.__leftTerm, roleList) and \
					not self.__checkRole(result[2], roleList):
					raise Exception("The term \"" + result[2] + "\" is not a role, while \"" + self.__leftTerm + "\" is.\nIt can't be used to build the following axiom:\n" + str(result))
					
				self.__rightTerm = result[2]
			
			elif isinstance(result[2], (ParseResults, tuple, list)):
				
				if isinstance(result[2][0], str) and result[2][0] == syntax.exists:
					
					if isinstance(result[2][1], str):
						#~ It's the term: exists P
						
						if not self.__checkRole(result[2][1], roleList):
							raise Exception("The term \"" + result[2][1] + "\" is not a valid role, it can't be used to build the following axiom:\n" + str(result))
						
						#~ If the first term is either P or P^-, then we raise an Exception
						if not self.__leftTermExists and self.__checkRole(self.__leftTerm, roleList):
							raise Exception("The term \"" + result[2][1] + "\" is not a concept, while \"" + self.__leftTerm + "\" is.\nIt can't be used to build the following axiom:\n" + str(result))
						
						self.__rightTerm = result[2][1]
						self.__rightTermExists = True
					
					elif isinstance(result[2][1], (ParseResults, tuple, list)) and \
						isinstance(result[2][1][0], str) and result[2][1][0] == syntax.inverse and \
						isinstance(result[2][1][1], str):
						#~ It's the term: exists P^-
						
						if not self.__checkRole(result[2][1][1], roleList):
							raise Exception("The term \"" + result[2][1][1] + "\" is not a valid role, it can't be used to build the following axiom:\n" + str(result))
						
						#~ If the first term is either P or P^-, then we raise an Exception
						if not self.__leftTermExists and self.__checkRole(self.__leftTerm, roleList):
							raise Exception("The term \"" + result[2][1][1] + "\" is not a concept, while \"" + self.__leftTerm + "\" is.\nIt can't be used to build the following axiom:\n" + str(result))
							
						self.__rightTerm = result[2][1][1]
						self.__rightTermExists = True
						self.__rightTermInverse = True
					
					else:
						#~ Something is wrong.
						raise Exception("The right term of the following axiom was not recognized as a valid one.\n" + str(result))
					
				elif isinstance(result[2][0], str) and result[2][0] == syntax.inverse and \
					isinstance(result[2][1], str):
					#~ It's the term: P^-
					
					if not self.__checkRole(result[2][1], roleList):
						raise Exception("The term \"" + result[2][1] + "\" is not a valid role, it can't be used to build the following axiom:\n" + str(result))
					
					#~ If the first term is either P or P^-, then we raise an Exception
					if not self.__leftTermExists and self.__checkRole(self.__leftTerm, roleList):
						raise Exception("The term \"" + result[2][1] + "\" is not a concept, while \"" + self.__leftTerm + "\" is.\nIt can't be used to build the following axiom:\n" + str(result))
						
					self.__rightTermTerm = result[2][1]
					self.__rightTermInverse = True
				
				elif isinstance(result[2][0], str) and result[2][0] == syntax.neg:
					#~ The axiom is a disjunction
					self.__disjoint = True
					
					if isinstance(result[2][1], str):
						#~ The second term is either an atomic concept A or atomic role P
						
						if not (self.__checkConcept(result[2][1], conceptList) or self.__checkRole(result[2][1], roleList)):
							raise Exception("The term \"" + result[2][1] + "\" is not valid, it can't be used to build the following axiom:\n" + str(result))
						
						if (self.__checkConcept(self.__leftTerm, conceptList) or \
							(self.__leftTermExists and self.__checkRole(self.__leftTerm, roleList))) and \
							not self.__checkConcept(result[2][1], conceptList):
							raise Exception("The term \"" + result[2][1] + "\" is not a concept, while \"" + self.__leftTerm + "\" is.\nIt can't be used to build the following axiom:\n" + str(result))
							
						if self.__checkRole(self.__leftTerm, roleList) and not self.__checkRole(result[2][1], roleList):
							raise Exception("The term \"" + result[2][1] + "\" is not a role, while \"" + self.__leftTerm + "\" is.\nIt can't be used to build the following axiom:\n" + str(result))
						
						self.__rightTerm = result[2][1]
						
					elif isinstance(result[2][1], (ParseResults, tuple, list)):
						
						if isinstance(result[2][1][0], str) and result[2][1][0] == syntax.exists:
						
							if isinstance(result[2][1][1], str):
								#~ It's the term: exists P
								
								if not self.__checkRole(result[2][1][1], roleList):
									raise Exception("The term \"" + result[2][1][1] + "\" is not a valid role, it can't be used to build the following axiom:\n" + str(result))
								
								#~ If the first term is either P or P^-, then we raise an Exception
								if not self.__leftTermExists and self.__checkRole(self.__leftTerm, roleList):
									raise Exception("The term \"" + result[2][1][1] + "\" is not a concept, while \"" + self.__leftTerm + "\" is.\nIt can't be used to build the following axiom:\n" + str(result))
								
								self.__rightTerm = result[2][1][1]
								self.__rightTermExists = True
							
							elif isinstance(result[2][1][1], (ParseResults, tuple, list)) and \
								isinstance(result[2][1][1][0], str) and result[2][1][1][0] == syntax.inverse and \
								isinstance(result[2][1][1][1], str):
								#~ It's the term: exists P^-
								
								if not self.__checkRole(result[2][1][1][1], roleList):
									raise Exception("The term \"" + result[2][1][1][1] + "\" is not a valid role, it can't be used to build the following axiom:\n" + str(result))
								
								#~ If the first term is either P or P^-, then we raise an Exception
								if not self.__leftTermExists and self.__checkRole(self.__leftTerm, roleList):
									raise Exception("The term \"" + result[2][1][1][1] + "\" is not a concept, while \"" + self.__leftTerm + "\" is.\nIt can't be used to build the following axiom:\n" + str(result))
								
								self.__rightTerm = result[2][1][1][1]
								self.__rightTermExists = True
								self.__rightTermInverse = True
							
							else:
								#~ Something is wrong.
								raise Exception("The right term of the following axiom was not recognized as a valid one.\n" + str(result))
							
						elif isinstance(result[2][1][0], str) and result[2][1][0] == syntax.inverse and \
							isinstance(result[2][1][1], str):
							#~ It's the term: P^-
							
							if not self.__checkRole(result[2][1][1], roleList):
								raise Exception("The term \"" + result[2][1][1] + "\" is not a valid role, it can't be used to build the following axiom:\n" + str(result))
							
							#~ If the first term is either P or P^-, then we raise an Exception
							if not self.__leftTermExists and self.__checkRole(self.__leftTerm, roleList):
								raise Exception("The term \"" + result[2][1][1] + "\" is not a concept, while \"" + self.__leftTerm + "\" is.\nIt can't be used to build the following axiom:\n" + str(result))
							
							self.__rightTermTerm = result[2][1][1]
							self.__rightTermInverse = True
						
						else:
							#~ Something is wrong.
							raise Exception("The right term of the following axiom was not recognized as a valid one.\n" + str(result))
					
					
				else:
					#~ Something is wrong.
					raise Exception("The right term of the following axiom was not recognized as a valid one.\n" + str(result))
			
			else:
				#~ Something is wrong.
				raise Exception("The right term of the following axiom was not recognized as a valid one.\n" + str(result))
		
		elif isinstance(result[0], str) and result[0] == syntax.funct:
			#~ It's a functionality axiom
			self.__functionality = True
			
			#~ Parse the first term
			if isinstance(result[1], str):
				#~ The first term is an atomic role P
				
				if not self.__checkRole(result[1], roleList):
					raise Exception("The term \"" + result[1] + "\" is not a valid role, it can't be used to build the following axiom:\n" + str(result))
				
				self.__leftTerm = result[1]
			
			elif isinstance(result[1], (ParseResults, tuple, list)) and \
				isinstance(result[1][0], str) and result[1][0] == syntax.inverse and \
				isinstance(result[1][1], str):
				#~ The first term is: P^-
				
				if not self.__checkRole(result[1][1], roleList):
					raise Exception("The term \"" + result[1][1] + "\" is not a valid role, it can't be used to build the following axiom:\n" + str(result))
				
				self.__leftTerm = result[1][1]
				self.__leftTermInverse = True
			
			else:
				#~ Something is wrong.
				raise Exception("The following functionality axiom was not recognized as a valid one.\n" + str(result))
				
		else:
			#~ Something is wrong.
			raise Exception("The axiom was not recognized as a valid one.\n" + str(result))

	def leftTerm(self):
		return self.__leftTerm
	
	def leftTermExists(self):
		return self.__leftTermExists
		
	def leftTermInverse(self):
		return self.__leftTermInverse
		
	def rightTerm(self):
		return self.__rightTerm
		
	def rightTermExists(self):
		return self.__rightTermExists
		
	def rightTermInverse(self):
		return self.__rightTermInverse
		
	def disjoint(self):
		return self.__disjoint
		
	def functionality(self):
		return self.__functionality
	
	def __repr__(self):
		axiomStr = ""
		
		if self.__functionality:
			if self.__leftTermInverse:
				axiomStr = "(funct (inverse " + self.__leftTerm + ") )"
			else:
				axiomStr = "(funct " + self.__leftTerm + ")"
		
		else:
			
			axiomStr = "(isA "
			
			if self.__leftTermExists and self.__leftTermInverse:
				axiomStr += "(exists (inverse " + self.__leftTerm + ") )"
			
			elif self.__leftTermExists:
				axiomStr += "(exists " + self.__leftTerm + ")"
			
			elif self.__leftTermInverse:
				axiomStr += "(inverse " + self.__leftTerm + ")"
			
			else:
				axiomStr += self.__leftTerm
			
			axiomStr += " "
			
			if self.__disjoint:
				axiomStr += "(not "
				
				if self.__rightTermExists and self.__rightTermInverse:
					axiomStr += "(exists (inverse " + self.__rightTerm + ") )"
				
				elif self.__rightTermExists:
					axiomStr += "(exists " + self.__rightTerm + ")"
				
				elif self.__rightTermInverse:
					axiomStr += "(inverse " + self.__rightTerm + ")"
				
				else:
					axiomStr += self.__rightTerm
				
				axiomStr += ")"
			
			else:
				
				if self.__rightTermExists and self.__rightTermInverse:
					axiomStr += "(exists (inverse " + self.__rightTerm + ") )"
				
				elif self.__rightTermExists:
					axiomStr += "(exists " + self.__rightTerm + ")"
				
				elif self.__rightTermInverse:
					axiomStr += "(inverse " + self.__rightTerm + ")"
				
				else:
					axiomStr += self.__rightTerm
			
			axiomStr += ")"
		
		return axiomStr
		
class Assertion:
	#~ Represent a membership assertion in a ABox
	#~ Possible type of assertions:
		#~ (concept val1)
		#~ (role val1 val2)
		
	def __init__(self, assertionToParse, conceptList, roleList, individualList):
		#~ The function __init__ takes as input:
			#~ - assertionToParse: the assertion that needs to be parsed.
			#~ - conceptList: a (possibly empty) list of concepts. It is used to validate the assertion.
			#~ - roleList: a (possibly empty) list of roles. It is used to validate the assertion.
			#~ - individualList: a (possibly empty) list of individuals. It is used to validate the assertion.
			
		self.__term = None
		self.__individual1 = None
		self.__individual2 = None
		
		#~ Check the input
		self.__checkInput(assertionToParse, conceptList, roleList, individualList)
		
		#~ Parse the input
		self.__parseAssertion(assertionToParse, conceptList, roleList, individualList)
		
		
	
	def __checkInput(self, assertionToParse, conceptList, roleList, individualList):
		
		if not isinstance(assertionToParse, (str, ParseResults, tuple, list)):
			#~ Formato non valido
			raise Exception("The provided assertion is not in a valid format: " + str(type(assertionToParse)) + "\n" + str(assertionToParse))
		
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
		
	def __checkConcept(self, term, conceptList):
		#~ Checks if term is a valid concept.
		#~ term must not be a reserved keyword,
		#~ and must be in conceptList
		#~ Returns True if it is valid, False otherwise
		
		if not isinstance(term, str):
			raise Exception("The term passed to the function __checkConcept must be a string: " + str(type(term)))
		
		syntax = Syntax()
		
		#~ The term can't be a reserved keyword
		if term in syntax.keywords:
			return False
			
		if not term in conceptList:
			return False
		
		return True
	
	def __checkRole(self, term, roleList):
		#~ Checks if term is a valid role.
		#~ term must not be a reserved keyword,
		#~ and must be in roleList
		#~ Returns True if it is valid, False otherwise
		
		if not isinstance(term, str):
			raise Exception("The term passed to the function __checkRole must be a string: " + str(type(term)))
		
		syntax = Syntax()
		
		#~ The term can't be a reserved keyword
		if term in syntax.keywords:
			return False
			
		if not term in roleList:
			return False
		
		return True
	
	def __checkIndividual(self, term, individualList):
		#~ Checks if term is a valid individual.
		#~ term must not be a reserved keyword,
		#~ and must be in individualList
		#~ Returns True if it is valid, False otherwise
		
		if not isinstance(term, str):
			raise Exception("The term passed to the function __checkIndividual must be a string: " + str(type(term)))
		
		syntax = Syntax()
		
		#~ The term can't be a reserved keyword
		if term in syntax.keywords:
			return False
			
		if not term in individualList:
			return False
		
		return True
	
	def __parseAssertion(self, assertionToParse, conceptList, roleList, individualList):
		syntax = Syntax()
		
		#~ If assertionToParse is a string, we parse it by considering the parenthesis that close every expression
		#~ and analyse the resulting pyparsing.ParseResults.
		#~ If axiomToParse is already a pyparsing.ParseResults (or a list, or a tuple), then we analise it directly.
		if isinstance(assertionToParse, str):
			raise Exception("Sorry, at the moment we can't parse assertions that are passed as a string.\n" + assertionToParse)
		
		#~ If assertionToParse is either a ParseResults, tuple, or list, then it must have
		#~ 2 or 3 elements, and all of them must be strings.
		#~ Also, if it has 2 elements, then the first element must be in conceptList (if specified),
		#~ while if it has 3 elements, it must be in roleList (if specified)
		if len(assertionToParse) < 2 or len(assertionToParse) > 3:
			raise Exception("An assertion must be formed of 2 elements (in case of an assertion involving a concept), or 3 (in case of a role).\n" + \
					"The following assertion has instead " + str(len(assertionToParse)) + " elements:\n" + \
					str(assertionToParse))
		
		if not all(isinstance(element, str) for element in assertionToParse):
			raise Exception("The element composing an assertion to parse must be all strings.\n" + str(assertionToParse))
		
		if len(assertionToParse) == 2:
			if not self.__checkConcept(assertionToParse[0], conceptList):
				raise Exception("The term used in the assertion is not a valid concept.\n" + str(assertionToParse))
			
			if not self.__checkIndividual(assertionToParse[1], individualList):
				raise Exception("The individual used in the assertionis not a individual.\n" + str(assertionToParse))
			
			#~ Save the elements
			self.__term = assertionToParse[0]
			self.__individual1 = assertionToParse[1]
		
		elif len(assertionToParse) == 3:
			if not self.__checkRole(assertionToParse[0], roleList):
				raise Exception("The term used in the assertion is not a valid concept.\n" + str(assertionToParse))
			
			if not self.__checkIndividual(assertionToParse[1], individualList):
				raise Exception("The individual used in the assertionis not a individual.\n" + str(assertionToParse))
			
			if not self.__checkIndividual(assertionToParse[2], individualList):
				raise Exception("The individual used in the assertionis not a individual.\n" + str(assertionToParse))
			
			#~ Save the elements
			self.__term = assertionToParse[0]
			self.__individual1 = assertionToParse[1]
			self.__individual2 = assertionToParse[2]
		
		else:
				#~ Something is wrong.
				raise Exception("Something went wrong with the analisys of the following assertion.\n" + str(assertionToParse))
			
	def term(self):
		return self.__term
		
	def individual1(self):
		return self.__individual1
		
	def individual2(self):
		return self.__individual2
	
	def __eq__(self, other):
		
		if not isinstance(other, Assertion):
			return False
		
		if other.term() != self.__term:
			return False
		
		if other.individual1() != self.__individual1:
			return False
		
		if other.individual2() != self.__individual2:
			return False
		
		return True
		
	def __ne__(self, other):
		
		return not self.__eq__(other)
	
	def __hash__(self):
		
		if self.__individual2 is None:
			return hash(str(type(self)) + self.__term + self.__individual1)
		else:
			return hash(str(type(self)) + self.__term + self.__individual1 + self.__individual2)
		
	def __repr__(self):
		return self.toADL()
	
	def toADL(self, indentLevel = 0):
		
		if not isinstance(indentLevel, int) or indentLevel < 0:
			raise Exception("The parameter indentLevel must be a positive integer.")
		
		def __indent(indentLevel):
			syntax = Syntax()
			
			return syntax.indent*indentLevel
		
		assertionString =  __indent(indentLevel) + "(" + str(self.__term) + " " + str(self.__individual1)
		
		if not self.__individual2 is None:
			assertionString += " " + str(self.__individual2)
			
		assertionString += ")\n"
		
		return assertionString
		
