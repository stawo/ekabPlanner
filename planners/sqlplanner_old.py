import sqlite3
import logging

concepts = set(["ticket","customer","place"])
roles = set(["owns","hasToPay"])	

class TBox:
	
	def __init__(self, concepts = None, roles = None):
		if not isinstance(concepts, set) or not isinstance(roles, set):
			raise AttributeError("The given concepts and roles are not valid sets.")
		
		for concept in concepts:
			if not isinstance(concept, str):
				raise AttributeError("The given concept is not a valid one.")
		
		for role in roles:
			if not isinstance(role, str):
				raise AttributeError("The given concept is not a valid one.")
		
		self.__concepts = concepts
		self.__roles = roles
		
	def getConcepts(self):
		return self.__concepts
		
	def getRoles(self):
		return self.__roles
		
	
class ABox:
	
	def __init__(self, tbox = None, conceptAssertions = None, roleAssertions = None):
		
		if not isinstance(tbox, TBox):
			raise AttributeError("The given TBox is not a valid one.")
		
		if not isinstance(conceptAssertions, set) or not isinstance(roleAssertions, set):
			raise AttributeError("The given assertions are not valid sets.")
		
		for assertion in conceptAssertions:
			if not isinstance(assertion, list) \
			or len(assertion) != 2 \
			or not isinstance(assertion[0], str) \
			or not isinstance(assertion[1], str):
				raise AttributeError("The given concept membership assertion is not a valid one.")
				
		for assertion in roleAssertions:
			if not isinstance(assertion, list) \
			or len(assertion) != 3 \
			or isinstance(assertion[0], str) \
			or isinstance(assertion[1], str) \
			or isinstance(assertion[2], str):
				raise AttributeError("The given role membership assertion is not a valid one.")
		
		self.__tbox = tbox
		self.__conceptAssertions = conceptAssertions
		self.__roleAssertions = roleAssertions
		self.__db = None
		self.__cursor = None
	
	def __createDB(self):
		self.__db = sqlite3.connect(':memory:')
		self.__cursor = self.__db.cursor()
		
		# Create table
		for concept in self.__tbox.getConcepts():
			self.__cursor.execute("CREATE TABLE " + concept + " (individual text PRIMARY KEY)")

		for role in self.__tbox.getRoles():
			self.__cursor.execute("CREATE TABLE " + role + " (individual1 text, individual2 text)")

		# Insert concept membership assertions
		for assertion in self.__conceptAssertions:
			try:
				self.__cursor.execute("INSERT INTO " + assertion[0] + " VALUES ('" + assertion[1] + "')")
			except:
				print("The assertion " + assertion[0] + "(" + assertion[1] + ") couldn't be inserted in the DB.")
				raise
		
		# Save (commit) the changes
		self.__db.commit()
		
		# Insert role membership assertions
		for assertion in self.__roleAssertions:
			try:
				self.__cursor.execute("INSERT INTO " + assertion[0] + " VALUES ('" + assertion[1] + "," + assertion[2] + "')")
			except:
				print("The assertion " + assertion[0] + "(" + assertion[1] + "," + assertion[2] + ") couldn't be inserted in the DB.")
				raise
		
		# Save (commit) the changes
		self.__db.commit()
	
	def __closeDB(self):
		if self.__db is not None:
			self.__db.close()
		
	def query(self, query):
		self.__createDB()
		self.__closeDB()
		
	def toSetStrings(self):
		#~ stateDump = set([])
		#~ for predicate in concepts:
			#~ for row in self.__cursor.execute('SELECT * FROM ' + predicate):
				#~ stateDump.add(predicate + "(" + str(row[0]) + ")")
		#~ for predicate in roles:
			#~ for row in self.__cursor.execute('SELECT * FROM ' + predicate):
				#~ stateDump.add(predicate + "(" + str(row[0]) + "," + str(row[1]) + ")")
		
		return self.__conceptAssertions.union(self.__roleAssertions)
	
	def __del__(self):
		if self.__db is not None:
			self.__db.close()
		
	def __eq__(self, other):
		#~ Check if other is a valid state
		if not isinstance(other, ABox):
			raise AttributeError("The element we are trying to compare is not a valid abox.")
		
		if self.toSetStrings() == other.toSetStrings():
			return True
		
		return False
	
class StateQueue:
	"""
	Special class to represent a queue of states (namely ABoxes).
	States are in-memory DBs, and can be represented as a set of strings.
	We assume that different states	generate different sets.
	We will use the sets in a deque to know if an element has already been
	added or not.
	A list (or set) of DBs will be transformed in a set of sets of strings.
	"""
	
	def __init__(self, fifo = True):
		
		#~ Create a deque for the states
		self.__states = deque()
		
		#~ Save the type of queue
		self.__fifo = fifo
	
	#~ Returns the lenght of the queue
	def __len__(self):
		return len(self.__queueStates)
		
	#~ Returns True if state is already present in the queue, False otherwise
	def __findElement(self, abox):
		
		for state in self.__states:
			if (len(state) == len(abox)
			and state == abox
			):
				return True
		
		#~ If I reach this point, means no correspondence is found
		return False
	
	def append(self, state):
		
		#~ Check if state is a valid DB
		if not isinstance(state, ABox):
			raise AttributeError("The given state is not a valid ABox.")
		
		#~ Check if the state is already in the deque
		#~ Add it to the deque if not
		if not self.__findElement(state):
			#~ Append state to __queueStates
			if self.__fifo:
				self.__states.appendleft(state)
			else:
				self.__states.append(state)
	
	def pop(self):
		#~ Return the last state inserted
		return self.__states.pop()

