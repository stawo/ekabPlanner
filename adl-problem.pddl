(define (problem robotProblem )
  (:domain robot)
  (:objects
    robot 
  )
  (:init
    (BelowOf6 robot)
    (LeftOf6 robot)
    (AboveOf0 robot)
    (RightOf2 robot)
    (not (CheckConsistency))
    (not (Error))
  )
  (:goal
    (and
      (not (CheckConsistency))
      (not (Error))
      (Column2 robot)
      (Row1 robot)
    )
  )
)