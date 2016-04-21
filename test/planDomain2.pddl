(define (domain elevators_sequencedstrips)
  (:requirements :ekab)

(:predicates 
	(concept1 ?x)
	(concept2 ?x)
	(role1 ?x ?y)
	(role2 ?x ?y)
)

(:axioms
  (isA	concept1 (not concept2))
  (isA  (exists (inverse role1)) concept1)
  (isA  (exists role2) concept2)
)

(:rule rule1
:condition (mko (concept1  ?x))
:action action1
)

(:action action1
  :parameters (?x ?y)
  :effects (
    :condition (:True)
    :add ((concept2 ?y))
  )

)
  
)