class ConditionalEffect:
	
	def __init__(self, name, ecq, addEffects, removeEffects):
		pass
		
class Action:
	"""
	Class representing actions that allow to modify a state.
	An Action is composed by 3 elements:
		- name: must be a string
		- precondition: an UCQ
		- conditional effects: a list of conditional effects. 	
	"""
	
	def __init__(self, name, precondition_ucq, conditionalEffects):
		
		#~ Check if name is a valid string
		if not isinstance(name, str):
			raise AttributeError("The name given is not a valid string.")
		
		#~ Check if precondition_ucq is a valid UCQ.
		if not isinstance(precondition_ucq, UnionConjunctiveQueries):
			raise AttributeError("The UCQ given is not valid.")
		
		#~ Check if effects is a list of lists
		if not (
		isinstance(effects, list)
		and (len(effects) >= 1) #~ Check that there is at least one element
		):
			raise AttributeError("The effects given is not valid."
		
		#~ Check if every element of the list is a list of two elements
		for effect in effects:
			if not (
			isinstance(effect, list) #~ Check if it is a list
			and (len(effect) == 2) #~ Check if it has 2 elements
			and (effect[0] in self.__possibleActions) #~ Check if the first string is exactly one of the possible values
			and isinstance(effect[1], Atom) #~ Check that the second element is a valid atom
			):
				raise AttributeError("The effects given is not valid."
			
			#~ Check that the atom:
			#~ 	- is a valid type of atom
			#~ 	- is not negated
			#~ 	- all the variables are also in the query
			if (
			(not effect[1].atomType() in ["concept","role"])
			or effect[1].isNegated()
			):	
				 raise AttributeError("The effect given is negated."
			
			effectVar = set(effect[1].variables())
			if not effectVar.issubset(precondition_ucq.freeVariables()):
				 raise AttributeError("The variables of effect given are not included in the query."
			
		#~ All checks have been passed, I save the elements
		self.__name = name
		self.__precondition_ucq = precondition_ucq
		self.__precondition_ecq = precondition_ecq
		self.__effects = effects
		
	#~ Return the name of the action
	def getName(self):
		return self.__name
	
	#~ Return the UCQ of the action
	def getUCQ(self):
		return self.__precondition_ucq
		
	#~ Return the effects of the action
	def getEffects(self):
		return self.__effects

		
class PlanningGraph:
	"""
	Used to represent a graph and export it in various formats (e.g. DOT)
	The nodes are represented by a set of assertions.
	If no assertion is specified for a vertex, assume it as the initial ABox.
	We assume that a vertex is equal to another if they have the same set of assertions.
	We assume that if a list is passed and contains two equal assertions, then we keep only one.
	Each assertion is represented in string form.
	We can specify a list of namespaces to shorten the strings in the output
	"""
	
	#~ graphTypes=["directed", "undirected"]
	
	#~ def __init__(self, graphType=graphTypes[0], graphNamespaces = None):
	def __init__(self):
		
		#~ if not graphType in self.graphTypes:
			#~ raise AttributeError("The given graph type is not recognized.\nValid types: " + str(graphTypes)
		#~ 
		#~ if not (
		#~ graphNamespaces is None
		#~ or (
			#~ isinstance(graphNamespaces, list)
			#~ and all(isinstance(ns, string) for ns in graphNamespaces)
			#~ )
		#~ ):
			#~ raise AttributeError("The given list of namespaces is not valid.\nIt is either not a list or contains non-string values."
			#~ 
		#~ self.__graphType = graphType
		
		self.__graphVertex = []
		self.__graphVertexLabels = []
		self.__graphVertexStarting = [] # Represents starting states
		self.__graphVertexEnding = [] # Represents ending states
		self.__graphEdge = []
		
	#~ Function that says if a vertex is a valid one or not
	def __isVertex(self, state):
		#~ Check that vertexId is None or a list of strings
		if isinstance(state, ABox):
			return True
		
		return False
	
	#~ Function that find a vertex in the graph given it's id.
	#~ The id is a list of objects
	#~ It returns the position of the vertex if it is already present
	#~ or -1 if it doesn't find it
	def __findVertex(self, vertexToFind):
		
		for vertex in self.__graphVertex:
			if vertex == vertexToFind:
				#~ logger.debug("\tFound two equal vertexes:")
				#~ logger.debug("\t\t" + str(vertex))
				#~ logger.debug("\t\t" + str(vertexToFind))
				return self.__graphVertex.index(vertex)
		
		#~ If I reach this point, it means the vertex is not in the graph
		return -1
		
	#~ Function that returns True if a vertex is in the graph, False otherwise
	def containsVertex(self, vertex):
		
		#~ Check that vertex is a valid one
		if not self.__isVertex(vertex):
			raise AttributeError("The given vertex is not a valid state.")
		
		if self.__findVertex(vertexId) == -1:
			return False
		
		return True
	
	#~ Function that returns the size of the graph, namely the number of vertexes
	def size(self):
		return len(self.__graphVertex)
	
	#~ Function to add a vertex to the graph
	#~ The vertexId is a list of objects that identifies the vertex
	def addVertex(self, vertex, vertexLabel = None, startingState = False, endingState = False):
		
		#~ Check that vertexId is None or a list of strings
		if not self.__isVertex(vertex):
			raise AttributeError("The given vertex is not a valid state.")
		
		#~ Find if the vertex is not already in the graph
		indexVertex = self.__findVertex(vertex)
		if indexVertex == -1:
			#~ Add the vertex to the graph
			self.__graphVertex.append(vertex)
			
			#~ I save the label. In case it is not specified I put an empty string
			if vertexLabel is None:
				self.__graphVertexLabels.append(vertexLabel)
			else:
				self.__graphVertexLabels.append("")
			
			#~ If startingState is True, I put True at the index of the
			#~ vertex in the list of starting states, otherwise False
			self.__graphVertexStarting.append(startingState)
			
			#~ If endingState is True, I put True at the index of the
			#~ vertex in the list of ending states, otherwise False
			self.__graphVertexEnding.append(endingState)
			
		
		else:
			
			#~ I save the label. In case it is not specified I put an empty string
			if vertexLabel is None:
				self.__graphVertexLabels[indexVertex] = vertexLabel
			else:
				self.__graphVertexLabels[indexVertex] = ""
			
			#~ If startingState is True, I put True at the index of the
			#~ vertex in the list of starting states, otherwise False
			self.__graphVertexStarting[indexVertex] = startingState
			
			#~ If endingState is True, I put True at the index of the
			#~ vertex in the list of ending states, otherwise False
			self.__graphVertexEnding[indexVertex] = endingState
		
		
		
	#~ Set a state as a starting state or remove it from the list of them
	def setStartingVertex(self, vertexId, startingVertex = True):
		
		#~ Check that vertex is None or a list of strings
		if not self.__isVertex(vertexId):
			raise AttributeError("The given vertex is not None or a list of strings.")
		
		#~ Find if the vertex is not already in the graph
		indexVertex = self.__findVertex(vertexId)
		if indexVertex == -1:
			#~ If startingState is True, I put True at the index of the
			#~ vertex in the list of starting states, otherwise False
			self.__graphVertexStarting.append(startingVertex)
			
		else:
			#~ If startingState is True, I put True at the index of the
			#~ vertex in the list of starting states, otherwise False
			self.__graphVertexStarting[indexVertex] = startingVertex
			
	
	#~ Set a state as a ending state or remove it from the list of them
	def setEndingVertex(self, vertexId, endingVertex = True):
		#~ Check that vertex is None or a list of strings
		if not self.__isVertex(vertexId):
			raise AttributeError("The given vertex is not None or a list of strings.")
		
		#~ Find if the vertex is not already in the graph
		indexVertex = self.__findVertex(vertexId)
		if indexVertex == -1:
			#~ If endingState is True, I put True at the index of the
			#~ vertex in the list of ending states, otherwise False
			self.__graphVertexEnding.append(endingVertex)
			
		else:
			#~ If endingState is True, I put True at the index of the
			#~ vertex in the list of ending states, otherwise False
			self.__graphVertexEnding[indexVertex] = endingVertex
		
	#~ Function to add an edge to the graph
	#~ An edge is identified also by the label, so two edges that share
	#~ the same vertexes but have different labels, are considered different
	def addEdge(self, vertexA, vertexB, edgeLabel=None):
		#~ Check that vertexA is None or a list of strings
		if not self.__isVertex(vertexA):
			raise AttributeError("The given vertex is not a valid state.")
		
		#~ Check that vertexB is None or a list of strings
		if not self.__isVertex(vertexB):
			raise AttributeError("The given vertex is not a valid state.")
		
		#~ Find if the vertexed are not already in the graph
		indexVertexA = self.__findVertex(vertexA)
		indexVertexB = self.__findVertex(vertexB)
		
		#~ If any of the two vertexes is not present in the graph,
		#~ I raise an error
		if indexVertexA == -1:
			raise AttributeError("Vertex A is not included in the graph.")
		
		if indexVertexB == -1:
			raise AttributeError("Vertex B is not included in the graph.")
			
		#~ Add the edge to the graph if it is not already in it
		if all(
			not((edge[0] == indexVertexA)
			and (edge[1] == indexVertexB)
			and (edge[2] == edgeLabel)
			) for edge in self.__graphEdge):
			self.__graphEdge.append([indexVertexA, indexVertexB, edgeLabel])
		
	
	#~ Function that removes one vertex and all the edges related to it
	#~ from the graph
	def remove(self, vertexId):
		
		#~ Check that vertexId is None or a list of strings
		if not self.__isVertex(vertexId):
			raise AttributeError("The given vertex is not a valid state.")
		
		#~ Search the index of the vertex to remove
		vertexIndex = self.__findVertex(vertexId)
		
		if vertexIndex == -1:
			return False
		
		#~ Remove the vertex from the list
		del self.__graphVertex[vertexIndex]
		del self.__graphVertexStarting[vertexIndex]
		del self.__graphVertexEnding[vertexIndex]
		
		#~ Remove all the edges that has vertex as one of the two vertexes
		for edge in self.__graphEdge:
			if edge[0] == vertexIndex or edge[1] == vertexIndex:
				self.__graphEdge.remove(edge)
	
	#~ Function to export graph in DOT language
	def exportGraphToDOT(self):
		
		graphString = ""
		
		#~ Check the graph type
		if self.__graphType == self.graphTypes[0]:
			#~ Directed graph
			graphString += "digraph "
		
			#~ Add the name of the graph
			graphString += "G {\n"
			
			#~ Add all the vertexes and use the id as a label
			for vertex in self.__graphVertex:
				#~ Save the index
				vertexIndex = self.__graphVertex.index(vertex)
				
				vertexLabel = str(vertex.toSetStrings())
				graphString += "\t" + str(vertexIndex) + " [label = \"" + vertexLabel + "\" "
				
				#~ Check if it is a starting state
				if self.__graphVertexStarting[vertexIndex]:
					graphString += "style=bold "
				
				#~ Check if it is a ending state
				if self.__graphVertexEnding[vertexIndex]:
					graphString += "shape=doublecircle "
				
				#~ Close the line
				graphString += "];\n"
				
			#~ Add all the edges
			for edge in  self.__graphEdge:
				graphString += "\t" + str(edge[0]) + " -> " + str(edge[1]) + " "
				
				#~ Add the label if it is present
				if not edge[2] is None:
					graphString += "[label=\"" + str(edge[2]) + "\"]"
				
				#~ Close the line
				graphString += ";\n"
			
			#~ Close the graph
			graphString += "}"
			
		return graphString

class Planner:
	"""
	
	"""
	
	#~ acceptedActionTypes = ["MonoticHorn"]
	
	
	def __init__ (self, initialState, caRules, actions, goalQuery):
		
		#~ Check if initialState is a valid ABox
		if not isinstance(initialState, ABox):
			raise AttributeError("The given state is not a valid ABox.")
		
		#~ Check if caRules are all valid condition-action rules
		
		#~ Check if actions are all valid actions
		
		#~ check if goalQuery is a valid query
		
		#~ Initial state
		#~ It provides also the TBox with concepts and roles
		self.__initialState = initialState
		
		#~ List of condition action rules and actions
		self.__caRules = caRules
		self.__actions = actions
		
		#~ Initialize the goal query
		self.__goalQuery = goalQuery
		
		#~ Initialize the planning graph for a given goal.
		#~ The meaning of possible values is:
		#~ 	- False: the function findPlanningGraph() has not been run, so we don't
		#~ 		know if there is a valid planning graph
		#~ 	- True: the goal is trivial and is already met by the current KB
		#~ 	- empty graph: the empty list denotes that the planner didn't find any
		#~ 		suitable plan to reach the goal.
		#~ A suitable plan is a directed graph.
		self.__planningGraph = False
		
	#~ Find the planning graph to reach the goal given an initial KB
	#~ and a set of possible actions.
	#~ We can use two algorithms to find a planning graph: forward or backward.
	def findPlanningGraph(self, goalQuery = None, algorithmType = "forward", checkConsistency=True):
		
		#~ If goal_ucq is defined, check if it's valid and save it
		if goalQuery is not None:
			self.defineGoal(goalQuery)
			
		#~ Initialize the planning graph to False
		self.__planningGraph = False
		
		#~ Check for trivial solutions like:
		#~ 	- the goal is empty
		#~ 		-> set self.__planningGraph = True
		#~ 	- the goal is already met in the current KB
		#~ 		-> set self.__planningGraph = True
		#~ 	- the goal is not met, but there are no available actions
		#~ 		-> set self.__planningGraph = empty graph
		
		#~ Empty goal
		if self.__goalQuery is None or self.__goalQuery == "":
			self.__planningGraph = True
			return True
		
		#~ Check if goal is already met
		solutions = self.__initialState.query(self.__goalQuery)
		if solutions == True:
			#~ The goal is met
			logger.debug( "The goal is already met in the current KB.")
			self.__planningGraph = True
			return True
		
		#~ The goal is not met
		#~ Build an empty graph
		self.__planningGraph = PlanningGraph()
		
		#~ Check if there are any actions
		if len(self.__usableActions) == 0:
			logger.debug( "No usable actions -> no plans available")
			return self.__planningGraph
		
		if algorithmType == "forward":
			#~ 	Launch forward strong planning algorithm
			self.__forwardPlanning()
			
		elif algorithmType == "backward":
			#~ 	Launch backward strong planning algorithm
			self.__backwardStrongPlanning()
			
		else:
			#~ The algorithm specified doesn't exist
			raise AttributeError("The algorithm specified doesn't exist."
		
		return self.__planningGraph
	
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
		
		logger.info( "\n-------------------------" )
		logger.info( "-------------------------" )
		logger.info( "Forward Planning")
		
		#~ Initialization of the elements
		#~ Queue of states to expand. "None" identifies the initial state
		statesToExpand = StateQueue(fifo=breadthFirst)
		statesToExpand.append(self.__initialState)
		statesExpanded = StateQueue()
		planningGraph = self.__planningGraph
		goalFound = False
		
		#~ Create the first node in the planning graph
		planningGraph.addVertex(self.__initialState, startingState = True)
		
		#~ Variable to count how many iterations are done
		iteration = 1
		
		while (True):
			
			if len(statesToExpand) == 0 or goalFound:
				break
			
			logger.info( "\n-------------------------" )
			logger.info( "Iteration " + str(iteration))
			logger.info( "Graph size " + str(planningGraph.size()))
			logger.info( "Expanded states " + str(statesExpanded.size()))
			logger.info( "States to expand " + str(len(statesToExpand)))
			#~ logger.debug( "Graph:\n" + planningGraph.exportGraphToDOT())
			#~ logger.debug( "\n")
			iteration += 1
			
			#~ Retrieve one state to expand
			state = statesToExpand.pop()
			
			logger.info( "State:  " + str(state))
			
			#~ Add the state to the list of states already expanded
			#~ I add it even if it is inconsistent, so I can avoid exploring
			#~ it again in case it is generated by another action
			statesExpanded.addVertex(state)
			
			#~ Check if the goal is met in state
			results = state.query(self.__goalQuery)
			if (
			(isinstance(results, bool) and results)
			or
			(isinstance(results, ResultSet) and results.hasNext())
			):
				
				logger.info( "The goal IS MET.\n")
				
				#~ Set the current state as an ending state in the graph
				#~ Create a node in the planning graph
				planningGraph.setEndingVertex(state)
				
				goalFound = True
				
				continue
				
			logger.debug( "The goal is NOT met.")
			
			#~ Check if there are condition-action rules that can be applied to the state
			for caRules in self.__usableActions:
				rs = state.query(action.getUCQ())
				
				#~ Check if the query returns results
				if isinstance(rs, ResultSet):
					
					while rs.hasNext():
						
						#~ Save the result
						result = rs.next()
						
						#~ For each ground result of each action's precondition query,
						#~ transform it in a temporary DB and use it in the ECQ to tie
						#~ down the values of the variables
						
						#~ Apply the substitution pattern to the ECQ of each conditional effect
						for each conditionalEffect in action....
						
							#~ Execute the ECQ of the conditional effect and get the result set
							
							#~ Apply the result set to the effects of the conditional effect
							
							#~ Create a new state
							
							#~ Remove all deletion effects
							
							#~ Add all additional effects
							
							#~ Check if the new state is consistent
							
							#~ If consistent, add it to the states to be expanded
							#~ only if it wasn't already expanded before
							
							#~ Add to the planning graph the new state
							planningGraph.addVertex(newState)
							#~ Connect it with the previous one.
							planningGraph.addEdge(state, newState, action.getName() + "\\n" + str(substituionPattern))
							
						logger.debug( "\tState type: " + str(type(state)) + "\tState: " + str(state))
						logger.debug( "\tNew state type: " + str(type(newState)) + "\tNew state: " + str(newState))
						
			
			logger.debug( "\tStates to expand: " + str(len(statesToExpand)))
				
			#~ The algorythm ended well
		
		#~ I need to prune the planning graph, in order to remove all paths
		#~ that do not end in the goal state
		
		return True
		
	#~ Export the graph in DOT notation
	def exportGraphToDOT(self, filename="graph", directory = None):
		
		#~ fileName must be a valid string
		if not isinstance(filename, basestring):
			raise AttributeError("The name given is not a valid string."
		
		#~ Check that directory is a valid string and exists
		if not(
		isinstance(directory, basestring)
		and os.path.isdir(directory)
		):
			raise AttributeError("The directory given is not a valid string or directory."
			
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


#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------
#~ --------------------------------------------------------------------------------

import re
import string
import random
import itertools
import logging
import time
from collections import deque

from os import listdir
from os.path import isfile, join
import os
import sys
import fnmatch

#~ -------------------------------------------------------------------

		
	

	
class Variable:
	"""
	Class that represent a variable.
	Can be used in creating a query (both UCQ and ECQ)
	"""
	
	#~ Possible patterns for the name
	__name_pattern = r"""
		(
			[A-Z]+
			\w*
		)|(
			_
			\w+
		)""" # esempi: A, _A, __, _a, _9, _aA2, A9, A_a_3
	
	#~ To create a variable I have to specify a name
	#~ I could either pass a specific name (a string) or a set of names.
	#~ The set represent names that are not valid, so I generate a name
	#~ that is not present in the set
	def __init__(self, name):
		#~ Check if name is a string and has a valid pattern
		if isinstance(name, basestring) and re.match(("^"+self.__name_pattern+"$"), name, re.VERBOSE):
			#~ Save the name
			self.__name = name
		#~ Check if it is a list of strings
		elif isinstance(name, set) and all(isinstance(element, basestring) for element in name):
			#~ Generate a random name
			self.__name = self.__createName(name)
		else:
			raise AttributeError("The name given for the atom is not valid."
		
		
	
	def __eq__(self, other):
		if isinstance(other, Variable) and str(other) == self.__name:
			return True
		
		return False
	
	def __ne__(self, other):
		if isinstance(other, Variable) and str(other) == self.__name:
			return False
		
		return True
	
	def __repr__(self):
		return self.__name
	
	def __hash__(self):
		return hash(self.__name)
	
	#~ Generate a random name for the variable
	#~ If alreadyGivenName is an empty set, then it will simply generate a random name
	def __createName(self, alreadyGivenName, num_char = 5):
		
		#~ Check if num_char is a valid integer
		if not (isinstance(num_char, int) and num_char > 1): raise AttributeError("The number of characters given is not a valid integer > 1."
		
		
		#~ Generate a name that is not already in the set
		while True:
			name = '_' + ''.join(random.choice(string.ascii_letters) for x in range(num_char))
			
			if not (name in alreadyGivenName):
				#~ Found a valid name. Return it.
				return name
		


class Atom:
	"""
	Represent an atom that can be used in creating a query or an action.
	The atom can be of the types:
	1) (negated) N(z) (represented as: z, rdf:type, N, negated=True/False)
	2) (negated) P(z,z') (represented as: z, P, z', negated=True/False)
	3) x = y (represented as: x, "equal", y)
	4) create_instance
	
	where z,z' can be either variables or ground terms of the ABox,
	while x,y can be only ground terms of the ABox.
	"""
	
	atomTypes = ["concept","role","equality"]
	
	def __init__(self, *args, **kwargs):
		
		#~ Check if it is the case for (negated) N(z)
		if (
		(isinstance(args[0], Individual) or isinstance(args[0], Variable))
		and (isinstance(args[1], Property) and args[1].getURI() == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
		and isinstance(args[2], OntClass)
		):
			
			#~ Check if there is specified the argument "negate" and if it's value is True.
			#~ All other named arguments will be ignored.
			if "negate" in kwargs:
				if not isinstance(kwargs["negated"], bool):
					raise AttributeError("The attribute 'negated' passed is not a valid boolean."
				self.__negated = kwargs["negated"]
			else:
				self.__negated = False
			
			#~ Save all the elements
			self.__arguments = args
			
			#~ Save the type of Atom
			self.__atomType = self.atomTypes[0]
			
		
		#~ Check if it is the case for (negated) P(z,z')
		elif (
		(isinstance(args[0], Individual) or isinstance(args[0], Variable))
		and isinstance(args[1], OntProperty)
		and (isinstance(args[2], Individual) or isinstance(args[2], Variable))
		):
			#~ Check if there is specified the argument "negate" and if it's value is True.
			#~ All other named arguments will be ignored.
			if "negated" in kwargs:
				if not isinstance(kwargs["negated"], bool):
					raise AttributeError("The attribute 'negated' passed is not a valid boolean."
				self.__negated = kwargs["negated"]
			else:
				self.__negated = False
			
			#~ Save all the elements
			self.__arguments = args
			
			#~ Save the type of Atom
			self.__atomType = self.atomTypes[1]
		
		#~ Check if it is the case for x = y
		elif (
		isinstance(args[0], Individual)
		and (args[1] == "=")
		and (isinstance(args[2], Individual))
		):
			#~ Save all the elements
			self.__arguments = args
			
			#~ Save the type of Atom
			self.__atomType = self.atomTypes[2]
		
		#~ If there is no matching case, then I raise an error
		else:
			raise AttributeError("The attributes passed do not represent a valid atom."
			
	#~ Act as the negation of the term
	#~ Simply returns a new Compound term with the flag __not set to true
	#~ def __neg__(self):
		#~ return Atom(*self.__arguments, **{negate:(not self.__negate)})
	
	#~ Function to get access to the single elements of the atom __arguments
	def __getitem__(self,key):
		return self.__arguments[key]
	
	#~ Return the string representation of the atom
	#~ using SPARQL notation
	def __repr__(self):
		
		if self.__atomType == self.atomTypes[0]:
			#~ C(X) is translated in "?X a iri:C"
			#~ C(z) is translated in "iri:z a iri:C"
			#~ I don't consider the not at this stage
			termString = (("?"+str(self.__arguments[0])) if isinstance(self.__arguments[0], Variable) else  ":" + self.__arguments[0].getLocalName()) \
				+ " a " \
				+ ":" + self.__arguments[2].getLocalName()
			
				
		elif self.__atomType == self.atomTypes[1]:
			#~ P(X,Y) is translated in "?X iri:P ?Y"
			#~ P(z,w) is translated in "iri:z iri:P iri:w"
			#~ I don't consider the not at this stage
			termString = (("?"+str(self.__arguments[0])) if isinstance(self.__arguments[0], Variable) else  ":" +self.__arguments[0].getLocalName()) \
				+ " " \
				+  ":" +self.__arguments[1].getLocalName() + " " \
				+ (("?"+str(self.__arguments[2])) if isinstance(self.__arguments[2], Variable) else  ":" +self.__arguments[2].getLocalName())
			
			
		elif self.__atomType == self.atomTypes[2]:
			pass
			
		else:
			pass
			
		return termString
		
	def __hash__(self):
		return hash(self.__repr__())
	
	#~ Returns True if the term is negated
	def isNegated(self):
		return self.__negated
		
	#~ Returns the type of the Atom
	def atomType(self):
		return self.__atomType
		
	#~ Returns all the variables used in the term
	def variables(self):
		
		variablesList = []
		for element in self.__arguments:
			if isinstance(element, Variable):
				variablesList.append(element)
			
		return variablesList
	
	#~ 
	def substitution(self, **kwargs):
		#~ Create a list of arguments
		#~ If the argument of the atom matches a substitution, then
		#~ substitute with the specified element
		new_args = [(kwargs[str(arg)] if str(arg) in kwargs else arg) for arg in self.__arguments]
		
		#~ Return a new atom with the new set of arguments
		return Atom(*new_args, **{"negated":self.__negated})
	
	#~ Compare two Atoms and check if otherAtom is more general than self.
	#~ Examples:
	#~ 	C(a) < C(X)
	#~ 	P(a,b) < P(X,b) < P(X,Y)
	#~ 	P(a,b) < P(a,Y) < P(X,Y)
	#~ 	P(a,a) < P(a,X) < P(X,X) < P(X,Y)
	def __ge__(self, otherAtom):
		
		#~ Check that otherAtom is a valid Atom
		if not isinstance(otherAtom, Atom):
			return False
			
		#~ The atom must be of the same type of atom
		if self.__atomType != otherAtom.__atomType:
			return False
		
		#~ Then I check for every type of atom if they are compatible
		if self.__atomType == self.atomTypes[0]:
			#~ The concept must be the same
			if self.__arguments[0] != otherAtom[0]:
				return False
			
			#~ Check if self contains an instance and other the same one
			#~ or a variable
			if isinstance(self.__arguments[2], Individual):
				
				if isinstance(otherAtom[2], Individual) and self.__arguments[2] == otherAtom[2]:
					#~ C(a) >= C(a)
					return True
				else:
					#~ C(a) >= C(X) or C(a) >= C(?)
					return False
				
			elif isinstance(self.__arguments[2], Variable):
				
				if isinstance(otherAtom[2], Individual):
					#~ C(X) >= C(a)
					return True
				elif isinstance(otherAtom[2], Variable):
					#~ C(X) >= C(Y)
					return True
				else:
					#~ C(X) >= C(?)
					return False
			else:
				return False
		
		elif self.__atomType == self.atomTypes[1]:
			#~ The role must be the same
			if self.__arguments[1] != otherAtom[1]:
				return False
			
			#~ Check if self contains instances and other the same ones
			#~ or variables
			if isinstance(self.__arguments[0], Individual) and isinstance(self.__arguments[2], Individual):
				#~ P(a,b)
				
				if (
				isinstance(otherAtom[0], Individual)
				and self.__arguments[0] == otherAtom[0]
				and isinstance(otherAtom[2], Individual)
				and self.__arguments[2] == otherAtom[2]
				):
					#~ P(a,b) >= P(a,b)
					return True
				else:
					#~ P(a,b) >= P(X,b) or P(a,b) >= P(a,Y) or P(a,b) >= P(X,Y)
					return False
				
			elif isinstance(self.__arguments[0], Individual) and isinstance(self.__arguments[2], Variable):
				#~ P(a,X)
				
				#~ The only case that is not ok is when other is of the
				#~ type P(b,_) and P(X,_)
				if (
				(isinstance(otherAtom[0], Individual) and self.__arguments[0] != otherAtom[0])
				or isinstance(otherAtom[2], Variable)
				):
					return False
				else:
					return True
			elif isinstance(self.__arguments[0], Variable) and isinstance(self.__arguments[2], Individual):
				#~ P(X,b)
				
				#~ The only case that is not ok is when other is of the
				#~ type P(_,a) and P(_,Y)
				if (
				(isinstance(otherAtom[2], Individual) and self.__arguments[2] != otherAtom[2])
				or isinstance(otherAtom[0], Variable)
				):
					return False
				else:
					return True
			elif isinstance(self.__arguments[0], Variable) and self.__arguments[0] == self.__arguments[2]:
				#~ P(X,X)
				
				#~ The only case that is not ok is when other is
				#~ P(a,b) (with a!=b) and P(X,Y)
				if otherAtom[0] != otherAtom[2]:
					return False
				else:
					return True
			else:
				#~ P(X,Y)
				return True
		else:
			return False
	
	
	def __le__(self, otherAtom):
		
		#~ Check that otherAtom is a valid Atom
		if not isinstance(otherAtom, Atom):
			return False
			
		#~ The atom must be of the same type of atom
		if self.__atomType != otherAtom.__atomType:
			return False
		
		#~ Then I check for every type of atom if they are compatible
		if self.__atomType == self.atomTypes[0]:
			#~ The concept must be the same
			if self.__arguments[0] != otherAtom[0]:
				return False
			
			#~ Check if self contains an instance and other the same one
			#~ or a variable
			if isinstance(self.__arguments[2], Individual):
				#~ C(a)
				
				#~ The only case which is not ok is when other is
				#~ C(b)
				if isinstance(otherAtom[2], Individual) and self.__arguments[2] != otherAtom[2]:
					#~ C(a) <= C(b)
					return False
				else:
					#~ C(a) <= C(X) or C(a) <= C(a)
					return True
				
			elif isinstance(self.__arguments[2], Variable):
				#~ C(X)
				#~ It's True only when other is C(Y)
				if isinstance(otherAtom[0], Variable):
					#~ C(X) <= C(Y)
					return True
				else:
					return False
				
			else:
				return False
		
		elif self.__atomType == self.atomTypes[1]:
			#~ The role must be the same
			if self.__arguments[1] != otherAtom[1]:
				return False
			
			#~ Check if self contains instances and other the same ones
			#~ or variables
			if isinstance(self.__arguments[0], Individual) and isinstance(self.__arguments[2], Individual):
				#~ P(a,b)
				
				#~ The only case that is not ok is when other is P(c,_)
				#~ or P(_,d)
				if (
				(isinstance(otherAtom[0], Individual) and self.__arguments[0] != otherAtom[0])
				or (isinstance(otherAtom[2], Individual) and self.__arguments[2] != otherAtom[2])
				):
					return False
				else:
					#~ P(a,b) <= P(a,b) or P(a,b) <= P(X,b) or P(a,b) <= P(a,Y) or P(a,b) <= P(X,Y)
					return True
				
			elif isinstance(self.__arguments[0], Individual) and isinstance(self.__arguments[2], Variable):
				#~ P(a,X)
				
				#~ The only case that are ok is when other is one of the
				#~ type P(a,X) or P(Y,X)
				#~ P(X,X) is not valid
				if (
				(isinstance(otherAtom[0], Individual) and self.__arguments[0] == otherAtom[0] and isinstance(otherAtom[2], Variable))
				or (isinstance(otherAtom[0], Variable) and isinstance(otherAtom[2], Variable) and otherAtom[0] != otherAtom[2])
				):
					return True
				else:
					return False
			elif isinstance(self.__arguments[0], Variable) and isinstance(self.__arguments[2], Individual):
				#~ P(X,b)
				
				#~ The only case that are ok is when other is one of the
				#~ type P(X,b) or P(X,Y)
				#~ P(X,X) is not valid
				if (
				(isinstance(otherAtom[2], Individual) and self.__arguments[2] == otherAtom[2] and isinstance(otherAtom[0], Variable))
				or (isinstance(otherAtom[0], Variable) and isinstance(otherAtom[2], Variable) and otherAtom[0] != otherAtom[2])
				):
					return True
				else:
					return False
			elif isinstance(self.__arguments[0], Variable) and self.__arguments[0] == self.__arguments[2]:
				#~ P(X,X)
				
				#~ The only cases that are ok is when other is
				#~ P(X,X) or P(X,Y)
				if isinstance(otherAtom[0], Variable) and isinstance(otherAtom[2], Variable):
					return True
				else:
					return False
			else:
				#~ P(X,Y)
				
				#~ The only cases that are ok is when other is
				#~ P(X,Y)
				if isinstance(otherAtom[0], Variable) and isinstance(otherAtom[2], Variable) and otherAtom[0] != otherAtom[2]:
					return True
				else:
					return False
		else:
			return False
		
	


#~ Set the logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
#~ logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler('example.log', mode='w')
handler.setLevel(logging.WARNING)
#~ handler.setLevel(logging.DEBUG)

# create a logging format
#~ formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#~ handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


#~ logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
		

if __name__ == "__main__":
	
	kbDirectory = "TestSuite"
	for kbFile in listdir(kbDirectory):
		if fnmatch.fnmatch(kbFile, '*.ttl'):
			
			print "Analyze: " + kbFile
			
			#~ kb = "minimal_example.ttl"
			kb_NS = "http://example.com/minimal-example#"
			rdf_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
			
			#~ IMPORTANT: The option to enable tracing should be turned
			#~ on before the ontology is loaded to the reasoner!
			PelletOptions.USE_TRACING = True
			
			#~ KB must be the path for a valid file
			#~ create an empty non-inferencing model
			rawModel = ModelFactory.createOntologyModel( OntModelSpec.OWL_MEM )

			#~ create Pellet reasoner
			pelletReasoner = PelletReasonerFactory.theInstance().create()

			#~ create an inferencing model using Pellet reasoner
			#~ model = ModelFactory.createInfModel(pelletReasoner, rawModel)
			model = ModelFactory.createOntologyModel( OntModelSpec.OWL_MEM )
			#~ Then read the data from the file into the ontology model
			model.read( os.path.join(kbDirectory,kbFile) )
			
			
			X = Variable("X")
			Y = Variable("Y")
			Z = Variable("Z")
			
			planner = Planner(os.path.join(kbDirectory,kbFile))
			
			action_appoint = Action(
				"appoint",
				UnionConjunctiveQueries(
					Atom(X, model.getResource(rdf_NS + "type").as(Property), model.getResource(kb_NS + "Manager").as(OntClass)), # Manager(X)
					Atom(X, model.getResource(kb_NS + "canAppoint").as(ObjectProperty), Y), # CAN_APPOINT(X,Y)
					Atom(Y, model.getResource(kb_NS + "canManage").as(ObjectProperty), Z), # CAN_MANAGE(Y,Z)
					freeVars = [X,Y,Z]
				), # UCQ
				None, # ECQ
				[
					["add", Atom(Y, model.getResource(kb_NS + "Manage").as(ObjectProperty), Z)]
				]
				)
			
			action_review = Action(
				"review",
				UnionConjunctiveQueries(
					Atom(X, model.getResource(rdf_NS + "type").as(Property), model.getResource(kb_NS + "Technician").as(OntClass)), # Technician(X)
					Atom(Y, model.getResource(rdf_NS + "type").as(Property), model.getResource(kb_NS + "TechnicalDoc").as(OntClass)), # TechnicalDoc(Y)
					Atom(X, model.getResource(kb_NS + "TecManage").as(ObjectProperty), Y), # TEC_MANAGE(X,Y)
					freeVars = [X,Y]
				), # UCQ
				None, # ECQ
				[
					["add", Atom(Y, model.getResource(kb_NS + "hasStatus").as(ObjectProperty), model.getResource(kb_NS + "reviewed").as(Individual))]
				]
				)
			
			planner.addAction(action_appoint)
			planner.addAction(action_review)
			
			goal_atom= Atom(model.getResource(kb_NS + "doc01").as(Individual), model.getResource(kb_NS + "hasStatus").as(ObjectProperty), model.getResource(kb_NS + "reviewed").as(Individual))
			planner.defineGoal(UnionConjunctiveQueries(goal_atom))
			
			#~ Measure the time it takes to create the graph
			start = time.clock()
			graph = planner.findPlanningGraph()
			elapsed = (time.clock() - start)
			
			planner.exportGraphToDOT(filename = (kbFile+str(elapsed)), directory = kbDirectory)
			
			print "Execution Time: " + str(elapsed) + " sec"
	


