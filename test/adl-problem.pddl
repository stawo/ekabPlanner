(define (problem taskAssigment_problem )
  (:domain taskAssigment)
  (:objects
    b a 
  )
  (:init
    (Designer a)
    (not (CheckConsistency))
    (not (Error))
  )
  (:goal
    (and
      (not (CheckConsistency))
      (not (Error))
      (exists ( ?x ?y )
        (and
          (and
            (ElectronicEngineer ?y)
            (ElectronicEngineer ?x)
          )
          (not
            (=?x ?y )
          )
        )
      )
    )
  )
)