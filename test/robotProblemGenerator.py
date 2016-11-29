#!/bin/python3
from itertools import product

def generate_planning_domain(columns, rows, filename):
	
	print("Inizio la generazione del planning domain.\n")
	
	#~ Inizializzo il dominio di planning
	planning_domain = """(define (domain robot)
	(:requirements :ekab)\n"""
	
	#~ Genero i predicati per ogni colonna e riga
	planning_domain += "\t(:predicates\n"
	planning_domain += "\t\t(Columns ?x)\n"
	planning_domain += "\t\t(Rows ?x)\n"
	
	for column in range(columns):
		planning_domain += "\t\t(Column"+str(column)+" ?x)\n"
	for column in range(columns):
		planning_domain += "\t\t(RightOf"+str(column)+" ?x)\n"
	for column in range(columns):
		planning_domain += "\t\t(LeftOf"+str(column+1)+" ?x)\n"
		
	for row in range(rows):
		planning_domain += "\t\t(Row"+str(row)+" ?x)\n"
	for row in range(rows):
		planning_domain += "\t\t(AboveOf"+str(row)+" ?x)\n"
	for row in range(rows):
		planning_domain += "\t\t(BelowOf"+str(row+1)+" ?x)\n"
	
	#~ Chiudo la parentesi di predicates
	planning_domain += "\t)\n"
	
	#~ Creo il file e gli scrivo dentro planning_domain
	output_file = open(filename, "w")
	output_file.write(planning_domain)
	output_file.close()
	
	planning_domain = ""
	print("Finito la sezione :predicates\n")
	
	#~ Genero gli assiomi
	planning_domain += "\t(:axioms\n"
	
	planning_domain += "\t\t(isA RightOf0 Columns)\n"
	for column in range(columns-1):
		planning_domain += "\t\t(isA RightOf"+str(column+1)+" RightOf"+str(column)+")\n"
	
	planning_domain += "\t\t(isA LeftOf"+str(columns)+" Columns)\n"
	for column in range(columns-1):
		planning_domain += "\t\t(isA LeftOf"+str(columns-column-1)+" LeftOf"+str(columns-column)+")\n"
		
	planning_domain += "\t\t(isA AboveOf0 Rows)\n"
	for row in range(rows-1):
		planning_domain += "\t\t(isA AboveOf"+str(row+1)+" AboveOf"+str(row)+")\n"
	
	planning_domain += "\t\t(isA BelowOf"+str(rows)+" Rows)\n"
	for row in range(rows-1):
		planning_domain += "\t\t(isA BelowOf"+str(rows-row-1)+" BelowOf"+str(rows-row)+")\n"
		
	for column in range(1,columns):
		planning_domain += "\t\t(isA LeftOf"+str(column)+" (not RightOf"+str(column)+"))\n"
	for row in range(1,rows):
		planning_domain += "\t\t(isA AboveOf"+str(row)+" (not BelowOf"+str(row)+"))\n"
	
	#~ Chiudo la parentesi di axioms
	planning_domain += "\t)\n"
	
	#~ Creo il file e gli scrivo dentro planning_domain
	output_file = open(filename, "a")
	output_file.write(planning_domain)
	output_file.close()
	
	planning_domain = ""
	print("Finito la sezione :axioms\n")
	
	#~ Genero le rules che muovono il robot
	planning_domain += "\t(:rule ruleRight\n"
	planning_domain += "\t\t:condition (mko(Columns ?x))\n"
	planning_domain += "\t\t:action moveRight\n"
	planning_domain += "\t)\n"
	
	planning_domain += "\t(:rule ruleLeft\n"
	planning_domain += "\t\t:condition (mko(Columns ?x))\n"
	planning_domain += "\t\t:action moveLeft\n"
	planning_domain += "\t)\n"
	
	planning_domain += "\t(:rule ruleUp\n"
	planning_domain += "\t\t:condition (mko(Rows ?x))\n"
	planning_domain += "\t\t:action moveUp\n"
	planning_domain += "\t)\n"
	
	planning_domain += "\t(:rule ruleDown\n"
	planning_domain += "\t\t:condition (mko(Rows ?x))\n"
	planning_domain += "\t\t:action moveDown\n"
	planning_domain += "\t)\n"
	
	#~ Creo il file e gli scrivo dentro planning_domain
	output_file = open(filename, "a")
	output_file.write(planning_domain)
	output_file.close()
	
	planning_domain = ""
	print("Finito la sezione :rule\n")
	
	#~ Genero le azioni
	#~ Genero moveRight
	planning_domain += "\t(:action moveRight\n"
	planning_domain += "\t\t:parameters (?x)\n"
	planning_domain += "\t\t:effects \n"
	
	for column in range(columns-1):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (RightOf"+str(column)+" ?x))\n"
		planning_domain += "\t\t:add ((RightOf"+str(column+1)+" ?x))\n"
		#~ planning_domain += "\t\t:delete ()\n"
		planning_domain += "\t\t)\n"
	
	for column in range(1,columns):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (LeftOf"+str(column)+" ?x))\n"
		planning_domain += "\t\t:add ((LeftOf"+str(column+1)+" ?x))\n"
		planning_domain += "\t\t:delete ((LeftOf"+str(column)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	for column in range(columns-1):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (Column"+str(column)+" ?x))\n"
		planning_domain += "\t\t:add ((Column"+str(column+1)+" ?x))\n"
		planning_domain += "\t\t:delete ((Column"+str(column)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	for column in range(columns-1):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (and (RightOf"+str(column)+" ?x) (LeftOf"+str(column+1)+" ?x)))\n"
		planning_domain += "\t\t:add ((Column"+str(column+1)+" ?x))\n"
		#~ planning_domain += "\t\t:delete ((Column"+str(column)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	#~ Chiudo la parentesi di moveRight
	planning_domain += "\t)\n"
	
	#~ Genero moveLeft
	planning_domain += "\t(:action moveLeft\n"
	planning_domain += "\t\t:parameters (?x)\n"
	planning_domain += "\t\t:effects \n"
	
	for column in range(2,columns+1):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (LeftOf"+str(column)+" ?x))\n"
		planning_domain += "\t\t:add ((LeftOf"+str(column-1)+" ?x))\n"
		#~ planning_domain += "\t\t:delete ()\n"
		planning_domain += "\t\t)\n"
	
	for column in range(1,columns):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (RightOf"+str(column)+" ?x))\n"
		planning_domain += "\t\t:add ((RightOf"+str(column-1)+" ?x))\n"
		planning_domain += "\t\t:delete ((RightOf"+str(column)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	for column in range(1,columns):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (Column"+str(column)+" ?x))\n"
		planning_domain += "\t\t:add ((Column"+str(column-1)+" ?x))\n"
		planning_domain += "\t\t:delete ((Column"+str(column)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	for column in range(1,columns):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (and (RightOf"+str(column)+" ?x) (LeftOf"+str(column+1)+" ?x)))\n"
		planning_domain += "\t\t:add ((Column"+str(column-1)+" ?x))\n"
		#~ planning_domain += "\t\t:delete ((Column"+str(column)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	#~ Chiudo la parentesi di moveLeft
	planning_domain += "\t)\n"
	
	#~ Genero moveUp
	planning_domain += "\t(:action moveUp\n"
	planning_domain += "\t\t:parameters (?x)\n"
	planning_domain += "\t\t:effects \n"
	
	for row in range(rows-1):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (AboveOf"+str(row)+" ?x))\n"
		planning_domain += "\t\t:add ((AboveOf"+str(row+1)+" ?x))\n"
		#~ planning_domain += "\t\t:delete ()\n"
		planning_domain += "\t\t)\n"
	
	for row in range(1,rows):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (BelowOf"+str(row)+" ?x))\n"
		planning_domain += "\t\t:add ((BelowOf"+str(row+1)+" ?x))\n"
		planning_domain += "\t\t:delete ((BelowOf"+str(row)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	for row in range(rows-1):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (Row"+str(row)+" ?x))\n"
		planning_domain += "\t\t:add ((Row"+str(row+1)+" ?x))\n"
		planning_domain += "\t\t:delete ((Row"+str(row)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	for row in range(rows-1):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (and (AboveOf"+str(row)+" ?x) (BelowOf"+str(row+1)+" ?x)))\n"
		planning_domain += "\t\t:add ((Row"+str(row+1)+" ?x))\n"
		#~ planning_domain += "\t\t:delete ((Row"+str(row)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	#~ Chiudo la parentesi di moveUp
	planning_domain += "\t)\n"
	
	#~ Genero moveDown
	planning_domain += "\t(:action moveDown\n"
	planning_domain += "\t\t:parameters (?x)\n"
	planning_domain += "\t\t:effects \n"
	
	for row in range(2,rows+1):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (BelowOf"+str(row)+" ?x))\n"
		planning_domain += "\t\t:add ((BelowOf"+str(row-1)+" ?x))\n"
		#~ planning_domain += "\t\t:delete ()\n"
		planning_domain += "\t\t)\n"
	
	for row in range(1,rows):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (AboveOf"+str(row)+" ?x))\n"
		planning_domain += "\t\t:add ((AboveOf"+str(row-1)+" ?x))\n"
		planning_domain += "\t\t:delete ((AboveOf"+str(row)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	for row in range(1,rows):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (Row"+str(row)+" ?x))\n"
		planning_domain += "\t\t:add ((Row"+str(row-1)+" ?x))\n"
		planning_domain += "\t\t:delete ((Row"+str(row)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	for row in range(1,rows):
		planning_domain += "\t\t(\n"
		planning_domain += "\t\t:condition (mko (and (AboveOf"+str(row)+" ?x) (BelowOf"+str(row+1)+" ?x)))\n"
		planning_domain += "\t\t:add ((Row"+str(row-1)+" ?x))\n"
		#~ planning_domain += "\t\t:delete ((Row"+str(row)+" ?x))\n"
		planning_domain += "\t\t)\n"
	
	#~ Chiudo la parentesi di moveDown
	planning_domain += "\t)\n"
	
	#~ Creo il file e gli scrivo dentro planning_domain
	output_file = open(filename, "a")
	output_file.write(planning_domain)
	output_file.close()
	
	planning_domain = ""
	print("Finito la sezione :action\n")
	
	#~ Chiudo la parentesi di domain
	planning_domain += "\n)"
	
	#~ Creo il file e gli scrivo dentro planning_domain
	output_file = open(filename, "a")
	output_file.write(planning_domain)
	output_file.close()
	
	print("Finito di scrivere il dominio!\n")

