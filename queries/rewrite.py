from pyparsing import *
import itertools
import os
import copy
import logging

#~ Local libraries
from syntax.syntax import Syntax
from queries.cq import *
from queries.ucq import UCQ
from queries.ecq import ECQ

def rewrite(query, posAxioms, conceptList, roleList, individualList):
	#~ Function that takes as input a query, a list of positive axioms
	#~ and calculates the rewritten query by following the algorithm
	#~ PerfectRef
	
	def __rewriteECQ(query, posAxioms):
		#~ Possible ECQs:
		#~ - True
		#~ - ["not", ECQ]
		#~ - ["exists", [vars], ECQ]
		#~ - ["and", ECQ, ... , ECQ]
		#~ - ["mko-eq", var1, var2]
		#~ - ["mko", UCQ]
		
		if not isinstance(query, ECQ):
			raise Exception("The function __rewriteECQ can work only with objects of the class ECQ(). It was instead passed a " + str(type(query)))
		
		syntax = Syntax()
		
		if query.isTrue():
			#~ Return the keyword True
			return [syntax.true]
		
		elif query.isNegated():
			#~ ["not", ECQ]
			if len(query.ecqs()) != 1:
				raise Exception("Something is wrong. A negated ECQ (\"(not ECQ)\") can contain only one internal ECQ, while here there are " + len(query.ecqs()) + ".")
			
			for ecq in query.ecqs():
				return [syntax.neg, __rewriteECQ(ecq, posAxioms)]
		
		elif len(query.existentialVars()) > 0:
			#~ ["exists", [vars], ECQ]
			
			if len(query.ecqs()) != 1:
				raise Exception("Something is wrong. An existential ECQ (\"(exists (vars) ECQ)\") can contain only a list of existential variables, and one internal ECQ")
			
			for ecq in query.ecqs():
				return [syntax.exists, [str(var) for var in query.existentialVars()], __rewriteECQ(ecq, posAxioms)]
		
		elif len(query.ecqs()) > 0:
			#~ ["and", ECQ, ... , ECQ]
			rewrittenEcq = [syntax.queryAnd]
			
			for ecq in query.ecqs():
				rewrittenEcq.append(__rewriteECQ(ecq, posAxioms))
			
			return rewrittenEcq
		
		elif isinstance(query.equalityVar1(), Variable) and isinstance(query.equalityVar2(), Variable):
			#~ ["mko-eq", var1, var2]
			
			eqEcq = [syntax.mkoEq,str(query.equalityVar1()),str(query.equalityVar2())]
				
			return eqEcq
		
		elif not query.ucq() is None:
			#~ ["mko", UCQ]
			return [syntax.mko, __rewriteUCQ(query.ucq(), posAxioms)]
		
		else:
			#~ If I reach this point, something went wrong
			raise Exception("Something went wrong in the query rewriting of the query:\n" + str(self))
	
	def __rewriteUCQ(query, posAxioms):
		
		if not isinstance(query, UCQ):
			raise Exception("The function __rewriteUCQ can work only with objects of the class UCQ(). It was instead passed a " + str(type(query)))
		
		#~ Algorithm PerfectRef(q, T)
		#~ Input: UCQ q, DL-LiteA TBox T
		#~ Output: UCQ pr
		#~ 
		#~ pr := q;
		#~ repeat 
			#~ pr' := pr;
			#~ for each CQ q' ∈ pr' do
				#~ for each atom g in q' do
					#~ for each PI α in T do
						#~ if α is applicable to g then
							#~ pr := pr ∪{q?[g/gr(g,α)] };
							#~ 
				#~ for each pair of atoms g1,g2 in q? do
					#~ if g1 and g2 unify then
						#~ pr := pr ∪ {anon(reduce(q?,g1,g2))};
		#~ until pr' = pr;
		#~ return pr
		
		syntax = Syntax()
		
		#~ Implement the line:
			#~ pr := q;
		rewrittenUCQ = set(query.cqs())
		#~ for cq in query.cqs():
			#~ rewrittenUCQ.add(cq)
		
		#~ Implement the line:
			#~ repeat
		while True:
			
			#~ Implement the line:
				#~ pr' := pr;
			rewrittenUCQold = set(rewrittenUCQ)
			#~ for cq in rewrittenUCQ:
				#~ rewrittenUCQold.add(cq)
				
			#~ Implement the line:
				#~ for each CQ q' ∈ pr' do
			for cq in rewrittenUCQold:
				
				#~ Implement the line:
				#~ for each atom g in q' do
					#~ for each PI α in T do
				for (atom, axiom) in itertools.product(cq.queryAtoms(), posAxioms):
					
					#~ print("Checking axiom: " + str(axiom))
						
					#~ Implement the line:
						#~ if α is applicable to g then
							#~ pr := pr ∪{q'[g/gr(g,α)] };
					newAtom = __applyAxiom(atom, axiom)
					
					if not newAtom is None:
						#~ Calculate q'[g/gr(g,α)]
						newAtoms = [] # The atoms that compose the rewritten cq
						for atomTemp in cq.queryAtoms(): # We copy all the query atoms, and just substitute the rewritten one
							if atomTemp == atom: # We check if it is the atom that was rewritten
								newAtoms.append(newAtom) # We add the rewritten atom
							else:
								newAtoms.append(atomTemp)
						
						logger.info("for axiom in posAxioms:")
						logger.info(str(cq))
						logger.info(str(cq.queryAtoms()))
						logger.info(str(atom))
						logger.info(str(axiom))
						logger.info(str(newAtom))
						logger.info(str(newAtoms))
						logger.info(" ")
						
						#~ If the __applyAxiom function added a NDNSVariable() to newAtom,
						#~ then we have to add it to the existential variables of the rewritten CQ
						ndnsVar = NDNSVariable()
						if ndnsVar in newAtom.freeVars():
							newExistentialVars = set([ndnsVar])
							if len(cq.existentialVars()) > 0:
								newExistentialVars.update(cq.existentialVars())
							
							rewrittenUCQ.add(CQ({"queryAtoms":newAtoms, "existentialVars":newExistentialVars}, conceptList, roleList, individualList))
							
						else:
							
							#~ Calculate the new existential vars set, because it could be the case that we
							#~ substitute a role with a concept, in which case we may reduce the number of 
							#~ existential vars.
							#~ Example:
							 #~ - we start with (exists ( ?_ ?x_1 ) (and (hasPersonalInfo ?x_1 ?_) (FullName ?x_1) ) )
							 #~ - we apply the axiom (isA Employee (exists hasPersonalInfo))
							 #~ - we substitute (hasPersonalInfo ?x_1 ?_) with (Employee ?x_1)
							 #~ - ?_ is not an existential var anymore
							newExistentialVars = set()
							for var in cq.existentialVars():
								for atom in newAtoms:
									if var in atom.freeVars():
										newExistentialVars.add(var)
							
							rewrittenUCQ.add(CQ({"queryAtoms":newAtoms, "existentialVars":newExistentialVars}, conceptList, roleList, individualList))
						
				#~ Implement the line: for each pair of atoms g1,g2 in q' do
				for (atom1, atom2) in itertools.combinations(cq.queryAtoms(),2):
					
					#~ Implement the line:
					#~ if g1 and g2 unify then
						#~ pr := pr ∪{anon(reduce(q',g1,g2))};	
					newCQ = __anon(__reduce(cq, atom1, atom2), cq.freeVars())
					
					#~ print("Old CQ: " + str(cq))
					#~ print("New CQ: " + str(newCQ))
					
					if not newCQ is None:
						rewrittenUCQ.add(newCQ)
						

			logger.info("rewrittenUCQ:")
			logger.info(rewrittenUCQ)
			logger.info(" ")
					
			#~ Implement the line:
				#~ until pr' = pr;
			if rewrittenUCQold == rewrittenUCQ:
				break
		
		#~ We have to substitutes each instance of NDNSVariable()
		#~ with a proper variable Variable().
		#~ NDNSVariable() instances can appear only in the CQs which
		#~ have existential variables.
		rewrittenUCQ_wo_NDNSVariables = set()
		for cq in rewrittenUCQ:
			if any([isinstance(var,NDNSVariable) for var in cq.existentialVars()]):
				
				cq_wo_NDNSVariables_existentialVars = set() # Temporary set in which the vars that substitute the NDNSVariable are saved
				cq_wo_NDNSVariables = set() # Temporary set in which we save the query atoms that contain the changed NDNSVariables
				counter = 0 # Used to generate uniquely named variables
				
				#~ Check if among the query atoms the NDNSVariable is used
				for queryAtom in cq.queryAtoms():
					
					newVar1 = None
					newVar2 = None
					
					if isinstance(queryAtom.var1(), NDNSVariable):
						#~ We need to change it.
						
						#~ Create a uniquely named variable
						newVar1 = Variable(syntax.ndnsVariable + str(counter))
						#~ Increase the counter
						counter += 1
						
						#~ Save the new variable in the set substituteVars
						cq_wo_NDNSVariables_existentialVars.add(newVar1)
					else:
						newVar1 = queryAtom.var1()
					
					if isinstance(queryAtom.var2(), NDNSVariable):
						#~ We need to change it.
						
						#~ Create a uniquely named variable
						newVar2 = Variable(syntax.ndnsVariable + str(counter))
						#~ Increase the counter
						counter += 1
						
						#~ Save the new variable in the set substituteVars
						cq_wo_NDNSVariables_existentialVars.add(newVar2)
					
					else:
						newVar2 = queryAtom.var2()
							
					#~ Create a new queryAtom where the NDNSVariable is
					#~ changed with the new one, and save it in cqs_wo_NDNSVariables.
					if newVar2 is None:
						cq_wo_NDNSVariables.add(QueryAtom([queryAtom.term(), newVar1], conceptList, roleList, individualList))			
					else:
						cq_wo_NDNSVariables.add(QueryAtom([queryAtom.term(), newVar1, newVar2], conceptList, roleList, individualList))
				
				#~ Update cq_wo_NDNSVariables_existentialVars by adding other
				#~ existential vars, but not NDNSVariable.
				for var in cq.existentialVars():
					if not isinstance(var, NDNSVariable):
						cq_wo_NDNSVariables_existentialVars.add(var)
				
				#~ Save the cq in rewrittenUCQ_wo_NDNSVariables
				rewrittenUCQ_wo_NDNSVariables.add(CQ({"queryAtoms":cq_wo_NDNSVariables, "existentialVars":cq_wo_NDNSVariables_existentialVars}, conceptList, roleList, individualList))
				
			else:
				#~ The cq doesn't use any NDNSVariable. We copy it in rewrittenUCQ_wo_NDNSVariables
				rewrittenUCQ_wo_NDNSVariables.add(cq)
				
		#~ Implement the line:
			#~ return pr
		rewrittenUCQ = list(rewrittenUCQ_wo_NDNSVariables)
		if len(rewrittenUCQ) > 1:
			rewrittenUCQ.insert(0, syntax.queryOr)
		
		#~ print("Fine __rewriteUCQ")
		#~ print(str(list(rewrittenUCQ)))
		#~ print("---------------------------\n")
		
		return rewrittenUCQ
	
	
	def __applyAxiom(queryAtom, axiom):
		"""
		The function checks if, given a query atom and axiom,
		we can apply the axiom and thus genereate a new "rewritten" query atom.
		We follow the table reported in Fig. 12 of [Calvanese2009].
		The table is:
		
		Atom g	| Axiom alpha					| gr(g, alpha)
		--------|-------------------------------|----------------
		A(x)	| A1 isA A						| A1(x)
		A(x)	| exists P isA A				| P(x,_)
		A(x)	| exists P^- isA A				| P(_,x)
		P(x,_)	| A isA exists P				| A(x)
		P(x,_)	| exists P1 isA exists P		| P1(x,_)
		P(x,_)	| exists P1^- isA exists P		| P1(_,x)
		P(_,y)	| A isA exists P^-				| A(y)
		P(_,y)	| exists P1 isA exists P^-		| P1(y,_)
		P(_,y)	| exists P1^- isA exists P^-	| P1(_,y)
		P(x,y)	| P1 isA P , P1^- isA P^-		| P1(x,y)
		P(x,y)	| P1 isA P^- , P1^- isA P		| P1(y,x)
		"""
		
		syntax = Syntax()
		
		#~ Check if the axiom involves, in the right side, the term used in the atom
		if queryAtom.term() == axiom.rightTerm():
			
			if not axiom.leftTermExists() and \
				not axiom.leftTermInverse() and \
				not axiom.rightTermExists() and \
				not axiom.rightTermInverse() and \
				not isinstance(queryAtom.var1(), NDNSVariable):
				#~ We have one of the following situations:
				#~ A1 isA A
				#~ P1 isA P
			
				if queryAtom.var2() is None:
					#~ Return A1(x)
					return QueryAtom([axiom.leftTerm(), queryAtom.var1()], conceptList, roleList, individualList)
				elif isinstance(queryAtom.var2(), Variable):
					#~ Return P1(x,y)
					return QueryAtom([axiom.leftTerm(), queryAtom.var1(), queryAtom.var2()], conceptList, roleList, individualList)
			
			elif axiom.leftTermExists() and \
				not axiom.leftTermInverse() and \
				not axiom.rightTermExists() and \
				not axiom.rightTermInverse() and \
				not isinstance(queryAtom.var1(), NDNSVariable):
				#~ We have the following situations:
				#~ exists P isA A
				#~ Return P(x,_)
				return QueryAtom([axiom.leftTerm(), queryAtom.var1(), NDNSVariable()], conceptList, roleList, individualList)
			
			elif axiom.leftTermExists() and \
				axiom.leftTermInverse() and \
				not axiom.rightTermExists() and \
				not axiom.rightTermInverse() and \
				not isinstance(queryAtom.var1(), NDNSVariable):
				#~ We have the following situations:
				#~ exists P^- isA A
				#~ Return P(_,x)
				return QueryAtom([axiom.leftTerm(), NDNSVariable(), queryAtom.var1()], conceptList, roleList, individualList)
			
			elif not axiom.leftTermExists() and \
				not axiom.leftTermInverse() and \
				axiom.rightTermExists() and \
				not axiom.rightTermInverse() and \
				not isinstance(queryAtom.var1(), NDNSVariable) and \
				isinstance(queryAtom.var2(), NDNSVariable):
				#~ We have the following situations:
				#~ A isA exists P
				#~ Return A(x)
				return QueryAtom([axiom.leftTerm(), queryAtom.var1()], conceptList, roleList, individualList)
			
			elif not axiom.leftTermExists() and \
				not axiom.leftTermInverse() and \
				axiom.rightTermExists() and \
				axiom.rightTermInverse() and \
				not isinstance(queryAtom.var2(), NDNSVariable) and \
				isinstance(queryAtom.var1(), NDNSVariable):
				#~ We have the following situations:
				#~ A isA exists P^-
				#~ Return A(y)
				return QueryAtom([axiom.leftTerm(), queryAtom.var2()], conceptList, roleList, individualList)
			
			elif axiom.leftTermExists() and \
				not axiom.leftTermInverse() and \
				axiom.rightTermExists() and \
				not axiom.rightTermInverse() and \
				not isinstance(queryAtom.var1(), NDNSVariable) and \
				isinstance(queryAtom.var2(), NDNSVariable):
				#~ We have the following situations:
				#~ exists P1 isA exists P
				#~ Return P1(x,_)
				return QueryAtom([axiom.leftTerm(), queryAtom.var1(), NDNSVariable()], conceptList, roleList, individualList)
			
			elif axiom.leftTermExists() and \
				axiom.leftTermInverse() and \
				axiom.rightTermExists() and \
				not axiom.rightTermInverse() and \
				not isinstance(queryAtom.var1(), NDNSVariable) and \
				isinstance(queryAtom.var2(), NDNSVariable):
				#~ We have the following situations:
				#~ exists P1^- isA exists P
				#~ Return P1(_,x)
				return QueryAtom([axiom.leftTerm(), NDNSVariable(), queryAtom.var1()], conceptList, roleList, individualList)
			
			elif axiom.leftTermExists() and \
				not axiom.leftTermInverse() and \
				axiom.rightTermExists() and \
				axiom.rightTermInverse() and \
				not isinstance(queryAtom.var2(), NDNSVariable) and \
				isinstance(queryAtom.var1(), NDNSVariable):
				#~ We have the following situations:
				#~ exists P1 isA exists P^-
				#~ Return P1(y,_)
				
				return QueryAtom([axiom.leftTerm(), queryAtom.var2(), NDNSVariable()], conceptList, roleList, individualList)
			
			elif axiom.leftTermExists() and \
				axiom.leftTermInverse() and \
				axiom.rightTermExists() and \
				axiom.rightTermInverse() and \
				not isinstance(queryAtom.var2(), NDNSVariable) and \
				isinstance(queryAtom.var1(), NDNSVariable):
				#~ We have the following situations:
				#~ exists P1^- isA exists P^-
				#~ Return P1(_,y)
				return QueryAtom([axiom.leftTerm(), NDNSVariable(), queryAtom.var2()], conceptList, roleList, individualList)
			
			elif not axiom.leftTermExists() and \
				axiom.leftTermInverse() and \
				not axiom.rightTermExists() and \
				axiom.rightTermInverse() and \
				not isinstance(queryAtom.var1(), NDNSVariable) and \
				not isinstance(queryAtom.var2(), NDNSVariable):
				#~ We have the following situations:
				#~ P1^- isA P^-
				#~ Return P1(x,y)
				return QueryAtom([axiom.leftTerm(), queryAtom.var1(), queryAtom.var2()], conceptList, roleList, individualList)
			
			elif not axiom.leftTermExists() and \
				not axiom.leftTermInverse() and \
				not axiom.rightTermExists() and \
				axiom.rightTermInverse() and \
				not isinstance(queryAtom.var1(), NDNSVariable) and \
				not isinstance(queryAtom.var2(), NDNSVariable):
				#~ We have the following situations:
				#~ P1 isA P^-
				#~ Return P1(y,x)
				return QueryAtom([axiom.leftTerm(), queryAtom.var2(), queryAtom.var1()], conceptList, roleList, individualList)
			
			elif not axiom.leftTermExists() and \
				axiom.leftTermInverse() and \
				not axiom.rightTermExists() and \
				not axiom.rightTermInverse() and \
				not isinstance(queryAtom.var1(), NDNSVariable) and \
				not isinstance(queryAtom.var2(), NDNSVariable):
				#~ We have the following situations:
				#~ P1^- isA P
				#~ Return P1(y,x)
				return QueryAtom([axiom.leftTerm(), queryAtom.var2(), queryAtom.var1()], conceptList, roleList, individualList)
			#~ else:
				#~ Something is wrong
				#~ raise Exception("Something went wrong analyzing the axiom " + str(axiom))
			
		#~ If the code reach this point, it means the axiom couldn't be applied
		return None
		
	def __reduce(cq, atom1, atom2):
		#~ __reduce is a function that takes as input a CQ cq and two atoms atom1 and atom2
		#~ occurring in the body of cq, and returns a CQ newCq obtained by applying to cq
		#~ the most general unifier between atom1 and atom2.
		#~ The function __reduce takes two query atoms and tries
		#~ to apply a most general unifier to their variables.
		#~ If the atoms are about the same term, the most general
		#~ unifier substitutes each NDNSVariable in atom1 with the corresponding
		#~ argument in atom2, and vice-versa (obviously, if both arguments are a 
		#~ NDNSVariable, the resulting argument is a NDNSVariable).
		
		
		
		if atom1.term() == atom2.term():
			
			newCQAtoms = []
			
			newVar1 = None # Variable/constant 1 for the reduced atom
			if isinstance(atom1.var1(), NDNSVariable) and not isinstance(atom2.var1(), NDNSVariable):
				newVar1 = atom2.var1()
			
			elif not isinstance(atom1.var1(), NDNSVariable) and isinstance(atom2.var1(), NDNSVariable):
				newVar1 = atom1.var1()
				
			elif isinstance(atom1.var1(), Variable) and isinstance(atom2.var1(), Constant):
				newVar1 = atom2.var1()
				
			elif isinstance(atom1.var1(), Constant) and isinstance(atom2.var1(), Variable):
				newVar1 = atom1.var1()
				
			else:
				#~ The two variables/constants can't be unified, thus no unification is possible.
				#~ We return None.
				return None
				#~ raise Exception("The first variables/constants of these atoms can't be unified.\nAtom 1: " + str(atom1) + "\nAtom 2: " + str(atom2))
			
			newVar2 = None # Variable/constant 2 for the reduced atom
			if not atom1.var2() is None and not atom2.var2() is None:
				#~ Both var2() are not None, thus the term is a role.
				
				if isinstance(atom1.var2(), NDNSVariable) and not isinstance(atom2.var2(), NDNSVariable):
					newVar2 = atom2.var2()
				
				elif not isinstance(atom1.var2(), NDNSVariable) and isinstance(atom2.var2(), NDNSVariable):
					newVar2 = atom1.var2()
					
				elif isinstance(atom1.var2(), Variable) and isinstance(atom2.var2(), Constant):
					newVar2 = atom2.var2()
					
				elif isinstance(atom1.var2(), Constant) and isinstance(atom2.var2(), Variable):
					newVar2 = atom1.var2()
					
				else:
					#~ The two variables/constants can't be unified, thus no unification is possible.
					#~ We return None.
					return None
					#~ raise Exception("The second variables/constants of these atoms can't be unified.\nAtom 1: " + str(atom1) + "\nAtom 2: " + str(atom2))
				
				#~ Return the list of atoms, where we substitute atom1 and atom2 with the reduced atom.
				for atom in cq.queryAtoms():
					if atom != atom1 and atom != atom2:
						newCQAtoms.append(atom)
				
				#~ Append the reduced atom
				newCQAtoms.append(QueryAtom([atom1.term(), newVar1, newVar2], conceptList, roleList, individualList))
				
			elif not (atom1.var2() is None and atom2.var2() is None):
				#~ One of the two variable/costant is None, while the other is not.
				#~ This can't be, because it would mean the term is used as a concept
				#~ in one query atom, and as a role in the other.
				raise Exception("The term " + str(atom1.term()) + " is used both as a concept and a role in the following atoms.\nAtom 1: " + \
							str(atom1) + "\nAtom 2: " + str(atom2))
			
			else:
				#~ Both var2() are None, thus the term is a concept.
				#~ Return the new query with the reduced atom.
				
				#~ Return the list of atoms, where we substitute atom1 and atom2 with the reduced atom.
				
				for atom in cq.queryAtoms():
					if atom != atom1 and atom != atom2:
						newCQAtoms.append(atom)
				
				#~ Append the reduced atom
				newCQAtoms.append(QueryAtom([atom1.term(), newVar1], conceptList, roleList, individualList))
				
			
			logger.info("__reduce:")
			logger.info(cq)
			logger.info(atom1)
			logger.info(atom2)
			logger.info(newCQAtoms)
			logger.info(" ")
			
			return newCQAtoms
			
		#~ Reaching this point means the two atoms are about different terms, thus no unification
		#~ was necessary. We return None.
		return None
			
	def __anon(queryAtomsList, freeVars):
		#~ anon is a function that takes as input a CQ cq and returns a new CQ 
		#~ obtained by replacing each occurrence of an unbound variable in cq with
		#~ a NDNSVariable.
		#~ The input is not a real instance of CQ(), but a list of query atoms coming
		#~ form the function __reduce(), and the list of free variables appearing in the
		#~ original cq.
		
		if queryAtomsList is None:
			return None
		
		newCQAtoms = []
		newVar1 = None
		newVar2 = None
		substitutionOfUnboundVariable = list() # boolean flag that tells if an existential var has been substitued
		
		for atom in queryAtomsList:
			
			if atom.var1() not in freeVars and not isinstance(atom.var1(), NDNSVariable):
				#~ We have an unbound variable, we need to substitute it
				newVar1 = NDNSVariable()
				substitutionOfUnboundVariable.append(newVar1)
			else:
				newVar1 = atom.var1()
			
			if atom.var2() is not None:
				if atom.var2() not in freeVars and not isinstance(atom.var2(), NDNSVariable):
					#~ We have an unbound variable, we need to substitute it
					newVar2 = NDNSVariable()
					substitutionOfUnboundVariable.append(newVar2)
				else:
					newVar2 = atom.var2()
				
				#~ Create a new atom with the new variables/constants
				newCQAtoms.append(QueryAtom([atom.term(), newVar1, newVar2], conceptList, roleList, individualList))
				
			else:
				#~ Create a new atom with the new variables/constants
				newCQAtoms.append(QueryAtom([atom.term(), newVar1], conceptList, roleList, individualList))
		
		logger.info("__anon:")
		logger.info(queryAtomsList)
		logger.info(freeVars)
		logger.info(newCQAtoms)
		logger.info(" ")
		
		#~ Create a new CQ with the new atoms
		if len(substitutionOfUnboundVariable) > 0:
			#~ Since we substituted every unbound variable with a NDNSVariable,
			#~ the existential vars set will contain only a NDNSVariable.
			return CQ({"queryAtoms":newCQAtoms, "existentialVars":substitutionOfUnboundVariable}, conceptList, roleList, individualList)
		else:
			#~ No existential vars where substitued, so it means that there are none of them.
			return CQ({"queryAtoms":newCQAtoms}, conceptList, roleList, individualList)
				
	#~ ------------------------------------
	#~ ------------------------------------
	#~ ------------------------------------
	#~ Principal function that calls the various sub functions for the rewriting of the queries
	#~ ------------------------------------
	#~ ------------------------------------
	#~ ------------------------------------
	
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
	
	if not isinstance(query, (ECQ,UCQ,CQ)):
		raise Exception("The query provided is not a valid one.")
	
	logger = logging.getLogger("sqlPlanner")
	logger.info("-"*30)
	logger.info("rewrite()")
	logger.info("query:")
	logger.info(str(query))
	logger.info("-"*30)
		
	rewrittenQuery = []
	
	if isinstance(query, ECQ):
		rewrittenQuery = __rewriteECQ(query, posAxioms)
		
		return ECQ(rewrittenQuery, conceptList, roleList, individualList)
	
	if isinstance(query, UCQ):
		rewrittenQuery = __rewriteUCQ(query, posAxioms)
		
		return UCQ(rewrittenQuery, conceptList, roleList, individualList)
	
	return rewrittenQuery
	
	
