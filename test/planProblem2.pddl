(define (problem elevators_sequencedstrips_problem)
	(:domain elevators_sequencedstrips)
	(:objects a b c d e f g h)
	(:init
		(concept1 a)
	)
	(:goal (exists (?x)
			(mko (role2 ?x ?x))
		)
	)
)