def generate_planning_problem(rightOf, leftOf, aboveOf, belowOf, column, row, filename):
	
	#~ Inizializzo il problema di planning
	planning_domain = """(define (problem robotProblem)
	(:domain robot)\n"""
	
	#~ Genero gli individui in :objects
	planning_domain += "\t(:objects robot)\n"
	
	#~ Definisco :init
	planning_domain += "\t(:init\n"
	planning_domain += "\t\t(RightOf" + str(rightOf) + " robot)\n"
	planning_domain += "\t\t(LeftOf" + str(leftOf) + " robot)\n"
	planning_domain += "\t\t(AboveOf" + str(aboveOf) + " robot)\n"
	planning_domain += "\t\t(BelowOf" + str(belowOf) + " robot)\n"
	
	#~ Chiudo la parentesi di init
	planning_domain += "\t)\n"
	
	#~ Definisco il goal
	planning_domain += "\t(:goal (mko (and (Column" + str(column) + " robot) (Row" + str(row) + " robot))))\n"
	
	#~ Chiudo la parentesi di domain
	planning_domain += "\n)"
	
	#~ Creo il file e gli scrivo dentro planning_domain
	output_file = open(filename, "w")
	output_file.write(planning_domain)
	output_file.close()

if __name__ == '__main__':
	columns = 7
	rows = 7
	generate_planning_domain(columns = columns, rows = rows, filename = "robotDomain.pddl")
	generate_planning_problem(rightOf = 2, leftOf = columns-1, aboveOf = 0, belowOf = rows-1, column = 2, row = 1, filename = "robotDomain-problem.pddl")
