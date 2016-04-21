(define (problem taskAssigment_problem)
	(:domain taskAssigment)
	(:objects a b c)
	(:init
		(Designer a)
	)
	(:goal (exists (?x ?y)
			(and
				(mko (and (ElectronicEngineer ?x) (ElectronicEngineer ?y)))
				(not (mko-eq ?x ?y))
			)
		)
	)
)
