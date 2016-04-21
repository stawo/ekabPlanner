from pyparsing import *
from itertools import *
import os

#~ Local libraries
from syntax.syntax import Syntax
from ekab.tbox import *
from queries.cq import *
from queries.ucq import UCQ
from queries.ecq import ECQ
from queries.rewrite import rewrite

		
class EKab:
	
	#~ A EKab object represents an EKab planning problem and its constituents.
	#~ An eKab is a tuple <C,C_0,T,A_0,act,rul>, where:
		#~ - C is the (infinite) object domain
		#~ - C_0 is a finite subset of C
		#~ - T is a DL-Lite TBox
		#~ - A_0 is a DL-Lite ABox
		#~ - act is a set of parametric actions
		#~ - rul is a set of condition-action actions
	#~ The planning problem is represented by a tuple <K,G>, where K in an eKab, and G a boolean ECQ.
	#~ 
	#~ A EKab object contains the following elements (and we show also their initial value):
		#~ - self.__concepts = set()
			#~ Represents the set of atomic concepts used in the TBox T.
			#~ Each atomic concept is saved as a string.
		#~ - self.__conceptsParse = NoMatch() 
			#~ Used when parsing, it's the conjuction of all atomic concepts,
			#~ i.e. Literal(concept name) + ... + Literal(concept name)
		#~ - self.__roles = set()
			#~ Represent the set of atomic roles used in the TBox T.
			#~ Each atomic role is saved as a string.
		#~ - self.__rolesParse = NoMatch()
			#~ Used when parsing, it's the conjuction of all atomic roles,
			#~ i.e. Literal(role name) + ... + Literal(role name)
		#~ - self.__axiomsPos = set()
			#~ The set of positive axioms of the TBox T.
			#~ Positive axioms are the one like:
			#~ basicConcept isA genericConcept, basicRole isA genericConcept
			#~ Each axiom is saved as a tuple where the first element represents
			#~ the left argument, and the second the right argument.
		#~ - self.__axiomsNeg = set()
			#~ The set of negative axioms of the TBox T.
			#~ Negative axioms are the one like:
			#~ basicConcept isA not genericConcept, basicRole isA not genericConcept
			#~ Each axiom is saved as a tuple where the first element represents
			#~ the left argument, and the second the right argument.
			#~ We don't need to save the "not".
		#~ - self.__axiomsFunct = set()
			#~ The set of functional axioms of the TBox T.
			#~ Functional axioms are the one like:
			#~ (funct basicRole)
			#~ For each axiom is saved only the basicRole, which is either a string (i.e., an atomic role)
			#~ or a tuple (i.e. inverse of an atomic role).
			#~ We don't need to save the "funct".
		#~ - self.__rules = set()
			#~ The set of condition-action rules.
			#~ Each rule is a tuple "(ruleName, ruleCond, ruleAction)", where:
				#~ - ruleName is a string of the name of the rule;
				#~ - ruleCond is an ECQ() representing the condition;
				#~ - ruleAction is a string of the called action.
		#~ - self.__actions = set()
			#~ The set of actions.
			#~ Each action is a tuple "(actionName, actionParam, actionEffects)" where:
				#~ - actionName is a string of the name of the action;
				#~ - actionParam is a tuple of strings of the parameteres of the action;
				#~ - actionEffects is a tuple of conditional effects.
			#~ Each conditional effect is a tuple "(effectCond, effectAdd, effectDel)", where:
				#~ - effectCond is an ECQ() representing the effect's condition;
				#~ - effectAdd is a tuple of QueryAtom() that represents the atoms that will be added;
				#~ - effectDel is a tuple of QueryAtom() that represents the atoms that will be deleted;
		#~ - self.__queryUnsat = None
			#~ Represents the query to check the satisfiability of the KB <T,A>
			#~ It is an UCQ with inequalities, thus an object from UCQ(queryToParse, inequalitiesAllowed = True)
		#~ - self.__rulesRewritten = set()
			#~ It is the set of condition-action rules from self.__rules, where ruleCond has been rewritten
			#~ in order to compile away the need of the TBox T
		#~ - self.__actionsRewritten = set()
			#~ It is the set of actions from self.__actions, where effectCond has been rewritten
			#~ in order to compile away the need of the TBox T
		#~ - self.__queryUnsatRewritten = None
			#~ It is the rewritten version of __queryUnsat,
			#~ in order to compile away the need of the TBox T
	#~ 
	#~ As we adopt the PDDL syntax to represent the problem, there are two files:
		#~ the planning domain
		#~ the planning problem
	#~ The planning domain contains:
		#~ - the planning domain name
		#~ - the TBox T
		#~ - the actions
		#~ - the condition-action rules
	#~ while the planning problem contains:
		#~ - the initial state, represented by A_0
		#~ - the goal formula G
	
	
	def __init__(self, planningDomainFile, planningProblemFile = None):
		
		self.__domainName = None
		self.__problemName = None
		
		self.__concepts = set()
		self.__conceptsParse = NoMatch() #Used when parsing, it's the list of all atomic concepts
		self.__roles = set()
		self.__rolesParse = NoMatch() #Used when parsing, it's the list of all atomic roles
		self.__axiomsPos = set()
		self.__axiomsNeg = set()
		self.__axiomsFunct = set()
		self.__rules = set()
		self.__actions = set()
		self.__queryUnsat = None
		self.__individuals = set()
		self.__assertions = set()
		self.__goalQuery = None
		
		self.__rulesRewritten = set()
		self.__actionsRewritten = set()
		self.__queryUnsatRewritten = None
		self.__goalQueryRewritten = None
		
		#~ Check if planningDomainFile is a proper file path
		if not isinstance(planningDomainFile, str) or not os.path.isfile(planningDomainFile):
			raise Exception("The provided file path for the planning domain is not valid!\n" + str(planningDomainFile))
		
		#~ Check if planningProblemFile is a proper file path
		if not isinstance(planningProblemFile, str) or not os.path.isfile(planningProblemFile):
			raise Exception("The provided file path for the planning problem is not valid!\n" + str(planningProblemFile))
		
		#~ Parse the planning domain and planning problem
		#~ The parsing is divided in parts:
		#~ - parse the domain file, in order to retrieve the domain name and check that
		#~ - the requirements and the predicates are ok. If not, raise an exception.
		#~ 		From the predicates we create the list of concepts and roles;
		#~ - parse the problem file, in order to retrieve the individuals, the ABox assertions, and the goal;
		#~ - parse the domain file again to retrieve the axioms, the condition-action rules, and the actions.
		
		self.__parseNameRequirementsPredicates(planningDomainFile)
		self.__parseProblem(planningProblemFile)
		self.__parseAxiomsRulesActions(planningDomainFile)
		
		#~ Calculate queryUnsat
		self.__calculateQueryUnsat()
		
		#~ Compile the TBox away
		self.__compileTBoxAway()
		
	def __parseNameRequirementsPredicates(self, planningDomainFile):
		#~ Predicates are defined in the usual PDDL way:
		#~ (:predicates
			#~ (C ?x)
			#~ (P ?x ?y)
			#~ ...
		#~ )
		
		syntax = Syntax()
		
		#~ A concept is composed by a name and only one variable, e.g. C ?x
		#~ We remove the variable and replace it with the keyword "Concept"
		pddlConcept =  Group(syntax.allowed_word.setResultsName("predicateName") + syntax.variable.setParseAction(replaceWith("Concept")).setResultsName("predicateType"))
		#~ A role is composed by a name and exactly two variables, e.g. P ?x ?y
		#~ We remove the first variable and replace it with the keyword "Role"
		#~ while we remove completely the second
		pddlRole = Group(syntax.allowed_word.setResultsName("predicateName") + \
					syntax.variable.setParseAction(replaceWith('Role')).setResultsName("predicateType")  + \
					syntax.variable.setParseAction().suppress() ) 
		#~ We put pddlVariable.setParseAction() in order to remove the effect of the previous pddlVariable.setParseAction(replaceWith('Role'))
		#~ If we fail to do so, then all the times we use self.variable, it will be substituted by the word "Role"
		
		#~ A PDDL Predicate is either concepts or roles
		pddlPredicate = pddlConcept ^ pddlRole
		pddlPredicates = syntax.leftPar + syntax.pddlPredicatesTag.suppress() + Group(OneOrMore(syntax.leftPar + pddlPredicate + syntax.rightPar)).setResultsName("predicates") + syntax.rightPar
		
		
		pddlDomain = StringStart() + \
					syntax.leftPar + syntax.pddlDefineTag + \
					syntax.leftPar + syntax.pddlDomainTag + \
					syntax.pddlDomainName.setResultsName("domainName") + \
					syntax.rightPar + \
					syntax.pddlRequirements.suppress() + \
					pddlPredicates + \
					Regex("(.*\r*\n*)*\)\r*\n*").suppress()
		
		#~ Parse the file
		result = pddlDomain.parseFile(planningDomainFile)
		
		self.__domainName = result["domainName"] #Save the domain name
		
		#~ Save the concepts and roles
		for predicate in result["predicates"]:
			
			#~ If a predicate has the same name as a keyword (e.g., "exists", "not", etc.), raise an Exception
			if str(predicate["predicateName"]) in syntax.keywords:
				raise Exception("It is not possible to use the word \"" + str(predicate["predicateName"]) + "\" as a name for a predicate, as it is a keyword.")
				
			if predicate["predicateType"][0] == "Concept":
				self.__concepts.add(str(predicate["predicateName"]))
				self.__conceptsParse = self.__conceptsParse ^ Literal(str(predicate["predicateName"]))
			else:
				self.__roles.add(str(predicate["predicateName"]))
				self.__rolesParse = self.__rolesParse ^ Literal(str(predicate["predicateName"]))
		
	def __parseAxiomsRulesActions(self, planningDomainFile):
		#~ The functions parse the following elements:
			#~ - axioms
			#~ - condition-action rules
			#~ - actions
		
		#~ The possible axioms, as defined in DL-Lite, are (here written in PDDL-EKab syntax):
			#~ (isA pddlBasicRole pddlGeneralRole)
			#~ (isA pddlBasicConcept pddlGeneralConcept)
			#~ (funct pddlBasicRole)
		#~ The possible terms participating in axioms are, instead:
			#~ pddlAtomicRole := nome del ruolo definito in predicates
			#~ pddlBasicRole := pddlAtomicRole | (inverse pddlAtomicRole)
			#~ pddlGeneralRole := pddlBasicRole | (not pddlBasicRole)
			#~ pddlAtomicRole := nome del concetto definito in predicates
			#~ pddlBasicConcept := pddlAtomicRole | (exists pddlBasicRole)
			#~ pddlGeneralConcept := pddlBasicConcept | (not pddlBasicConcept) | (existsQualified pddlBasicRole pddlBasicConcept) | topC
		#~ 
		#~ The parser divides immediately the axioms in: positive axioms, negative axioms, and functionality axioms
		
		syntax = Syntax()
		
		pddlAtomicRole = self.__rolesParse
		pddlAtomicConcept = self.__conceptsParse
		
		pddlBasicRole = pddlAtomicRole ^ Group((syntax.leftPar + Literal(syntax.inverse) + pddlAtomicRole + syntax.rightPar))
		pddlBasicConcept = pddlAtomicConcept ^ Group((syntax.leftPar + Literal(syntax.exists) +  pddlBasicRole + syntax.rightPar))
		
		pddlGeneralConcept = syntax.topC ^ \
					Group((syntax.leftPar + Literal(syntax.existsQualified) + pddlBasicConcept + pddlBasicRole + syntax.rightPar)) ^ \
					pddlBasicConcept
		#~ pddlGeneralRole = Group((self.leftPar + "not" + pddlBasicRole + self.rightPar)) ^ \
		#~			pddlBasicRole
		
		pddlAxiomPos = Group(\
					Empty().setParseAction(replaceWith("AxiomPos")) + \
					Group(((syntax.isA + pddlBasicConcept + pddlGeneralConcept) ^ (syntax.isA + pddlBasicRole + pddlBasicRole))) \
					)
		pddlAxiomNeg = Group( \
					Empty().setParseAction(replaceWith("AxiomNeg")) + \
					Group(((syntax.isA + pddlBasicConcept + syntax.leftPar + Literal(syntax.neg).suppress() +  pddlBasicConcept + syntax.rightPar) ^ \
					(syntax.isA + pddlBasicRole + syntax.leftPar + Literal(syntax.neg).suppress() + pddlBasicRole + syntax.rightPar)) \
					))
		pddlAxiomFunct = Group(Empty().setParseAction(replaceWith("AxiomFunct")) + Literal(syntax.funct).suppress() + pddlBasicRole)
		
		#~ pddlAxioms = syntax.leftPar + syntax.pddlAxiomsTag + \
				#~ Group(OneOrMore(syntax.leftPar + (pddlAxiomPos ^ pddlAxiomNeg ^ pddlAxiomFunct) + syntax.rightPar)).setResultsName("axioms") + syntax.rightPar
		
		pddlAxioms = syntax.leftPar + syntax.pddlAxiomsTag + \
				Group(OneOrMore(nestedExpr())).setResultsName("axioms") + syntax.rightPar
		
		#~ A condition-action rule has the form of:
			#~ ECQ -> action name
		#~ This, in the PDDL-EKab sytax is expressed as:
			#~ (:rule rule-name
				#~ :condition ECQ
				#~ :action action-name
			#~ )
		pddlRuleName = syntax.allowed_word.setResultsName("ruleName") # Rule name
		pddlRuleCondition = syntax.pddlRuleConditionTag + nestedExpr().setResultsName("ruleCondition")
		pddlRuleAction = syntax.pddlRuleActionTag + syntax.allowed_word.setResultsName("ruleAction")
		pddlRule = Group(syntax.leftPar + syntax.pddlRuleTag + pddlRuleName + pddlRuleCondition + pddlRuleAction + syntax.rightPar)
		pddlRules = Group(ZeroOrMore(pddlRule)).setResultsName("rules")
		
		#~ An action has the form of:
			#~ name (input parameters): { list of effects }
		#~ Each effect has the form:
			#~ ECQ ~> add F+, del F-
		#~ where F+ and F- are a set of atomic effects.
		#~ This, in the PDDL-EKab sytax is expressed as:
			#~ (:action action-name
				#~ :parameters ( list of variables )
				#~ :effects (
					#~ :condition ECQ
					#~ :add (atoms list)
					#~ :remove (atoms list)
					#~ )
					#~ ...
					#~ (
					#~ :condition ECQ
					#~ :add (atoms list)
					#~ :delete (atoms list)
					#~ )
			#~ )
		pddlActionName = syntax.allowed_word.setResultsName("actionName")
		pddlActionParameters = Literal(":parameters").suppress() + syntax.leftPar + Group(ZeroOrMore(syntax.variable)).setResultsName("actionParameters") + syntax.rightPar
		
		pddlActionEffectCondition = syntax.pddlActionEffectConditionTag + nestedExpr().setResultsName("effectCondition")
		pddlActionEffectAdd = syntax.pddlActionEffectAddTag + nestedExpr().setResultsName("effectAdd")
		pddlActionEffectDel = syntax.pddlActionEffectDelTag + nestedExpr().setResultsName("effectDelete")
		pddlActionEffect = Group(syntax.leftPar + pddlActionEffectCondition + pddlActionEffectAdd + syntax.rightPar) ^ \
							Group(syntax.leftPar + pddlActionEffectCondition + pddlActionEffectDel + syntax.rightPar) ^ \
							Group(syntax.leftPar + pddlActionEffectCondition + pddlActionEffectAdd + pddlActionEffectDel + syntax.rightPar)
		pddlActionEffects = syntax.pddlActionEffectsTag + Group(OneOrMore(pddlActionEffect)).setResultsName("actionEffects")
		
		pddlAction = Group(syntax.leftPar + syntax.pddlActionTag + pddlActionName + pddlActionParameters + pddlActionEffects + syntax.rightPar)

		pddlActions = Group(ZeroOrMore(pddlAction)).setResultsName("actions")
		
		#~ The section (:predicates ...) is matched by the Regex expression:
		#~ Regex("\(\s*\:predicates\s*\r*\n*(\s*\(.*\)\s*\r*\n*)*\s*\)").suppress()
		pddlDomain = StringStart() + \
					syntax.leftPar + syntax.pddlDefineTag + \
					syntax.leftPar + syntax.pddlDomainTag + \
					Literal(self.__domainName).suppress() + syntax.rightPar + \
					syntax.pddlRequirements.suppress() + \
					Regex("\(\s*\:predicates\s*\r*\n*(\s*\(.*\)\s*\r*\n*)*\s*\)").suppress() + \
					pddlAxioms + \
					pddlRules + \
					pddlActions + \
					syntax.rightPar + \
					StringEnd()
		
		#~ Parse the file
		try:
			result = pddlDomain.parseFile(planningDomainFile)
		except ParseException as x:
			print ("Line {e.lineno}, column {e.col}:\n'{e.line}'".format(e=x))
			raise
			
		#~ 
		#~ Analyse the axioms
		#~ 
		for axiomParse in result["axioms"]:
			
			axiom = Axiom(axiomParse, self.__concepts, self.__roles)
			
			if axiom.disjoint():
				self.__axiomsNeg.add(axiom)
			elif axiom.functionality():
				self.__axiomsFunct.add(axiom)
			else:
				self.__axiomsPos.add(axiom)
		
		#~ 
		#~ Analyse the rules
		#~ 
		for rule in result["rules"]:
			
			#~ Check that no other action has the same name
			for otherRule in result["rules"]:
				if rule != otherRule and str(rule["ruleName"]) == str(otherRule["ruleName"]):
					raise Exception("There are two rule with the same name: " + str(rule["ruleName"]))
			
			#~ Create the ECQ
			ruleCond = ECQ(rule["ruleCondition"][0], self.__concepts, self.__roles, self.__individuals)
			
			#~ We need to check that the terms used in the rules are present in the
			#~ TBox vocabulary (thus, in the predicate section)
			if not ruleCond.concepts().issubset(self.__concepts):
				raise Exception("The following rule is using terms that are not concepts in the predicates: (:" + str(rule["ruleName"]) + " ... )\n" \
				"Terms that are not concepts: " + str(ruleCond.concepts().difference(self.__concepts)))
			if not ruleCond.roles().issubset(self.__roles):
				raise Exception("The following rule is using terms that are not roles in the predicates: (:" + str(rule["ruleName"]) + " ... )\n" \
				"Terms that are not roles: " + str(ruleCond.roles().difference(self.__roles)))
			
			#~ Check that the action called exists
			found = False
			for action in result["actions"]:
				if str(rule["ruleAction"]) == str(action["actionName"]):
					found = True
			
			if not found:
				raise Exception("The rule (:" + str(rule["ruleName"]) + " ... ) is calling an action ("+ str(rule["ruleAction"]) + " ... ) that is not specified after.")
				
			#~ Save the rule
			self.__rules.add((str(rule["ruleName"]), ruleCond, str(rule["ruleAction"])))
		
		#~ 
		#~ Analyse the actions
		#~ 
		for action in result["actions"]:
			
			#~ Check that no other action has the same name
			for otherAction in result["actions"]:
				if action != otherAction and str(action["actionName"]) == str(otherAction["actionName"]):
					raise Exception("There are two actions with the same name: " + str(action["actionName"]))
			
			#~ Save the parameters in a tuple
			actionParameters = tuple([Variable(parameter) for parameter in action["actionParameters"]])
			
			#~ Every action can be called only by one rule, and
			#~ the free variables of the rule condition must be a subset of
			#~ the parameters of the action.
			counter = 0
			for rule in self.__rules:
				if str(action["actionName"]) == rule[2]:
					#~ Increase the counter
					counter += 1
					
					#~ Check the free variables
					if not rule[1].freeVars().issubset(actionParameters):
						raise Exception("The rule " + rule[0] + " calls the action " + str(action["actionName"]) + \
						", but the free variables of its condition (" + str(rule[1].freeVars()) + \
						") are not a subset of the parameters of the action (" + str(actionParameters) + ").")
			
			#~ Check that only one rule calls the action
			if counter != 1:
				raise Exception("There are " + str(counter) + " rules that call the action " + str(action["actionName"]) +". There must be 1!")
			
			#~ Analyze each effect
			effects = [] # Temporary list for the effects
			for effect in action["actionEffects"]:
				
				#~ Create the ECQ of the effect
				effectCond = ECQ(effect["effectCondition"][0], self.__concepts, self.__roles, self.__individuals)
				
				#~ We need to check that the terms used in the effect condition are present in the
				#~ TBox vocabulary (thus, in the predicate section)
				if not effectCond.concepts().issubset(self.__concepts):
					raise Exception("The following action is using terms that are not concepts in the predicates: (:" + str(action["actionName"]) + " ... )\n" \
					"Terms that are not concepts: " + str(effectCond.concepts().difference(self.__concepts)))
				if not effectCond.roles().issubset(self.__roles):
					raise Exception("The following action is using terms that are not roles in the predicates: (:" + str(action["actionName"]) + " ... )\n" \
					"Terms that are not roles: " + str(effectCond.roles().difference(self.__roles)))
				
				effectConcepts = set() #Set used to save the concepts that appear in the effects, for check purposes
				effectRoles = set() #Set used to save the roles that appear in the effects, for check purposes
				effectVars = set() #Set used to save the variables that appear in the effects, for check purposes
				
				effectAdd = [] # Temporary list for the addition effects
				if "effectAdd" in effect.keys():
					for atomicEffect in effect["effectAdd"][0]:
						
						atom = QueryAtom(atomicEffect, self.__concepts, self.__roles, self.__individuals)
						
						if atom.atomType() == "role":
							effectRoles.add(atom.term())
							
							if isinstance(atom.var1(), Variable):
								effectVars.add(atom.var1())
							if isinstance(atom.var2(), Variable):
								effectVars.add(atom.var2())
						elif atom.atomType() == "concept":
							effectConcepts.add(atom.term())
							
							if isinstance(atom.var1(), Variable):
								effectVars.add(atom.var1())
						else:
							raise Exception("An atomic effect can be only about a concept or a role. The following atom is not valid: " + str(atom))
								
						effectAdd.append(atom) # Add the effect to the list
				
				effectDel = [] # Temporary list for the deletion effects
				if "effectDelete" in effect.keys():
					for atomicEffect in effect["effectDelete"][0]:
						
						atom = QueryAtom(atomicEffect, self.__concepts, self.__roles, self.__individuals)
						
						if atom.atomType() == "role":
							effectRoles.add(atom.term())
							
							if isinstance(atom.var1(), Variable):
								effectVars.add(atom.var1())
							if isinstance(atom.var2(), Variable):
								effectVars.add(atom.var2())
						elif atom.atomType() == "concept":
							effectConcepts.add(atom.term())
							
							if isinstance(atom.var1(), Variable):
								effectVars.add(atom.var1())
						else:
							raise Exception("An atomic effect can be only about a concept or a role. The following atom is not valid: " + str(atom))
						
						effectDel.append(atom) # Add the effect to the list
				
				#~ We need to check that the terms used in the atomic effects are present in the
				#~ TBox vocabulary (thus, in the predicate section)
				if not effectConcepts.issubset(self.__concepts):
					raise Exception("The following action is using terms that are not concepts in the predicates: (:" + str(action["actionName"]) + " ... )\n" \
					"Terms that are not concepts: " + str(effectConcepts.difference(self.__concepts)))
				if not effectRoles.issubset(self.__roles):
					raise Exception("The following action is using terms that are not roles in the predicates: (:" + str(action["actionName"]) + " ... )\n" \
					"Terms that are not roles: " + str(effectRoles.difference(self.__roles)))
				
				#~ We need to check that the variables used in the atomic effects are present either 
				#~ in the ECQ of the effect, or in the parameters of the action.
				if not effectVars.issubset(effectCond.freeVars().union(actionParameters)):
					raise Exception("The following action is using variables in the atomic effects that do not appear among the free variables of the effect's condition: (:" + str(action["actionName"]) + " ... )\n" \
					"Variables that do not appear in the condition: " + str(effectVars.difference(effectCond.freeVars())))
				
				#~ Save the analyzed effect as a tuple
				effects.append(tuple((effectCond,tuple(effectAdd),tuple(effectDel))))
			
			#~ Save the action
			self.__actions.add( tuple((str(action["actionName"]),actionParameters,tuple(effects))) )
		
	def __calculateQueryUnsat(self):
		#~ Function that calculates the unsatisfiability query for the given DL KB,
		#~ which is an UCQ with inequalities
		queryUnsat = ""
		
		counter = 0 #counter used for the generation of unique variables
		
		for negAxiom in self.__axiomsNeg:
			
			#~ Each axioms is composed of two elements, the left one and the right one.
			#~ An element could be:
				#~ - A , saved as the string 'A' and has to be in self.__concepts
				#~ - \exists P , saved as the tuple ('exists','P')
				#~ - \exists P^- , saved as the tuple ('exists', ('inverse','P'))
				#~ - P , saved as the string 'P' and has to be in self.__roles
				#~ - P^- , saved as the tuple ('inverse','P')
			#~ Thus the possible negative axioms are:
				#~ - A is not A
				#~ - A is not \exists P
				#~ - A is not \exists P^-
				#~ - \exists P is not A
				#~ - \exists P^- is not A
				#~ - \exists P1 is not \exists P2
				#~ - \exists P1^- is not \exists P2
				#~ - \exists P1 is not \exists P2^-
				#~ - \exists P1^- is not \exists P2?-
				#~ - P1 is not P2
				#~ - P1^- is not P2
				#~ - P1 is not P2^-
				#~ - P1^- is not P2^-
			
			#~ The following "if" is dedicated to tind the following axioms:
			#~ - A is not A
			#~ - A is not \exists P
			#~ - A is not \exists P^-
			if negAxiom.leftTerm() in self.__concepts:
				
				if negAxiom.rightTerm() in self.__concepts:
					#~ - A is not A
					#~ We have to add to queryUnsat the subquery:
					#~ \exists x_counter. (elementLeft(x_counter) and elementRight(x_counter)]
					#~ which, written in a PDDL-EKab format, will be:
					#~ (exists (?x_counter) (and (elementLeft ?x_counter) (elementRight ?x_counter))
					queryUnsat += "(exists (?x_"+str(counter)+") (and ("+ negAxiom.leftTerm() +" ?x_"+str(counter)+ \
									") ("+negAxiom.rightTerm()+" ?x_"+str(counter)+") ))\n"
				
				elif negAxiom.rightTermExists and negAxiom.rightTerm() in self.__roles:
					
					if not negAxiom.rightTermInverse():
						#~ - A is not \exists P
						#~ We have to add to queryUnsat the subquery:
						#~ \exists x_counter, y_2. (elementLeft(x_counter) and elementRight[1](x_counter, y_2)]
						#~ which, written in a PDDL-EKab format, will be:
						#~ (exists (?x_counter ?y_2) (and (elementLeft ?x_counter) (elementRight[1] ?x_counter ?y_2))
						queryUnsat += "(exists (?x_"+str(counter)+" ?y_2) (and ("+negAxiom.leftTerm()+" ?x_"+str(counter)+ \
									") ("+negAxiom.rightTerm()+" ?x_"+str(counter)+" ?y_2) ))\n"
						
					elif negAxiom.rightTermInverse():
						#~ - A is not \exists P^-
						#~ We have to add to queryUnsat the subquery:
						#~ \exists x_counter,?y_2. (elementLeft(x_counter) and elementRight[1][1](?y_2, x_counter)]
						#~ which, written in a PDDL-EKab format, will be:
						#~ (exists (?x_counter ?y_2) (and (elementLeft ?x_counter) (elementRight[1][1] ?y_2 ?x_counter))
						queryUnsat += "(exists (?x_"+str(counter)+" ?y_2) (and ("+negAxiom.leftTerm()+" ?x_"+str(counter)+ \
									") ("+negAxiom.rightTerm()+" ?y_2 ?x_"+str(counter)+") ))\n"
						
					else:
						raise Exception("Something went wrong during the building of query_unsat. The following element couldn't be recognized: " + \
									str(negAxiom.rightTerm()) )
				else:
					raise Exception("Something went wrong during the building of query_unsat. The following element couldn't be recognized: " + \
								str(negAxiom.rightTerm()) )
				
			
			#~ The following "if" is dedicated to tind the following axioms:
			#~ - \exists P is not A
			#~ - \exists P1 is not \exists P2
			#~ - \exists P1 is not \exists P2^-
			elif negAxiom.leftTermExists() and negAxiom.leftTerm() in self.__roles:
				
				if negAxiom.rightTerm() in self.__concepts:
					#~ - \exists P is not A
					#~ We have to add to queryUnsat the subquery:
					#~ \exists x_counter, y_1. (elementLeft[1](x_counter, y_1) and elementRight(x_counter)]
					#~ which, written in a PDDL-EKab format, will be:
					#~ (exists (?x_counter ?y_1) (and (elementLeft[1] ?x_counter ?y_1) (elementRight ?x_counter))
					queryUnsat += "(exists (?x_"+str(counter)+" ?y_1) (and ("+ negAxiom.leftTerm() +" ?x_"+str(counter)+ \
								" ?y_1) ("+ negAxiom.rightTerm() +" ?x_"+str(counter)+") ))\n"
				
				elif negAxiom.rightTermExists() and negAxiom.rightTerm() in self.__roles:
					
					if not negAxiom.rightTermInverse():
						#~ - \exists P1 is not \exists P2
						#~ We have to add to queryUnsat the subquery:
						#~ \exists x_counter, y_1, y_2. (elementLeft[1](x_counter, y_1) and elementRight[1](x_counter, y_2)]
						#~ which, written in a PDDL-EKab format, will be:
						#~ (exists (?x_counter ?y_1 ?y_2) (and (elementLeft[1] ?x_counter ?y_1) (elementRight[1] ?x_counter ?y_2))
						queryUnsat += "(exists (?x_"+str(counter)+" ?y_1 ?y_2) (and ("+ negAxiom.leftTerm() +" ?x_"+str(counter)+ \
									" ?y_1) ("+ negAxiom.rightTerm() +" ?x_"+str(counter)+" ?y_2) ))\n"
						
					elif negAxiom.rightTermInverse():
						#~ - \exists P1 is not \exists P2^-
						#~ We have to add to queryUnsat the subquery:
						#~ \exists x_counter,y_1,y_2. (elementLeft[1](x_counter y_1) and elementRight[1][1](?y_2, x_counter)]
						#~ which, written in a PDDL-EKab format, will be:
						#~ (exists (?x_counter ?y_1 ?y_2) (and (elementLeft[1] ?x_counter ?y_1) (elementRight[1][1] ?y_2 ?x_counter))
						queryUnsat += "(exists (?x_"+str(counter)+" ?y_1 ?y_2) (and ("+ negAxiom.leftTerm() + \
									" ?x_"+str(counter)+" ?y_1) ("+ negAxiom.rightTerm() +" ?y_2 ?x_"+str(counter)+") ))\n"
						
					else:
						raise Exception("Something went wrong during the building of query_unsat. The following element couldn't be recognized: " + str(negAxiom.rightTerm()) )
				else:
					raise Exception("Something went wrong during the building of query_unsat. The following element couldn't be recognized: " + str(negAxiom.rightTerm()) )
				
				
			#~ The following "if" is dedicated to tind the following axioms:
			#~ - \exists P^- is not A
			#~ - \exists P1^- is not \exists P2
			#~ - \exists P1^- is not \exists P2?-
			elif negAxiom.leftTermExists() and \
				negAxiom.leftTermInverse() and \
				negAxiom.leftTerm() in self.__roles:
				
				if negAxiom.rightTerm() in self.__concepts:
					#~ - \exists P^- is not A
					#~ We have to add to queryUnsat the subquery:
					#~ \exists x_counter, y_1. (elementLeft[1][1](y_1, x_counter) and elementRight(x_counter)]
					#~ which, written in a PDDL-EKab format, will be:
					#~ (exists (?x_counter ?y_1) (and (elementLeft[1][1] ?y_1 ?x_counter) (elementRight ?x_counter))
					queryUnsat += "(exists (?x_"+str(counter)+" ?y_1) (and ("+ negAxiom.leftTerm() + \
								" ?y_1 ?x_"+str(counter)+") ("+ negAxiom.rightTerm() +" ?x_"+str(counter)+") ))\n"
				
				elif negAxiom.rightTermExists() and negAxiom.rightTerm() in self.__roles:
					
					if not negAxiom.rightTermInverse():
						#~ - \exists P1^- is not \exists P2
						#~ We have to add to queryUnsat the subquery:
						#~ \exists x_counter, y_1, y_2. (elementLeft[1][1](y_1, x_counter) and elementRight[1](x_counter, y_2)]
						#~ which, written in a PDDL-EKab format, will be:
						#~ (exists (?x_counter ?y_1 ?y_2) (and (elementLeft[1][1] ?y_1 ?x_counter) (elementRight[1] ?x_counter ?y_2))
						queryUnsat += "(exists (?x_"+str(counter)+" ?y_1 ?y_2) (and ("+ negAxiom.leftTerm() + \
										" ?y_1 ?x_"+str(counter)+") ("+ negAxiom.rightTerm() +" ?x_"+str(counter)+" ?y_2) ))\n"
						
					elif negAxiom.rightTermInverse():
						#~ - \exists P1^- is not \exists P2^-
						#~ We have to add to queryUnsat the subquery:
						#~ \exists x_counter,y_1,y_2. (elementLeft[1][1](y_1 x_counter) and elementRight[1][1](?y_2, x_counter)]
						#~ which, written in a PDDL-EKab format, will be:
						#~ (exists (?x_counter ?y_1 ?y_2) (and (elementLeft[1][1] ?y_1 ?x_counter) (elementRight[1][1] ?y_2 ?x_counter))
						queryUnsat += "(exists (?x_"+str(counter)+" ?y_1 ?y_2) (and ("+ negAxiom.leftTerm() + \
										" ?y_1 ?x_"+str(counter)+") ("+ negAxiom.rightTerm() +" ?y_2 ?x_"+str(counter)+") ))\n"
						
					else:
						raise Exception("Something went wrong during the building of query_unsat. The following element couldn't be recognized: " + str(negAxiom.rightTerm()) )
				else:
					raise Exception("Something went wrong during the building of query_unsat. The following element couldn't be recognized: " + str(negAxiom.rightTerm()) )
				
				
			#~ The following "if" is dedicated to tind the following axioms:
			#~ - P1 is not P2
			#~ - P1 is not P2^-
			elif negAxiom.leftTerm() in self.__roles:
				
				if negAxiom.rightTerm() in self.__roles and not negAxiom.rightTermExists():
					
					if not negAxiom.rightTermInverse():
						#~ - P1 is not P2
						#~ We have to add to queryUnsat the subquery:
						#~ \exists x_counter,y_counter. (elementLeft(x_counter,y_counter) and elementRight(x_counter,y_counter))
						#~ which, written in a PDDL-EKab format, will be:
						#~ (exists (?x_counter ?y_counter) (and (elementLeft ?x_counter ?y_counter) (elementRight ?x_counter ?y_counter) ))
						queryUnsat += "(exists (?x_"+str(counter)+" ?y_"+str(counter)+")" +\
										"(and ("+negAxiom.leftTerm()+" ?x_"+str(counter)+" ?y_"+str(counter)+")" + \
										" ("+negAxiom.rightTerm()+" ?x_"+str(counter)+" ?y_"+str(counter)+") ))\n"
				
					else:
						#~ - P1 is not P2^-
						#~ We have to add to queryUnsat the subquery:
						#~ \exists x_counter,y_counter. (elementLeft(x_counter,y_counter) and elementRight[1](y_counter,x_counter))
						#~ which, written in a PDDL-EKab format, will be:
						#~ (exists (?x_counter ?y_counter) (and (elementLeft ?x_counter ?y_counter) (elementRight[1] ?y_counter ?x_counter) ))
						queryUnsat += "(exists (?x_"+str(counter)+" ?y_"+str(counter)+")" +\
										"(and ("+negAxiom.leftTerm()+" ?x_"+str(counter)+" ?y_"+str(counter)+")" + \
										" ("+negAxiom.rightTerm()+" ?y_"+str(counter)+" ?x_"+str(counter)+") ))\n"
				else:
					#~ Something went wrong
					raise Exception("Something went wrong during the building of query_unsat. The following element couldn't be recognized: " + str(negAxiom) )
				
			#~ The following "if" is dedicated to tind the following axioms:
			#~ - P1^- is not P2
			#~ - P1^- is not P2^-
			elif negAxiom.leftTerm() in self.__roles and negAxiom.leftTermInverse():
				
				if negAxiom.rightTerm() in self.__roles and not negAxiom.rightTermInverse():
					#~ - P1^- is not P2
					#~ We have to add to queryUnsat the subquery:
					#~ \exists x_counter,y_counter. (elementLeft[1](y_counter,x_counter) and elementRight(x_counter,y_counter))
					#~ which, written in a PDDL-EKab format, will be:
					#~ (exists (?x_counter ?y_counter) (and (elementLeft[1] ?y_counter ?x_counter) (elementRight ?x_counter ?y_counter) ))
					queryUnsat += "(exists (?x_"+str(counter)+" ?y_"+str(counter)+")" +\
									"(and ("+negAxiom.leftTerm()+" ?y_"+str(counter)+" ?x_"+str(counter)+")" + \
									" ("+negAxiom.rightTerm()+" ?x_"+str(counter)+" ?y_"+str(counter)+") ))\n"
				
				elif negAxiom.rightTerm() in self.__roles and negAxiom.rightTermInverse():
					#~ - P1^- is not P2^-
					#~ We have to add to queryUnsat the subquery:
					#~ \exists x_counter,y_counter. (elementLeft[1](y_counter,x_counter) and elementRight[1](y_counter,x_counter))
					#~ which, written in a PDDL-EKab format, will be:
					#~ (exists (?x_counter ?y_counter) (and (elementLeft[1] ?y_counter ?x_counter) (elementRight[1] ?y_counter ?x_counter) ))
					queryUnsat += "(exists (?x_"+str(counter)+" ?y_"+str(counter)+")" +\
									"(and ("+negAxiom.leftTerm()+" ?y_"+str(counter)+" ?x_"+str(counter)+")" + \
									" ("+negAxiom.rightTerm()+" ?y_"+str(counter)+" ?x_"+str(counter)+") ))\n"
				else:
					#~ Something went wrong
					raise Exception("Something went wrong during the building of query_unsat. The following element couldn't be recognized: " + str(negAxiom.rightTerm()) )
				
			else:
				#~ Something went wrong
				raise Exception("Something went wrong during the building of query_unsat. The following element couldn't be recognized: " + str(negAxiom.leftTerm()))
			
			#~ Increase the counter
			counter += 1
			
		
		for functAxiom in self.__axiomsFunct:
			
			#~ Each axioms is composed of one element, which could be:
				#~ - funct P , saved as the string 'P'
				#~ - funct P^-, saved as the tuple ('inverse','P')
			
			if functAxiom.leftTerm() in self.__roles:
				if not functAxiom.leftTermInverse():
					#~ It's the case:
					#~ - funct P , saved as the string 'P'
					#~ We have to add to queryUnsat the subquery:
					#~ \exists x_counter, y_1, y_2. (functAxiom(x_counter,y_1) and functAxiom(x_counter,y_2) and (y1 \neq y2))
					#~ which, written in a PDDL-EKab format, will be:
					#~ (exists (?x_counter ?y_1 ?y_2) (and (functAxiom x_counter y_1) (functAxiom x_counter y_2) (neq ?y_1 ?y_2)))
					queryUnsat += "(exists (?x_"+str(counter)+" ?y_1 ?y_2) (and ("+functAxiom.leftTerm() + \
						" ?x_"+str(counter)+" ?y_1) ("+functAxiom.leftTerm()+" ?x_"+str(counter)+" ?y_2) (neq ?y_1 ?y_2)))\n"

				else:
					#~ It's the case:
					#~ - funct P^-, saved as the tuple ('inverse','P')
					#~ We have to add to queryUnsat the subquery:
					#~ \exists y_counter, x_1, x_2. (functAxiom[1](x_1,y_counter) and functAxiom[1](x_2,y_counter) and (x1 \neq x2))
					#~ which, written in a PDDL-EKab format, will be:
					#~ (exists (?y_counter ?x_1 ?x_2) (and (functAxiom[1] x_1 y_counter) (functAxiom[1] x_2 y_counter) (neq ?x_1 ?x_2)))
					queryUnsat += "(exists (?y_"+str(counter)+" ?x_1 ?x_2) (and ("+functAxiom.leftTerm() + \
						" ?x_1 ?y_"+str(counter)+") ("+functAxiom.leftTerm()+" ?x_2 ?y_"+str(counter)+") (neq ?x_1 ?x_2)))\n"
				
			else:
				#~ Something went wrong
				raise Exception("Something went wrong during the building of query_unsat. The following element couldn't be recognized: " + str(functAxiom))
			
			#~ Increase the counter
			counter += 1
		
		#~ If there are more than two axioms from both self.__axiomsNeg and self.__axiomsFunct,
		#~ we have to consider each part that was created as connected by AND.
		#~ We wrap the query in "(and .... )"
		if counter > 1:
			queryUnsat = "(or \n" + queryUnsat + ")"
			
		self.__queryUnsat = UCQ(queryUnsat, self.__concepts, self.__roles, self.__individuals, inequalitiesAllowed = True)
		
	def __parseProblem(self, planningProblemFile):
		#~ The parsing is divided in parts:
		#~ - retrieve the domain name and check that the requirements and the predicates are ok. If not, raise an exception.
		#~ 		From the predicates we create the list of concepts and roles;
		#~ - read the file again to retrieve the axioms, the condition-action rules, and the actions.
		
		syntax = Syntax()
		
		#~ The domain specified in the problem must be the same name specified in the domain parsed before.
		#~ For this reason we put Literal(self.__domainName)
		pddlProblem = StringStart() + \
					syntax.leftPar + syntax.pddlDefineTag + \
					syntax.leftPar + syntax.pddlProblemTag + syntax.pddlProblemName.setResultsName("problemName") + syntax.rightPar + \
					syntax.leftPar + syntax.pddlProblemDomainTag + Literal(self.__domainName) + syntax.rightPar + \
					syntax.leftPar + syntax.pddlProblemObjectsTag + Group(OneOrMore(syntax.pddlProblemObject)).setResultsName("problemObjects") + syntax.rightPar + \
					syntax.leftPar + syntax.pddlProblemInitTag + Group(OneOrMore(nestedExpr())).setResultsName("problemAssertions") + syntax.rightPar + \
					syntax.leftPar + syntax.pddlProblemGoalTag + nestedExpr().setResultsName("problemGoal") + syntax.rightPar + \
					syntax.rightPar + \
					StringEnd()
		
		#~ Parse the file
		result = pddlProblem.parseFile(planningProblemFile)
		
		self.__problemName = result["problemName"] #Save the problem name
		
		#~ Save the individuals.
		#~ In PDDL they are reffered to as objects.
		for obj in result["problemObjects"]:
			self.__individuals.add(obj)
		
		#~ Save the assertions.
		for assertion in result["problemAssertions"]:
			self.__assertions.add(Assertion(assertion, self.__concepts, self.__roles, self.__individuals))
		
		#~ Save the goal query.
		self.__goalQuery = ECQ(result["problemGoal"][0], self.__concepts, self.__roles, self.__individuals)
		
		#~ Check that the goal query is boolean
		if len(self.__goalQuery.freeVars()) > 0:
			raise Exception("The goal query must be boolean.")
		
	def __compileTBoxAway(self):
		#~ This function is used to rewrite all the queries
		#~ in rules, actions, and queryUnsat to remove the need of the TBox.
		
		#~ Rewrite queryUnsat
		self.__queryUnsatRewritten = rewrite(self.__queryUnsat, self.__axiomsPos, self.__concepts, self.__roles, self.__individuals)
		
		#~ Create a new set of rules by rewriting their condition
		for rule in self.__rules:
			self.__rulesRewritten.add((rule[0], rewrite(rule[1], self.__axiomsPos, self.__concepts, self.__roles, self.__individuals), rule[2]))
			
		#~ Create a new set of actions by rewriting the condition in the effects
		for action in self.__actions:
			rewrittenActionEffects = []
			for effect in action[2]:
				rewrittenActionEffects.append((rewrite(effect[0], self.__axiomsPos, self.__concepts, self.__roles, self.__individuals), effect[1], effect[2]))
			
			self.__actionsRewritten.add((action[0],action[1],tuple(rewrittenActionEffects)))
		
		#~ Rewrite goalQuery
		self.__goalQueryRewritten = rewrite(self.__goalQuery, self.__axiomsPos, self.__concepts, self.__roles, self.__individuals)
		
	def domainName(self):
		return self.__domainName
	
	def problemName(self):
		return self.__problemName
	
	def individuals(self):
		return self.__individuals
	
	def concepts(self):
		return self.__concepts
	
	def roles(self):
		return self.__roles
	
	def axiomPos(self):
		return self.__axiomsPos
	
	def axiomNeg(self):
		return self.__axiomsNeg
	
	def axiomFunct(self):
		return self.__axiomsFunct
	
	def assertions(self):
		return self.__assertions
		
	def rules(self):
		return self.__rules
	
	def rulesRewritten(self):
		return self.__rulesRewritten
	
	def actions(self):
		return self.__actions
		
	def actionsRewritten(self):
		return self.__actionsRewritten
		
	def goalQuery(self):
		return self.__goalQuery
		
	def goalQueryRewritten(self):
		return self.__goalQueryRewritten
		
	def queryUnsat(self):
		return self.__queryUnsat
		
	def queryUnsatRewritten(self):
		return self.__queryUnsatRewritten
		
# --------------------------

if __name__ == '__main__':
	
	prova = EKab("planDomain.pddl","planProblem.pddl")
	
	print(prova.individuals())
	
	print("\n-------------------------")
	print("Rewritten rules:")
	for rule in prova.rules():
		for rewRule in prova.rulesRewritten():
			if rule[0] == rewRule[0]:
				print(rule)
				print(rewRule)
				print()
	print("\n-------------------------")
	print("Rewritten Actions:")
	for action in prova.actions():
		for rewAction in prova.actionsRewritten():
			if action[0] == rewAction[0]:
				print(action)
				print(rewAction)
				print()
	
