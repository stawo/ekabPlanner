import logging
import inspect
import os
import sys
import subprocess
import time

#~ Local libraries
from syntax.syntax import Syntax
from ekab.ekab import EKab
from planners.mysqlPlanner import MySqlPlanner
from lib.logger import custom_logger

def indent(indentLevel):
	
	if not isinstance(indentLevel, int) or indentLevel < 1:
		raise Exception("Indent level must be a positive integer.")
	
	syntax = Syntax()
	
	return syntax.indent*indentLevel
	
class ekabPlanner:
	"""
	The ekabPlanner class takes as input an EKab instance, and allows to perform
	various planning-related operations over it, such as:
	- toADL(): translates the EKab in an ADL planning problem, expressed in PDDL.
			The resulting files (one for the planning domain, one for the planning problem)
			can be fed to an ADL planner;
	- callADLPlanner(): call the specified ADL planner, and feeds it the translated PDDL-ADL
			planning problem;
	- callMySqlPlanner(): call the planner based on MySql and the Forward Planning algorithm;
	-
	"""
	
	def __init__(self, ekab):
		
		
		if not isinstance(ekab, EKab):
			raise Exception("The eKab provided is not valid.")
			
		self.__ekab = ekab
		
	def toADL(self, domainOutputFilePath, problemOutputFilePath):
		"""The function toADL translates an input eKab to a PDDL-ADL
		planning problem."""
		
		#~ An ADL planning problem written in PDDL is composed by two parts,
		#~ the domain file and the problem file.
		#~ We start by creating the domain file, which contains the following sections:
		#~ (domain domain name)
		#~ (:requirements :adl)
		#~ (:predicates predicates list)
		#~ (:action action name
		#~ :parameters ( parameters )
		#~ :precondition precondition Query
		#~ :effect effects
		#~ )
		#~ ... more actions
		#~ 
		#~ An ADL action is the merge of an eKab condition/action rule with
		#~ the related called action.
		#~ An ADL action is formed as follow:
		#~ (:action action name
		#~ :parameters ( parameters )
		#~ :precondition precondition Query
		#~ :effect effects
		#~ )
		#~ where:
			#~ - parameters are the parameters of the eKab action
			#~ - the precondition query is the rule's condition, to which we
			#~   add the negated boolean predicates CheckConsistency and Error
			#~ - the effect of the action is the conjunction of the effects of
			#~   the eKab action, plus the boolean predicate CheckConsistency
		#~ 
		#~ The problem file contains the following sections:
		#~ (define (problem problem name)
		#~ (:domain domain name)
		#~ (:objects individuals list)
		#~ (:init membership assertions list + (not (CheckConsistency)) + (not (Error)) )
		#~ (:goal
		#~ rewritten goal query
		#~ )	
			
		syntax = Syntax()
		
		indentLevel = 1
		
		#~ Check if domainOutputFilePath is a proper file path
		if not isinstance(domainOutputFilePath, str):
			raise Exception("The file path for the planning domain must be a string! Type provided: " + str(type(domainOutputFilePath)))
		if domainOutputFilePath[-5:] != ".pddl":
			raise Exception("The file for the planning domain must have a .pddl extension!")
		
		#~ Check if domainOutputFilePath is already a file.
		#~ If yes, ask for permission to overwrite it.
		if os.path.isfile(domainOutputFilePath):
			
			while True:
				print("The specified file (" + domainOutputFilePath + ") already exists. Overwrite it?")
				answer = input("Y/n: ")
				
				if answer == "Y" or answer == "y":
					break
				elif answer == "N" or answer == "n":
					print("OK. The translation to ADL will halt here.")
					return 0
				else:
					print("Answer not recognized. Please type either \"Y\" or \"n\".")
		
		#~ Check if problemOutputFilePath is a proper file path
		if not isinstance(problemOutputFilePath, str):
			raise Exception("The file path for the planning problem must be a string! Type provided: " + str(type(problemOutputFilePath)))
		if problemOutputFilePath[-5:] != ".pddl":
			raise Exception("The file for the planning problem must have a .pddl extension!")
		
		#~ Check if problemOutputFilePath is already a file.
		#~ If yes, ask for permission to overwrite it.
		if os.path.isfile(problemOutputFilePath):
			
			while True:
				print("The specified file (" + problemOutputFilePath + ") already exists. Overwrite it?")
				answer = input("Y/n: ")
				
				if answer == "Y" or answer == "y":
					break
				elif answer == "N" or answer == "n":
					print("OK. The translation to ADL will halt here.")
					return 0
				else:
					print("Answer not recognized. Please type either \"Y\" or \"n\".")
		
		
		#~ Open the file for the domain
		domainOutputFile = open(domainOutputFilePath, "wt")
		
		#~ Write "(define"
		domainOutputFile.write("(define\n")
		#~ Write the domain name
		domainOutputFile.write(indent(indentLevel) + "(domain " + self.__ekab.domainName() + ")\n")
		#~ Write "(:requirements :adl)"
		domainOutputFile.write(indent(indentLevel) + "(:requirements :adl)\n")
		#~ Write the predicates list
		domainOutputFile.write(indent(indentLevel) + "(:predicates\n")
		indentLevel += 1
		for concept in self.__ekab.concepts():
			domainOutputFile.write(indent(indentLevel) + "(" + str(concept) + " ?x )\n")
		for role in self.__ekab.roles():
			domainOutputFile.write(indent(indentLevel) + "(" + str(role) + " ?x ?y )\n")
		
		#~ Add the boolean predicates CheckConsistency and Error
		domainOutputFile.write(indent(indentLevel) + "(" + syntax.ADLCheckConsistency + ")\n")
		domainOutputFile.write(indent(indentLevel) + "(" + syntax.ADLError + ")\n")
		
		#~ Close the :predicates section
		indentLevel -= 1
		domainOutputFile.write(indent(indentLevel) + ")\n") 
		
		#~ Write the actions
		#~ We use the rewritten actions
		for action in self.__ekab.actionsRewritten():
			
			#~ Find the related rewritten rule
			relatedRule = None
			for rule in self.__ekab.rulesRewritten():
				if rule[2] == action[0]:
					relatedRule = rule
					break
			
			if relatedRule is None:
				#~ The action has no related rule, and this can't be
				raise Exception("The action " + action[0] + " has no related rule, and this can't be.")
			
			#~ Write the action name
			domainOutputFile.write(indent(indentLevel) + "(:action " + action[0] + "\n")
			indentLevel += 1
			
			#~ Write the action's parameters.
			#~ parameters are the parameters of the eKab action
			domainOutputFile.write(indent(indentLevel) + ":parameters ( ")
			for param in action[1]:
				domainOutputFile.write(str(param) + " ")
			domainOutputFile.write(")\n")
			
			#~ Write the action's precondition.
			#~ The precondition query is the rule's condition, to which we
			#~ add the negated boolean predicates CheckConsistency and Error
			domainOutputFile.write(indent(indentLevel) + ":precondition ( and\n")
			domainOutputFile.write(indent(indentLevel +1) + "(not (" + syntax.ADLCheckConsistency + "))\n")
			domainOutputFile.write(indent(indentLevel +1) + "(not (" + syntax.ADLError + "))\n")
			domainOutputFile.write(relatedRule[1].toADL(indentLevel +1))
			domainOutputFile.write(indent(indentLevel) + ")\n") # Close the precondition
			
			#~ Write the effects of the action
			domainOutputFile.write(indent(indentLevel) + ":effect ( and\n")
			indentLevel += 1
			domainOutputFile.write(indent(indentLevel) + "(" + syntax.ADLCheckConsistency + ")\n")
			#~ For each effect in the eKab action, we create a conditional ADL effect
			for effect in action[2]:
				domainOutputFile.write(indent(indentLevel) + "(when\n" + effect[0].toADL(indentLevel+1))
				domainOutputFile.write(indent(indentLevel+1) + "(and\n")
				#~ Add the add effects
				for addEff in effect[1]:
					domainOutputFile.write(addEff.toADL(indentLevel+2))
				#~ Add the del effects
				for delEff in effect[2]:
					domainOutputFile.write(indent(indentLevel+2) + "(not " + delEff.toADL(0) + ")\n")
				#~ domainOutputFile.write(indent(indentLevel+2) + ")\n") # Close not
				domainOutputFile.write(indent(indentLevel+1) + ")\n") # Close and
				
				domainOutputFile.write(indent(indentLevel) + ")\n") # Close when
			
			indentLevel -= 1
			domainOutputFile.write(indent(indentLevel) + ")\n") # Close the effect
			
			indentLevel -= 1
			domainOutputFile.write(indent(indentLevel) + ")\n") # Close the action
		
		#~ Add the special action to check consistency
		domainOutputFile.write(indent(indentLevel) + "(:action " + syntax.ADLCheckConsistencyAction + "\n")
		indentLevel += 1
		
		#~ The action has no parameters, since queryUnsatRewritten is a boolean query
		domainOutputFile.write(indent(indentLevel) + ":parameters ( )\n")
		
		#~ Write the action's precondition.
		#~ The precondition query is conjunction of
		#~ the boolean predicate CheckConsistency and the negated Error
		domainOutputFile.write(indent(indentLevel) + ":precondition ( and\n")
		domainOutputFile.write(indent(indentLevel +1) + "(" + syntax.ADLCheckConsistency + ")\n")
		domainOutputFile.write(indent(indentLevel +1) + "(not (" + syntax.ADLError + "))\n")
		domainOutputFile.write(indent(indentLevel) + ")\n") # Close the precondition
		
		#~ Write the effects of the action, which are two:
		#~ - one has as precondition queryUnsatRewritten, and, if Ture, set Error to True
		#~ - the other simply set to False CheckConsistency
		domainOutputFile.write(indent(indentLevel) + ":effect ( and\n")
		indentLevel += 1
		domainOutputFile.write(indent(indentLevel) + "(not (" + syntax.ADLCheckConsistency + "))\n")
		domainOutputFile.write(indent(indentLevel) + "(when\n" + self.__ekab.queryUnsatRewritten().toADL(indentLevel+1))
		domainOutputFile.write(indent(indentLevel+1) + "(" + syntax.ADLError + ")\n")
		domainOutputFile.write(indent(indentLevel) + ")\n") # Close when
		indentLevel -= 1
		domainOutputFile.write(indent(indentLevel) + ")\n") # Close the effect
		
		indentLevel -= 1
		domainOutputFile.write(indent(indentLevel) + ")\n") # Close the action
		
		domainOutputFile.write(")") # Close define
		
		#~ Close the file
		domainOutputFile.close()
		
		#~ -----------------------------------------------------------
		
		#~ Open the file for the domain
		problemOutputFile = open(problemOutputFilePath, "wt")
		
		#~ Write "(define (problem problem name)"
		problemOutputFile.write("(define (problem " + self.__ekab.problemName() + " )\n")
		#~ Write the domain name
		problemOutputFile.write(indent(indentLevel) + "(:domain " + self.__ekab.domainName() + ")\n")
		#~ Write the individuals list
		problemOutputFile.write(indent(indentLevel) + "(:objects\n" + indent(indentLevel+1))
		for individual in self.__ekab.individuals():
			problemOutputFile.write(str(individual) + " ")
		problemOutputFile.write("\n" + indent(indentLevel) + ")\n") # Close :objects
		
		#~ Write the membership assertions list
		problemOutputFile.write(indent(indentLevel) + "(:init\n")
		for assertion in self.__ekab.assertions():
			problemOutputFile.write(assertion.toADL(indentLevel+1))
		#~ Add (not (CheckConsistency)) and (not (Error))
		problemOutputFile.write(indent(indentLevel+1) + "(not (" + syntax.ADLCheckConsistency + "))\n")
		problemOutputFile.write(indent(indentLevel+1) + "(not (" + syntax.ADLError + "))\n")
		
		problemOutputFile.write(indent(indentLevel) + ")\n") # Close :init
		
		#~ Write the goal
		problemOutputFile.write(indent(indentLevel) + "(:goal\n")
		problemOutputFile.write(indent(indentLevel+1) + "(and\n")
		problemOutputFile.write(indent(indentLevel+2) + "(not (" + syntax.ADLCheckConsistency + "))\n")
		problemOutputFile.write(indent(indentLevel+2) + "(not (" + syntax.ADLError + "))\n")
		problemOutputFile.write(self.__ekab.goalQueryRewritten().toADL(indentLevel+2))
		problemOutputFile.write(indent(indentLevel+1) + ")\n") # Close and
		problemOutputFile.write(indent(indentLevel) + ")\n") # Close :goal
			
		problemOutputFile.write(")") # Close define
		
		#~ Close the file
		problemOutputFile.close()
		
		
	def toDCDS(self, outputFile):
		"""
		The translation to a DCDS requires the translation of the eKab
		to elements fo a database.
		The translation is done as following:
			- each concept and role are translated to tables with, respectively,
			one and two columns, named "domain" and "range";
			- membership assertions are translated by adding rows to the respective
			tables;
			- queries are translated to SQL queries;
		"""	
		pass

	def callADLPlanner(self, plannerExecutable, domainOutputFilePath, problemOutputFilePath):
		
		def get_script_dir(follow_symlinks=True):
			if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
				path = os.path.abspath(sys.executable)
			else:
				path = inspect.getabsfile(get_script_dir)
			if follow_symlinks:
				path = os.path.realpath(path)
			return os.path.dirname(path)
		
		startTimeTranslation = time.process_time()
		#~ Translate the eKab to ADL
		self.toADL(domainOutputFilePath, problemOutputFilePath)
		stopTimeTranslation = time.process_time()
		startTimePlanning = time.process_time()
		#~ Call the planner
		plannerCommand = [os.path.join(get_script_dir(), plannerExecutable), domainOutputFilePath, problemOutputFilePath, \
								"--heuristic","hff=ff()", "--search","lazy_greedy(hff, preferred=hff)"]
		result = None
		print(plannerCommand)
		try:
			result = subprocess.Popen(plannerCommand, universal_newlines=True, stdout=subprocess.PIPE)
			resultOutput = result.communicate()[0]
		except subprocess.CalledProcessError as error:
			print(error.output)
			return -1
		
		stopTimePlanning = time.process_time()
		
		print("-------------------------")
		if not result is None:
			print(resultOutput)
		print("Translation time: " + str(stopTimeTranslation - startTimeTranslation))
		print("Planning time: " + str(stopTimePlanning - startTimePlanning))
		
	def callDCDSPlanner(self, plannerExecutable):
		pass
	
	def callMySqlPlanner(self,dbConfig):
		
		#~ Create a MySqlPlanner
		planner = MySqlPlanner(self.__ekab, dbConfig)
		
		#~ Find if there is a plan
		plan = planner.findPlanningGraph()
		
		return plan

