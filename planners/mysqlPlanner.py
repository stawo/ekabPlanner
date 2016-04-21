import mysql.connector
import copy
import itertools
import networkx
import collections
import random
import logging
from matplotlib import pyplot

#~ Local libraries
from syntax.syntax import Syntax
from ekab.ekab import EKab
from ekab.tbox import *
from queries.cq import *
from queries.ucq import UCQ
from queries.ecq import ECQ

class MySqlPlanner:
	"""
	
	"""
	
	def __init__ (self, ekab, dbConfig):
		
		#~ Check if ekab is a valid eKab
		if not isinstance(ekab, EKab):
			raise Exception("The eKab provided is not valid.")
		
		self.__ekab = ekab
		
		self.__dbConfig = dbConfig
		
		#~ Clean and create the DB
		self.__cleanDB()
		self.__createEkabDB()
		
		#~ Insert the individuals in the table _domain
		#~ Create the connection and the cursor to the DB
		connection = mysql.connector.connect(**self.__dbConfig)
		cursor = connection.cursor()
		
		query = "INSERT INTO _domain (individual) VALUES " + \
				",".join(["('{0}')".format(individual) for individual in self.__ekab.individuals()]) + \
				";"
		cursor.execute(query)
		connection.commit()
		#~ Close the cursor and the connection
		cursor.close()
		connection.close()
		
		#~ Create the initial state, which will be identified by the number 0
		self.__createNewState(-1,0,self.__ekab.assertions())
		
		
		#~ Initialize the planning graph for a given goal.
		#~ A suitable plan is a directed graph.
		self.__planningGraph = networkx.DiGraph()
		
	def __cleanDB(self):
		#~ Function that cleans the DB
		
		#~ Create the connection to the DB
		connection = mysql.connector.connect(**self.__dbConfig)
		#~ Create the cursor
		cursor = connection.cursor()
		
		#~ Drop and recreate the DB, in order to have a clean DB
		cursor.execute("DROP DATABASE IF EXISTS " + self.__dbConfig["database"])
		cursor.execute("CREATE DATABASE IF NOT EXISTS `{0}` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;".format(self.__dbConfig["database"]))
		
		#~ Close the cursor and the connection
		cursor.close()
		connection.close()
	
	def __createEkabDB(self):
		"""
		This function creates a DB that will contain all the states that
		the eKab will generates while we look for a plan.
		The translation of the eKab to SQL is done as following:
			- for each concept, we create a table that has 3 columns:
				- id: represents the primary key, it is an integer;
				- termDomain: represents the individual participating in a 
					membership assertion concept(individual).
				- state: represents in which state the membership assertion
					is appearing.
			- for each role, we create a table that has 4 columns:
				- id: represents the primary key, it is an integer;
				- termDomain: represents the individual ind1 participating in a 
					membership assertion role(ind1, ind2) as the domain.
				- termRange: represents the individual ind2 participating in a 
					membership assertion role(ind1, ind2) as the range.
				- state: represents in which state the membership assertion
					is appearing.
			- a special table "_states" in which there are 2 columns:
				- the hash of a state, which is a primary key
				- the number representing the state, which is a primary key
		"""
		#~ Create the connection to the DB
		connection = mysql.connector.connect(**self.__dbConfig)
		#~ Create the cursor
		cursor = connection.cursor()
		
		for concept in self.__ekab.concepts():
			cursor.execute(self.__createConceptTable(concept))
		for role in self.__ekab.roles():
			cursor.execute(self.__createRoleTable(role))
		
		#~ Create the table for states
		query = """
		CREATE TABLE IF NOT EXISTS `_states` (
		  `stateHash` BIGINT(20) NOT NULL UNIQUE,
		  `stateNum` INT(11) NOT NULL UNIQUE,
		  PRIMARY KEY (`stateHash`)
		) ENGINE=InnoDB DEFAULT CHARSET=latin1 ;
		"""
		cursor.execute(query)
		
		#~ Create the table for storing the hashes of inconsistent states
		query = """
		CREATE TABLE IF NOT EXISTS `_inconsistentStates` (
		  `stateHash` BIGINT(20) NOT NULL UNIQUE,
		  PRIMARY KEY (`stateHash`)
		) ENGINE=InnoDB DEFAULT CHARSET=latin1 ;
		"""
		cursor.execute(query)
		
		#~ Create the table for storing the individuals of the domain
		query = """
		CREATE TABLE IF NOT EXISTS `_domain` (
		  `individual` varchar(30) NOT NULL UNIQUE,
		  PRIMARY KEY (`individual`)
		) ENGINE=InnoDB DEFAULT CHARSET=latin1 ;
		"""
		cursor.execute(query)
		
		#~ Close the cursor and the connection
		cursor.close()
		connection.close()
		
	def __createConceptTable(self, name):
		
		return """
		CREATE TABLE IF NOT EXISTS `{0}` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `termDomain` varchar(30) NOT NULL,
		  `state` int(11) NOT NULL,
		  PRIMARY KEY (`id`)
		) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
		""".format(name)
		
	def __createRoleTable(self, name):
		
		return """
		CREATE TABLE IF NOT EXISTS `{0}` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `termDomain` varchar(30) NOT NULL,
		  `termRange` varchar(30) NOT NULL,
		  `state` int(11) NOT NULL,
		  PRIMARY KEY (`id`)
		) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
		""".format(name)
	
	def __insertMembershipAssertion(self, assertions, stateId):
		#~ This function takes a list membership assertions regarding a state of the
		#~ eKab, and saves it in the DB.
		
		#~ DO INPUT CHECK
		
		#~ Create the connection to the DB
		connection = mysql.connector.connect(**self.__dbConfig)
		#~ Create the cursor
		cursor = connection.cursor(dictionary=True)
		
		
		for assertion in assertions:
			
			query = ""
			
			if assertion.individual2() is None:
				#~ The assertion is about a concept, thus the values inserted
				#~ in the table regard the columns "domain" and "state"
				query += "INSERT INTO {0} (termDomain, state) VALUES ('{1}',{2});\n".format(assertion.term(), assertion.individual1(), stateId)
			else:
				#~ The assertion is about a concept, thus the values inserted
				#~ in the table regard the columns "domain" and "state"
				query += "INSERT INTO {0} (termDomain, termRange, state) VALUES ('{1}','{2}',{3});\n".format(assertion.term(), assertion.individual1(), assertion.individual2(), stateId)
			
			cursor.execute(query)
			
		
		#~ Check the consistency of the state after the insert
		#~ We can't use the function __consistencyCheck(), as we already have
		#~ an open connection and we did some changes to the DB.
		query = self.__ekab.queryUnsatRewritten().toSQL(state = stateId)
		cursor.execute(query)
		result = cursor.fetchall()
		
		if result[0]["booleanValue"] == 0:
			#~ The state is consistent, we commit the changes
			connection.commit()
			
			#~ Close the cursor and the connection
			cursor.close()
			connection.close()
			
			#~ Return True to indicate the success of the operation
			return True
			
		elif result[0]["booleanValue"] == 1:
			#~ The state is not consistent, we rollback the changes
			connection.rollback()
			
			#~ Close the cursor and the connection
			cursor.close()
			connection.close()
			
			#~ Return False to indicate the failure of the operation
			return False
		
		#~ The returned result is not valid raise an Exception
		raise Exception("The SQL query of the rewritten query q_unsat returned an invalid result:\n" + str(result))
			
		
	def __executeSqlQuery(self, query, state = 0, substitutions = {}):
		#~ The function executes the query over the DB,
		#~ and returns the results
		
		#~ The query can be passed as a string, or as a eKab query (CQ, UCQ, ECQ).
		#~ In the first case, we execute the query as it is and return the results.
		#~ In the second case, we translate the query to SQL by (eventually)
		#~ passing the parameters state and substitution (if specified).
		#~ Also, we check if the query is boolean, in which case we return True
		#~ or False.
		
		
		if isinstance(query, str):
			#~ The query is passed as a string. We execute it as it is.
			#~ Create the connection to the DB
			connection = mysql.connector.connect(**self.__dbConfig)
			#~ Create the cursor
			cursor = connection.cursor(dictionary=True)
			
			cursor.execute(query)
			
			result = copy.deepcopy([row for row in cursor])
			
			#~ Close the cursor and the connection
			cursor.close()
			connection.close()
			
			return result
		
		if not isinstance(query, (ECQ, UCQ, CQ)):
			raise Exception("The query must be either a string or an instance of ECQ, UCQ, or CQ.")
			
		
		#~ logger = logging.getLogger("sqlPlanner")
		#~ logger.info("\t\t__executeSqlQuery")
		#~ logger.info("SQL query:")
		#~ logger.info(query)
		#~ logger.info("-"*30)
		
		#~ Create the connection to the DB
		connection = mysql.connector.connect(**self.__dbConfig)
		#~ Create the cursor
		cursor = connection.cursor(dictionary=True)
		
		cursor.execute(query.toSQL(state = state, substitutions = substitutions))
		
		result = copy.deepcopy([row for row in cursor])
		
		#~ Close the cursor and the connection
		cursor.close()
		connection.close()
		
		#~ Check if query is boolean
		if len(query.freeVars()) == 0:
			#~ It's boolean
			if result[0]["booleanValue"] == 1:
				return [{"booleanValue": True}]
			elif result[0]["booleanValue"] == 0:
				return [{"booleanValue": False}]
			
			#~ The returned result is not valid raise an Exception
			raise Exception("The following boolean SQL query returned an invalid result:{0}\nQuery:\n{1}".format(str(result),query.toSQL(state = state, substitutions = substitutions)))
		
		#~ It's not boolean
		return result
		
	def __consistencyCheck(self, stateId):
		#~ The function executes the rewritten query q_unsat over the DB,
		#~ and returns either False if the state is not consistent (the SQL 
		#~ query returns 1, since q_unsat returns True if the state is not
		#~ consistent) or True if the state is consistent (if the SQL query returns 0)
		
		result = self.__executeSqlQuery(self.__ekab.queryUnsatRewritten(), state = stateId)
		
		print("Consistency check for state {0}: {1}".format( str(stateId), str(result[0]["booleanValue"])))
		
		if result[0]["booleanValue"] == False:
			return True
		elif result[0]["booleanValue"] == True:
			return False
		
		#~ The returned result is not valid raise an Exception
		raise Exception("The SQL query of the rewritten query q_unsat returned an invalid result:\n" + str(result))
		
	def __goalCheck(self, stateId):
		#~ The function executes the rewritten query q_unsat over the DB,
		#~ and returns either True (if the SQL query returns 1) or False
		#~ (if the SQL query returns 0)
		
		result = self.__executeSqlQuery(self.__ekab.goalQueryRewritten(), state = stateId)
		
		if result[0]["booleanValue"] == False:
			return False
		else:
			return True
		
		#~ The returned result is not valid raise an Exception
		raise Exception("The SQL query of the rewritten goal query returned an invalid result:\n" + str(result))
	
	def __createNewState(self, oldStateId, newStateId, addEffectsSet = set(), delEffectsSet = set()):
		#~ This function takes care of the creation of a new state in the DB.
		#~ The creation of a new state is subject to the following operations:
			#~ - the creation is based on a previous state, specified through oldStateId;
			#~ - given oldStateId, we extract all its assertions from the DB and
			#~ generate a set of Assertion() objects;
			#~ - we remove the Assertion() objects specified in delEffectsSet;
			#~ - we add the Assertion() objects specified in addEffectsSet;
			#~ - we calculate the hash of this set, and compare it with the hashes in
			#~ the table that contains the hashes of each state. If the hash already
			#~ exists, it means that the state has already been inserted and its consistency
			#~ checked. We thus return the stateId of the state already inserted in the DB;
			#~ - if the hash is not present in the table, we create a new state;
			#~ - we add all these assertions to the DB, specifying which stateId to use
			#~ - we check the consistency of the new generated state
			#~ - if not consistent, we remove it from the DB, and return False;
			#~ - if consistent, we return the new stateId
		
		if not isinstance(oldStateId, int) or oldStateId < -1:
			raise Exception("The parameter oldStateId must be an integer >= -1")
		
		if not isinstance(newStateId, int) or newStateId < 0:
			raise Exception("The parameter newStateId must be an integer >= 0")
		
		logger = logging.getLogger("sqlPlanner")
		logger.info("__createNewState:")
		logger.info(str(oldStateId) + "," + str(newStateId))
		logger.info("Add:\n" + str(addEffectsSet))
		logger.info("Remove:\n" + str(delEffectsSet))
		
		#~ Retrieve all the assertions of oldStateId
		stateAssertions = set()
		
		#~ We retrieve the assertions belonging to a state only if it is not
		#~ the special case -1, in which case, as we have to create the initial
		#~ state, there are no assertions to retrieve.
		if oldStateId > -1:
			#~ Retrieve all the assertions about concepts
			for concept in self.__ekab.concepts():
				query = "SELECT termDomain FROM {0} WHERE state = {1}".format(concept, str(oldStateId))
				results = self.__executeSqlQuery(query)
				
				#~ print("Fetching: " + query)
				#~ print("results: " + str(results))
				
				if len(results) > 0:
					stateAssertions.update([Assertion([concept, result["termDomain"]], self.__ekab.concepts(), self.__ekab.roles(), self.__ekab.individuals()) for result in results])
					
			#~ Retrieve all the assertions about roles
			for role in self.__ekab.roles():
				query = "SELECT termDomain, termRange FROM {0} WHERE state = {1}".format(role, str(oldStateId))
				results = self.__executeSqlQuery(query)
				
				if len(results) > 0:
					stateAssertions.update([Assertion([role, result["termDomain"], result["termRange"]], self.__ekab.concepts(), self.__ekab.roles(), self.__ekab.individuals()) for result in results])
		
		logger.info("stateAssertions:")
		logger.info(stateAssertions)
		logger.info("-"*10)
		
		#~ Remove all deletion effects
		stateAssertions.difference_update(delEffectsSet)
		
		#~ Add all additional effects
		stateAssertions.update(addEffectsSet)
		
		#~ Calculate the hash of the new state
		stateHash = hash(frozenset(stateAssertions))
		
		logger.info("new stateAssertions:")
		logger.info(stateAssertions)
		logger.info("stateHash:  " + str(stateHash))
		
		
		#~ Check if the new state already exists in the db
		query = "SELECT stateNum FROM _states WHERE stateHash = " + str(stateHash)
		results = self.__executeSqlQuery(query)
		
		#~ logger.info("SELECT stateNum FROM _states WHERE stateHash = " + str(stateHash))
		#~ logger.info("Results: " + str(results))
		
		if len(results) > 0:
			#~ We found that the generated is already present in the DB.
			#~ Return its identifying number.
			
			logger.info("Fine __createNewState. Stato già presente: " + str(results[0]["stateNum"]))
			logger.info("-"*30)
			
			return results[0]["stateNum"]
		
		#~ Check if the new state is already known to be inconsistent in the db
		query = "SELECT COUNT(*) > 0 AS booleanValue FROM _inconsistentStates WHERE stateHash = " + str(stateHash)
		results = self.__executeSqlQuery(query)
		
		if results[0]["booleanValue"] == True:
			#~ We found that the generated is already present in the DB
			#~ and it's inconsistent
			
			logger.info("Fine __createNewState. Stato già presente ed inconsistente.")
			logger.info("-"*30)
			
			return -1
		
		#~ The new state is not present in the DB.
		#~ We thus create it by saving all the statements.
		#~ The function already check for the consistency, and returns -1
		#~ in case the operation can't be performed.
		if not self.__insertMembershipAssertion(stateAssertions,newStateId):
			#~ The new state is not consistent.
			#~ Save its hash in the table _inconsistentStates
			query = "INSERT INTO _inconsistentStates (stateHash) VALUES ({0});".format(str(stateHash))
			
			#~ Create the connection and cursor to the DB
			connection = mysql.connector.connect(**self.__dbConfig)
			cursor = connection.cursor(dictionary=True)
			
			cursor.execute(query)
			connection.commit()
			
			#~ Close the cursor and the connection
			cursor.close()
			connection.close()
			
			logger.info("Fine __createNewState. Stato nuovo ma inconsistente.")
			logger.info("-"*30)
			
			return -1
		
		#~ If consistent, add it to the states table
		query = "INSERT INTO _states (stateHash, stateNum) VALUES ({0},{1});".format(str(stateHash), str(newStateId))
		
		#~ Create the connection and cursor to the DB
		connection = mysql.connector.connect(**self.__dbConfig)
		cursor = connection.cursor(dictionary=True)
		
		cursor.execute(query)
		connection.commit()
			
		#~ Close the cursor and the connection
		cursor.close()
		connection.close()
		
		logger.info("Fine __createNewState. Stato nuovo: " + str(newStateId))
		logger.info("-"*30)
		
		#~ Return the numeric ID of the new state
		return newStateId
		
	#~ Find the planning graph to reach the goal given an eKab
	def findPlanningGraph(self):
		
		self.__endStateId = None
		self.__plan = None
		
		logger = logging.getLogger("sqlPlanner")
		
		#~ 	Launch forward strong planning algorithm
		self.__forwardPlanning()
		
		#~ Find a plan if the goal was met
		if not self.__endStateId is None:
			self.__planNodes = networkx.shortest_path(self.__planningGraph,source=0,target=self.__endStateId)
			
			#~ Create a list that represent a plan where the elements are as follows:
				#~ - [state, rule selected, action selected]
				#~ - [resulting state, rule selected, ... ]
				#~ ...
			self.__plan = list()
			
			networkx.draw(self.__planningGraph)
			pyplot.savefig("path_graph1.png")
			#~ pyplot.show()
			
			logger.info( "-------------------------" )
			logger.info( "if not self.__endStateId is None")
			logger.info("Nodes of graph: ")
			logger.info(self.__planningGraph.nodes())
			logger.info("Edges of graph: ")
			logger.info(self.__planningGraph.edges())
			logger.info( "--" )
			logger.info( self.__planNodes )
			logger.info( "-------------------------" )
			
			for counter in range(len(self.__planNodes)-1):
				self.__plan.append([self.__planNodes[counter], \
					self.__planningGraph[self.__planNodes[counter]][self.__planNodes[counter+1]]["rule"], \
					self.__planningGraph[self.__planNodes[counter]][self.__planNodes[counter+1]]["action"], \
					self.__planningGraph[self.__planNodes[counter]][self.__planNodes[counter+1]]["parameters"]] \
					)
				
				counter += 1
				
			#~ Add the goal state
			self.__plan.append(self.__endStateId)
		
		
			logger.info("Plan:")
			for step in self.__plan:
				logger.info(str(step))
			logger.info("-"*30)
			logger.info( self.__ekab.queryUnsatRewritten().toSQL() )
			logger.info("-"*30)
		
		return self.__plan
	
	"""
	Forward planning algorithm
	
	The algorithm works as follows:
	- create a temporary KB
	- add to the model the current KB and a list of assertions (they
		represent the effect of an action that brought us in this state).
		Filter out from the list the assertions that are already present
		in the KB
	- check if the new KB is consistent. If not, stop the algorithm and
		return False
		We can avoid this step if the actions implement the Blocking Query
	- crete a new state in the planning graph represented by the purged 
		list of assertions added to the KB
	- check if the goal is met in the KB. If yes, stop the algorithm and
		return the purged list of assertions added to the KB (since they
		represent the state in the planning graph)
	- check which actions can be performed
	- for each ground result of each action's precondition query:
		- create a list of Statements using the action's effect with free
		variables substitued by ground terms (taken from the query result)
		- add to the list the statements that were added at this step
		- call again the algorithm and pass the list of statements that
		have to be added
		- wait to get back the id of the planning graph node that results
		from the action effect and connect it with an edge to the node
		created in this step
	- return the purged list of assertions added to the KB (since they
		represent the state in the planning graph)
		
	additionalAssertions is a list of Statements that have to be added
	to the KB.
	"""
	def __forwardPlanning(self, breadthFirst = False):
		
		logger = logging.getLogger("sqlPlanner")
		logger.info( "\n-------------------------" )
		logger.info( "-------------------------" )
		logger.info( "Forward Planning")
		
		#~ Initialization of the elements
		#~ Queue of states to expand. "None" identifies the initial state
		statesToExpand = collections.deque()
		statesToExpand.append(0)
		statesExpanded = collections.deque()
		newStateCounter = 1 # Counter used to name the new generated states
		goalFound = False
		individuals = list(self.__ekab.individuals())
		
		#~ Create the first node in the planning graph
		self.__planningGraph.add_node(0, startingState = True)
		
		#~ Variable to count how many iterations are done
		iteration = 1
		
		while (True):
			
			if len(statesToExpand) == 0 or goalFound:
				break
			
			logger.info( "\n-------------------------" )
			logger.info( "Iteration " + str(iteration))
			logger.info( "Graph size " + str(self.__planningGraph.size()))
			logger.info( "Expanded states " + str(len(statesExpanded)))
			logger.info( "States to expand " + str(len(statesToExpand)))
			#~ logger.debug( "Graph:\n" + self.__planningGraph.exportGraphToDOT())
			#~ logger.debug( "\n")
			iteration += 1
			
			#~ Retrieve one state to expand
			stateId = statesToExpand.pop()
			
			logger.info( "State explored:  " + str(stateId))
			
			#~ Add the state to the list of states already expanded
			statesExpanded.append(stateId)
			
			#~ Check if the goal is met in state
			if self.__goalCheck(stateId):
				
				logger.info( "The goal IS MET.\n")
				
				#~ Set the current state as an ending state in the graph
				#~ Create a node in the planning graph
				self.__planningGraph.node[stateId]['endingState'] = True
				self.__endStateId = stateId
				
				goalFound = True
				
				continue
				
			logger.debug( "The goal is NOT met.")
			
			#~ Check if there are condition-action rules that can be applied to the state
			for rule in self.__ekab.rulesRewritten():
				
				#~ Collect the results of the condition query
				ruleResults = self.__executeSqlQuery(rule[1], state = stateId)
				
				#~ Check if the query is boolean
				if len(rule[1].freeVars()) == 0 and ruleResults[0]["booleanValue"] == False:
					#~ The condition returned False
					#~ Pass to the next rule
					continue
										
				#~ Retrieve the action that the rule triggers
				action = None
				for actionTemp in self.__ekab.actionsRewritten():
					if actionTemp[0] == rule[2]:
						action = actionTemp
				
				#~ Each result is used as a substitution for the parameters of the action
				for ruleResult in ruleResults:
					
					
					#~ We check if all parameters of the actions are covered in the substitution.
					#~ If not, for the ones that are not covered, we pick a random individual from
					#~ the domain and add the substitution.
					ruleResultSubstitutions = dict()
					for var in action[1]:
						if var.toSQL() in ruleResult.keys():
							ruleResultSubstitutions[var.toSQL()] = ruleResult[var.toSQL()]
						else:
							ruleResultSubstitutions[var.toSQL()] = individuals[random.randint(0, len(individuals)-1)]
					
					#~ Sets that contains all the effects that have to be applied to the current
					#~ state to get the new one. They are built by evaluating all the conditional
					#~ effects of the action.
					addEffectsSet = set()
					delEffectsSet = set()
					
					logger.info("-----")
					logger.info("rule: " + str(rule[0]))
					logger.info("rule query: " + rule[1].toSQL(state = stateId))
					logger.info("ruleResult: " + str(ruleResult))
					logger.info("substitutions: " + str(ruleResultSubstitutions))
					logger.info("rule action: " + rule[2])
					logger.info("action: " + action[0])
					
					
					for conditionalEffect in action[2]:
					
						#~ Execute the ECQ of the conditional effect and get the result set
						#~ Use each ruleResult as a substitution for
						#~ the action effects' condition
						
						logger.info("for conditionalEffect in action[2]: conditionalEffect[0]")
						
						logger.info("Query:")
						logger.info(conditionalEffect[0].toSQL(state = stateId, substitutions = ruleResultSubstitutions))
						logger.info("-----------")
						
						effectResults = self.__executeSqlQuery(conditionalEffect[0], state = stateId, substitutions = ruleResultSubstitutions)
						
						logger.info("results:")
						logger.info(str(effectResults) + "\n")
						
						#~ Check if the query is boolean
						if len(conditionalEffect[0].freeVars()) == 0 and effectResults[0]["booleanValue"] == False:
							#~ The effect's condition returned False
							#~ Pass to the next effect
							continue
								
						#~ For every result returned by the effect's condition query,
						#~ we need to create a complete substitution by adding the variables
						#~ that are among the parameters, but do not appear in the query.
						#~ We add the missing variables directly to each result, and take
						#~ the specific substitution from ruleResultSubstitutions (as we
						#~ already fixed there a value for the missing parameters).
						for result in effectResults:
							for var in action[1]:
								if not var.toSQL() in result.keys():
									result[var.toSQL()] = ruleResultSubstitutions[var.toSQL()]
						
						
						logger.info("results after adding:")
						logger.info(str(effectResults) + "\n")
						
						#~ Apply the result set to the effects of the conditional effect
						for (addEffect,effectResult) in itertools.product(conditionalEffect[1],effectResults):
							if addEffect.var2() is None:
								#~ The effect is about a concept
								if isinstance(addEffect.var1(),Variable):
									#~ Create an assertion by substituting the variable with the constant
									#~ specified in effectResult.
									addEffectsSet.add(Assertion( \
										[addEffect.term(), \
										effectResult[addEffect.var1().toSQL()]], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
								else:
									#~ The add effect is not using any variable
									addEffectsSet.add(Assertion( \
										[addEffect.term(), \
										addEffect.var1().toSQL()], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
							
							elif isinstance(addEffect.var2(),Constant):
								#~ The effect is about a role, and the second element is a constant
								if isinstance(addEffect.var1(),Variable):
									#~ Create an assertion by substituting the variable with the constant
									#~ specified in effectResult.
									addEffectsSet.add(Assertion( \
										[addEffect.term(), \
										effectResult[addEffect.var1().toSQL()], \
										addEffect.var2().toSQL()], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
								else:
									#~ The add effect is not using any variable
									addEffectsSet.add(Assertion( \
										[addEffect.term(),
										addEffect.var1().toSQL(), \
										addEffect.var2().toSQL()], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
							
							else:
								#~ The effect is about a role, and the second element is a variable
								if isinstance(addEffect.var1(),Variable):
									#~ Create an assertion by substituting the variable with the constant
									#~ specified in effectResult.
									addEffectsSet.add(Assertion( \
										[addEffect.term(), \
										effectResult[addEffect.var1().toSQL()], \
										effectResult[addEffect.var2().toSQL()]], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
								else:
									#~ The add effect is not using any variable
									addEffectsSet.add(Assertion( \
										[addEffect.term(),
										addEffect.var1().toSQL(), \
										effectResult[addEffect.var2().toSQL()]], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
							
						#~ Apply the result set to the effects of the conditional effect
						for (delEffect,effectResult) in itertools.product(conditionalEffect[2],effectResults):
							if delEffect.var2() is None:
								#~ The effect is about a concept
								if isinstance(delEffect.var1(),Variable):
									#~ Create an assertion by substituting the variable with the constant
									#~ specified in effectResult.
									delEffectsSet.add(Assertion( \
										[delEffect.term(), \
										effectResult[delEffect.var1().toSQL()]], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
								else:
									#~ The add effect is not using any variable
									delEffectsSet.add(Assertion( \
										[delEffect.term(), \
										delEffect.var1().toSQL()], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
							
							elif isinstance(delEffect.var2(),Constant):
								#~ The effect is about a role, and the second element is a constant
								if isinstance(delEffect.var1(),Variable):
									#~ Create an assertion by substituting the variable with the constant
									#~ specified in effectResult.
									delEffectsSet.add(Assertion( \
										[delEffect.term(), \
										effectResult[delEffect.var1().toSQL()], \
										delEffect.var2().toSQL()], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
								else:
									#~ The add effect is not using any variable
									delEffectsSet.add(Assertion( \
										[delEffect.term(),
										delEffect.var1().toSQL(), \
										delEffect.var2().toSQL()], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
							
							else:
								#~ The effect is about a role, and the second element is a variable
								if isinstance(delEffect.var1(),Variable):
									#~ Create an assertion by substituting the variable with the constant
									#~ specified in effectResult.
									delEffectsSet.add(Assertion( \
										[delEffect.term(), \
										effectResult[delEffect.var1().toSQL()], \
										effectResult[delEffect.var2().toSQL()]], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
								else:
									#~ The add effect is not using any variable
									delEffectsSet.add(Assertion( \
										[delEffect.term(),
										delEffect.var1().toSQL(), \
										effectResult[delEffect.var2().toSQL()]], \
										self.__ekab.concepts(), \
										self.__ekab.roles(), \
										self.__ekab.individuals() \
										))
									
					#~ Create a new state in the DB
					newStateId = self.__createNewState(stateId, newStateCounter, addEffectsSet, delEffectsSet)
					
					logger.info( "newStateCounter: " + str(newStateCounter))
					logger.info( "newStateId: " + str(newStateId))
					
					
					if newStateId == -1:
						#~ The new state was inconsistent
						#~ Do nothing
						pass
						
					elif newStateCounter != newStateId:
						#~ The state was already in the DB
						#~ Add to the planning graph the new state
						self.__planningGraph.add_node(newStateId)
						#~ Connect it with the previous one.
						self.__planningGraph.add_edge(stateId, newStateId, rule = rule[0], action = rule[2], parameters = effectResults)
						
					else:
						#~ The new state is consistent and didn't exist in the DB
						#~ Add it to the states expand
						if newStateId not in statesExpanded:
							statesToExpand.append(newStateId)
						
						#~ Add to the planning graph the new state
						self.__planningGraph.add_node(newStateId)
						#~ Connect it with the previous one.
						self.__planningGraph.add_edge(stateId, newStateId, rule = rule[0], action = rule[2], parameters = effectResults)
						
						#~ Increase newStateCounter
						newStateCounter += 1
						
						
					
			logger.debug( "\tStates to expand: " + str(len(statesToExpand)))
				
			#~ The algorythm ended well
		
		#~ I need to prune the planning graph, in order to remove all paths
		#~ that do not end in the goal state
		
		return True
		
	#~ Export the graph in DOT notation
	def exportGraphToDOT(self, filename="graph", directory = None):
		
		#~ fileName must be a valid string
		if not isinstance(filename, basestring):
			raise AttributeError("The name given is not a valid string.")
		
		#~ Check that directory is a valid string and exists
		if not( isinstance(directory, basestring) and \
			os.path.isdir(directory)):
			raise AttributeError("The directory given is not a valid string or directory.")
			
		if isinstance(self.__planningGraph, BasicGraph):
			#~ Get the graph as a string
			#~ graphString = sw.toString()
			graphString = self.__planningGraph.exportGraphToDOT()
			
			#~ Remove from the string all occurences of the local namespace
			graphString = graphString.replace(self.__modelMainNamespace, "")
			
			#~ Clean filename
			keepcharacters = ('.','_') # Special characters I want to keep
			filename = "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()
			#~ Add the extension
			filename += ".dot"
			#~ Join directory and filename
			filename = os.path.join(directory,filename)
			
			#~ Write the graph string on a file
			fp = open(filename,'w')
			fp.write(graphString)
			fp.close()
			
			return True
		
		#~ If I'm here, it means there is no graph to export
		return False


if __name__ == "__main__":
	
	#~ dbConfig = {
		  #~ 'user': 'prova',
		  #~ 'password': 'qwerty',
		  #~ 'host': '127.0.0.1',
		  #~ 'database': 'planner',
		  #~ 'raise_on_warnings': True,
		#~ }
	
	dbConfig = {
		  'user': 'prova',
		  'password': 'qwerty',
		  'host': '127.0.0.1',
		  'database': 'planner'
		}
	
	ekab = EKab("planDomain2.pddl","planProblem2.pddl")
	
	sqlPlanner = Planner(ekab, dbConfig)
	
	print(sqlPlanner.findPlanningGraph())
