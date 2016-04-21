from pyparsing import *

class Syntax:
	#~ We simply collect useful syntax that will be used throughout the other classes
	
	def __init__(self):
		
		self.keywords = ["isA", "not", "funct", ":topC", "inverse", "exists", "existsQualified", "neq", "mko", "mko-eq", "and", "or", "CheckConsistencyAction"]
		
		#~ Symbols used in the parsing phase
		self.leftPar = Literal("(").suppress() #Left parenthesis, can be suppressed
		self.rightPar = Literal(")").suppress() #Right parenthesis, can be suppressed
		self.isA = "isA"
		self.neg = "not"
		self.funct = "funct"
		self.topC = Literal(":topC")
		self.inverse = "inverse"
		self.exists = "exists"
		self.existsQualified = "existsQualified"
		self.neq = "neq"
		self.queryAnd = "and"
		self.queryOr = "or"
		self.true = ":True"
		self.mko = "mko"
		self.mkoEq = "mko-eq"
		
		self.allowed_symbols = "-"
		self.allowed_word = Regex("[a-zA-Z0-9]+[a-zA-Z0-9_]*")
		self.variable = Literal("?").suppress() + self.allowed_word #~ A PDDL Variable is of the type "?x", so a word always with "?" at the beginning
		self.ndnsVariable = "_"
		
		#~ PDDL Keywords
		self.pddlDefineTag = Literal("define").suppress()
		self.pddlDomainTag = Literal("domain").suppress()
		self.pddlDomainName = self.allowed_word # PDDL Domain name
		self.pddlRequirements = self.leftPar + Literal(":requirements :ekab") + self.rightPar # PDDL Requirements
		self.pddlPredicatesTag = Literal(":predicates")
		self.pddlAxiomsTag = Literal(":axioms").suppress()
		self.pddlRuleTag = Literal(":rule").suppress()
		self.pddlRuleConditionTag = Literal(":condition").suppress()
		self.pddlRuleActionTag = Literal(":action").suppress()
		self.pddlActionTag = Literal(":action").suppress()
		self.pddlActionEffectConditionTag = Literal(":condition").suppress()
		self.pddlActionEffectAddTag = Literal(":add").suppress()
		self.pddlActionEffectDelTag = Literal(":delete").suppress()
		self.pddlActionEffectsTag = Literal(":effects").suppress()
		self.pddlProblemTag = Literal("problem").suppress()
		self.pddlProblemName = self.allowed_word # PDDL Problem name
		self.pddlProblemDomainTag = Literal(":domain").suppress()
		self.pddlProblemObjectsTag = Literal(":objects")
		self.pddlProblemObject = self.allowed_word # PDDL Objects
		self.pddlProblemInitTag = Literal(":init").suppress()
		self.pddlProblemGoalTag = Literal(":goal").suppress()
		
		self.pddlNDNSVar = Literal(":blank") # non-distinguished non-shared variable
		
		#~ ADL Keywords
		self.ADLCheckConsistency = "CheckConsistency"
		self.ADLError = "Error"
		self.ADLCheckConsistencyAction = "CheckConsistencyAction"
		
		#~ Miscellaneous
		self.indent = "  "