#~ Set the logging
logger = custom_logger('sqlPlanner')

# create a file handler
#~ handler = logging.FileHandler('sqlPlanner.log', mode='w')
#~ handler.setLevel(logging.WARNING)
#~ handler.setLevel(logging.DEBUG)

# create a logging format
#~ formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#~ handler.setFormatter(formatter)

# add the handlers to the logger
#~ logger.addHandler(handler)


#~ logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
		

if __name__ == '__main__':
	
	prova = EKab("taskAssigment.pddl","taskAssigment-problem.pddl")
	
	#~ print(prova.individuals())
	#~ 
	#~ print("\n-------------------------")
	#~ print("Rewritten rules:")
	#~ for rule in prova.rules():
		#~ for rewRule in prova.rulesRewritten():
			#~ if rule[0] == rewRule[0]:
				#~ print(rule)
				#~ print(rewRule)
				#~ print()
	#~ print("\n-------------------------")
	#~ print("Rewritten Actions:")
	#~ for action in prova.actions():
		#~ for rewAction in prova.actionsRewritten():
			#~ if action[0] == rewAction[0]:
				#~ print(action)
				#~ print(rewAction)
				#~ print()
	
	planner = ekabPlanner(prova)
	
	#~ print(prova.queryUnsat())
	#~ print("-"*20)
	#~ print(prova.queryUnsatRewritten())
	
	dbConfig = {
		  'user': 'prova',
		  'password': 'qwerty',
		  'host': '127.0.0.1',
		  'database': 'planner'
		}
		
	plan = planner.callMySqlPlanner(dbConfig)
	print("Plan:")
	if plan is None:
		print(plan)
	else:
		for step in plan:
			print(str(step))
	
	#~ planner.callADLPlanner("planners/FastDownward/fast-downward.py","adl-domain.pddl","adl-problem.pddl")
	
	
