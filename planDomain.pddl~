(define (domain elevators_sequencedstrips)
  (:requirements :ekab)

(:predicates 
	(passenger_at ?floor)
	(boarded ?person)
	
 (lift_at ?floor ?x)
	(reachable_floor ?lift ?x)
	(above ?floor1)
	(passengers ?lift)
	(can_hold ?lift )
	(next ?n1 ?n1)

  (osr ?sx)
)

(:axioms
  (isA	 passenger_at   above)
  (isA  passenger_at above)
  (isA above (not can_hold))
  (isA  above  (not (exists   (inverse next ))   )  )
  (isA next (not reachable_floor))
  (isA (exists (inverse reachable_floor)) above)
  (funct next)
)

(:rule rule_move1
:condition (mko (above  ?a))
:action move_up_slow1
)




(:rule rule_move2
:condition (mko (and (can_hold  ?lift) (next ?f1 ?f2)))
:action move_up_slow2
)

(:action move_up_slow1
  :parameters (?a)
  :effects (
    :condition (not (mko (next ?x ?y)))
    :add ((passengers a))
    :delete ((next a b) (passengers ?y))
  )
  (
    :condition (not (mko (next ?bc ?z)))
    :add ((passengers a))
    :delete ((next a ?bc) (passengers ?z))
  )

)

(:action move_up_slow2
  :parameters (?lift ?f1 ?f2 )
  :effects (
    :condition (not (mko (next ?x ?y)))
    :add ()
    :delete ((next a b) (passengers e))
  )

)
  
)

