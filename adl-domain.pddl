(define
  (domain robot)
  (:requirements :adl)
  (:predicates
    (AboveOf3 ?x )
    (LeftOf5 ?x )
    (LeftOf7 ?x )
    (BelowOf3 ?x )
    (Columns ?x )
    (Column1 ?x )
    (Column5 ?x )
    (RightOf6 ?x )
    (Row1 ?x )
    (RightOf0 ?x )
    (BelowOf6 ?x )
    (LeftOf2 ?x )
    (RightOf2 ?x )
    (Column3 ?x )
    (Column4 ?x )
    (Row3 ?x )
    (Column0 ?x )
    (LeftOf6 ?x )
    (AboveOf0 ?x )
    (Column2 ?x )
    (RightOf1 ?x )
    (RightOf4 ?x )
    (Rows ?x )
    (Row4 ?x )
    (Row0 ?x )
    (AboveOf1 ?x )
    (AboveOf5 ?x )
    (BelowOf2 ?x )
    (BelowOf7 ?x )
    (AboveOf2 ?x )
    (AboveOf6 ?x )
    (BelowOf4 ?x )
    (AboveOf4 ?x )
    (LeftOf4 ?x )
    (BelowOf1 ?x )
    (BelowOf5 ?x )
    (LeftOf1 ?x )
    (RightOf3 ?x )
    (Row2 ?x )
    (Row5 ?x )
    (LeftOf3 ?x )
    (Row6 ?x )
    (Column6 ?x )
    (RightOf5 ?x )
    (CheckConsistency)
    (Error)
  )
  (:action moveDown
    :parameters ( ?x )
    :precondition ( and
      (not (CheckConsistency))
      (not (Error))
      (or
        (AboveOf5 ?x)
        (Rows ?x)
        (BelowOf5 ?x)
        (BelowOf7 ?x)
        (BelowOf6 ?x)
        (BelowOf4 ?x)
        (AboveOf4 ?x)
        (BelowOf2 ?x)
        (AboveOf3 ?x)
        (BelowOf1 ?x)
        (AboveOf1 ?x)
        (AboveOf6 ?x)
        (AboveOf2 ?x)
        (BelowOf3 ?x)
        (AboveOf0 ?x)
      )
    )
    :effect ( and
      (CheckConsistency)
      (when
        (or
          (BelowOf1 ?x)
          (BelowOf2 ?x)
        )
        (and
          (BelowOf1 ?x)
        )
      )
      (when
        (or
          (BelowOf3 ?x)
          (BelowOf1 ?x)
          (BelowOf2 ?x)
        )
        (and
          (BelowOf2 ?x)
        )
      )
      (when
        (or
          (BelowOf4 ?x)
          (BelowOf1 ?x)
          (BelowOf3 ?x)
          (BelowOf2 ?x)
        )
        (and
          (BelowOf3 ?x)
        )
      )
      (when
        (or
          (BelowOf2 ?x)
          (BelowOf4 ?x)
          (BelowOf1 ?x)
          (BelowOf3 ?x)
          (BelowOf5 ?x)
        )
        (and
          (BelowOf4 ?x)
        )
      )
      (when
        (or
          (BelowOf2 ?x)
          (BelowOf5 ?x)
          (BelowOf6 ?x)
          (BelowOf4 ?x)
          (BelowOf1 ?x)
          (BelowOf3 ?x)
        )
        (and
          (BelowOf5 ?x)
        )
      )
      (when
        (or
          (BelowOf5 ?x)
          (BelowOf2 ?x)
          (BelowOf6 ?x)
          (BelowOf4 ?x)
          (BelowOf7 ?x)
          (BelowOf1 ?x)
          (BelowOf3 ?x)
        )
        (and
          (BelowOf6 ?x)
        )
      )
      (when
        (or
          (AboveOf5 ?x)
          (AboveOf4 ?x)
          (AboveOf3 ?x)
          (AboveOf1 ?x)
          (AboveOf6 ?x)
          (AboveOf2 ?x)
        )
        (and
          (AboveOf0 ?x)
          (not (AboveOf1 ?x))
        )
      )
      (when
        (or
          (AboveOf2 ?x)
          (AboveOf3 ?x)
          (AboveOf4 ?x)
          (AboveOf5 ?x)
          (AboveOf6 ?x)
        )
        (and
          (AboveOf1 ?x)
          (not (AboveOf2 ?x))
        )
      )
      (when
        (or
          (AboveOf3 ?x)
          (AboveOf4 ?x)
          (AboveOf5 ?x)
          (AboveOf6 ?x)
        )
        (and
          (AboveOf2 ?x)
          (not (AboveOf3 ?x))
        )
      )
      (when
        (or
          (AboveOf4 ?x)
          (AboveOf5 ?x)
          (AboveOf6 ?x)
        )
        (and
          (AboveOf3 ?x)
          (not (AboveOf4 ?x))
        )
      )
      (when
        (or
          (AboveOf5 ?x)
          (AboveOf6 ?x)
        )
        (and
          (AboveOf4 ?x)
          (not (AboveOf5 ?x))
        )
      )
      (when
        (AboveOf6 ?x)
        (and
          (AboveOf5 ?x)
          (not (AboveOf6 ?x))
        )
      )
      (when
        (Row1 ?x)
        (and
          (Row0 ?x)
          (not (Row1 ?x))
        )
      )
      (when
        (Row2 ?x)
        (and
          (Row1 ?x)
          (not (Row2 ?x))
        )
      )
      (when
        (Row3 ?x)
        (and
          (Row2 ?x)
          (not (Row3 ?x))
        )
      )
      (when
        (Row4 ?x)
        (and
          (Row3 ?x)
          (not (Row4 ?x))
        )
      )
      (when
        (Row5 ?x)
        (and
          (Row4 ?x)
          (not (Row5 ?x))
        )
      )
      (when
        (Row6 ?x)
        (and
          (Row5 ?x)
          (not (Row6 ?x))
        )
      )
      (when
        (or
          (and
            (BelowOf1 ?x)
            (AboveOf3 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf1 ?x)
          )
          (and
            (AboveOf4 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf2 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf1 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf2 ?x)
          )
          (and
            (AboveOf3 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row0 ?x)
        )
      )
      (when
        (or
          (and
            (BelowOf1 ?x)
            (AboveOf3 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf4 ?x)
          )
          (and
            (AboveOf4 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf2 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf3 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf2 ?x)
          )
          (and
            (AboveOf3 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf2 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row1 ?x)
        )
      )
      (when
        (or
          (and
            (BelowOf1 ?x)
            (AboveOf3 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf3 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf4 ?x)
          )
          (and
            (AboveOf4 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf3 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf3 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row2 ?x)
        )
      )
      (when
        (or
          (and
            (AboveOf5 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf4 ?x)
          )
          (and
            (AboveOf4 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf3 ?x)
          )
          (and
            (BelowOf5 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf5 ?x)
          )
          (and
            (AboveOf4 ?x)
            (BelowOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf4 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row3 ?x)
        )
      )
      (when
        (or
          (and
            (AboveOf5 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf3 ?x)
          )
          (and
            (BelowOf5 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf6 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf4 ?x)
          )
          (and
            (BelowOf6 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row4 ?x)
        )
      )
      (when
        (or
          (and
            (BelowOf4 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf5 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf6 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf7 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row5 ?x)
        )
      )
    )
  )
  (:action moveLeft
    :parameters ( ?x )
    :precondition ( and
      (not (CheckConsistency))
      (not (Error))
      (or
        (RightOf2 ?x)
        (RightOf4 ?x)
        (RightOf5 ?x)
        (LeftOf6 ?x)
        (LeftOf7 ?x)
        (LeftOf2 ?x)
        (LeftOf5 ?x)
        (RightOf3 ?x)
        (LeftOf4 ?x)
        (LeftOf1 ?x)
        (Columns ?x)
        (RightOf0 ?x)
        (LeftOf3 ?x)
        (RightOf1 ?x)
        (RightOf6 ?x)
      )
    )
    :effect ( and
      (CheckConsistency)
      (when
        (or
          (LeftOf1 ?x)
          (LeftOf2 ?x)
        )
        (and
          (LeftOf1 ?x)
        )
      )
      (when
        (or
          (LeftOf1 ?x)
          (LeftOf2 ?x)
          (LeftOf3 ?x)
        )
        (and
          (LeftOf2 ?x)
        )
      )
      (when
        (or
          (LeftOf1 ?x)
          (LeftOf4 ?x)
          (LeftOf3 ?x)
          (LeftOf2 ?x)
        )
        (and
          (LeftOf3 ?x)
        )
      )
      (when
        (or
          (LeftOf1 ?x)
          (LeftOf2 ?x)
          (LeftOf4 ?x)
          (LeftOf3 ?x)
          (LeftOf5 ?x)
        )
        (and
          (LeftOf4 ?x)
        )
      )
      (when
        (or
          (LeftOf6 ?x)
          (LeftOf2 ?x)
          (LeftOf5 ?x)
          (LeftOf4 ?x)
          (LeftOf1 ?x)
          (LeftOf3 ?x)
        )
        (and
          (LeftOf5 ?x)
        )
      )
      (when
        (or
          (LeftOf6 ?x)
          (LeftOf7 ?x)
          (LeftOf2 ?x)
          (LeftOf5 ?x)
          (LeftOf4 ?x)
          (LeftOf1 ?x)
          (LeftOf3 ?x)
        )
        (and
          (LeftOf6 ?x)
        )
      )
      (when
        (or
          (RightOf5 ?x)
          (RightOf4 ?x)
          (RightOf2 ?x)
          (RightOf3 ?x)
          (RightOf1 ?x)
          (RightOf6 ?x)
        )
        (and
          (RightOf0 ?x)
          (not (RightOf1 ?x))
        )
      )
      (when
        (or
          (RightOf2 ?x)
          (RightOf4 ?x)
          (RightOf5 ?x)
          (RightOf3 ?x)
          (RightOf6 ?x)
        )
        (and
          (RightOf1 ?x)
          (not (RightOf2 ?x))
        )
      )
      (when
        (or
          (RightOf3 ?x)
          (RightOf4 ?x)
          (RightOf5 ?x)
          (RightOf6 ?x)
        )
        (and
          (RightOf2 ?x)
          (not (RightOf3 ?x))
        )
      )
      (when
        (or
          (RightOf5 ?x)
          (RightOf4 ?x)
          (RightOf6 ?x)
        )
        (and
          (RightOf3 ?x)
          (not (RightOf4 ?x))
        )
      )
      (when
        (or
          (RightOf5 ?x)
          (RightOf6 ?x)
        )
        (and
          (RightOf4 ?x)
          (not (RightOf5 ?x))
        )
      )
      (when
        (RightOf6 ?x)
        (and
          (RightOf5 ?x)
          (not (RightOf6 ?x))
        )
      )
      (when
        (Column1 ?x)
        (and
          (Column0 ?x)
          (not (Column1 ?x))
        )
      )
      (when
        (Column2 ?x)
        (and
          (Column1 ?x)
          (not (Column2 ?x))
        )
      )
      (when
        (Column3 ?x)
        (and
          (Column2 ?x)
          (not (Column3 ?x))
        )
      )
      (when
        (Column4 ?x)
        (and
          (Column3 ?x)
          (not (Column4 ?x))
        )
      )
      (when
        (Column5 ?x)
        (and
          (Column4 ?x)
          (not (Column5 ?x))
        )
      )
      (when
        (Column6 ?x)
        (and
          (Column5 ?x)
          (not (Column6 ?x))
        )
      )
      (when
        (or
          (and
            (RightOf6 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf1 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf2 ?x)
            (LeftOf2 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf2 ?x)
            (LeftOf1 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf1 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf1 ?x)
          )
        )
        (and
          (Column0 ?x)
        )
      )
      (when
        (or
          (and
            (RightOf6 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf2 ?x)
            (LeftOf2 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf2 ?x)
            (LeftOf1 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf4 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf6 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf2 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf3 ?x)
          )
          (and
            (RightOf2 ?x)
            (LeftOf3 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf1 ?x)
          )
        )
        (and
          (Column1 ?x)
        )
      )
      (when
        (or
          (and
            (RightOf6 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf4 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf4 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf4 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf6 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf4 ?x)
          )
          (and
            (LeftOf4 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf2 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf3 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf1 ?x)
          )
        )
        (and
          (Column2 ?x)
        )
      )
      (when
        (or
          (and
            (RightOf6 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf4 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf5 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf5 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf4 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf6 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf5 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf4 ?x)
          )
          (and
            (LeftOf4 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf1 ?x)
          )
        )
        (and
          (Column3 ?x)
        )
      )
      (when
        (or
          (and
            (RightOf6 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf4 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf5 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf5 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf6 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf6 ?x)
            (RightOf6 ?x)
          )
          (and
            (LeftOf6 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf4 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf2 ?x)
          )
        )
        (and
          (Column4 ?x)
        )
      )
      (when
        (or
          (and
            (RightOf6 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf4 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf5 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf6 ?x)
          )
          (and
            (LeftOf6 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf7 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf2 ?x)
          )
        )
        (and
          (Column5 ?x)
        )
      )
    )
  )
  (:action moveRight
    :parameters ( ?x )
    :precondition ( and
      (not (CheckConsistency))
      (not (Error))
      (or
        (RightOf2 ?x)
        (RightOf4 ?x)
        (RightOf5 ?x)
        (LeftOf6 ?x)
        (LeftOf7 ?x)
        (LeftOf2 ?x)
        (LeftOf5 ?x)
        (RightOf3 ?x)
        (LeftOf4 ?x)
        (LeftOf1 ?x)
        (Columns ?x)
        (RightOf0 ?x)
        (LeftOf3 ?x)
        (RightOf1 ?x)
        (RightOf6 ?x)
      )
    )
    :effect ( and
      (CheckConsistency)
      (when
        (or
          (RightOf5 ?x)
          (RightOf4 ?x)
          (RightOf2 ?x)
          (RightOf3 ?x)
          (RightOf1 ?x)
          (RightOf0 ?x)
          (RightOf6 ?x)
        )
        (and
          (RightOf1 ?x)
        )
      )
      (when
        (or
          (RightOf5 ?x)
          (RightOf4 ?x)
          (RightOf2 ?x)
          (RightOf3 ?x)
          (RightOf1 ?x)
          (RightOf6 ?x)
        )
        (and
          (RightOf2 ?x)
        )
      )
      (when
        (or
          (RightOf2 ?x)
          (RightOf4 ?x)
          (RightOf5 ?x)
          (RightOf3 ?x)
          (RightOf6 ?x)
        )
        (and
          (RightOf3 ?x)
        )
      )
      (when
        (or
          (RightOf3 ?x)
          (RightOf4 ?x)
          (RightOf5 ?x)
          (RightOf6 ?x)
        )
        (and
          (RightOf4 ?x)
        )
      )
      (when
        (or
          (RightOf5 ?x)
          (RightOf4 ?x)
          (RightOf6 ?x)
        )
        (and
          (RightOf5 ?x)
        )
      )
      (when
        (or
          (RightOf5 ?x)
          (RightOf6 ?x)
        )
        (and
          (RightOf6 ?x)
        )
      )
      (when
        (LeftOf1 ?x)
        (and
          (LeftOf2 ?x)
          (not (LeftOf1 ?x))
        )
      )
      (when
        (or
          (LeftOf1 ?x)
          (LeftOf2 ?x)
        )
        (and
          (LeftOf3 ?x)
          (not (LeftOf2 ?x))
        )
      )
      (when
        (or
          (LeftOf1 ?x)
          (LeftOf2 ?x)
          (LeftOf3 ?x)
        )
        (and
          (LeftOf4 ?x)
          (not (LeftOf3 ?x))
        )
      )
      (when
        (or
          (LeftOf1 ?x)
          (LeftOf4 ?x)
          (LeftOf3 ?x)
          (LeftOf2 ?x)
        )
        (and
          (LeftOf5 ?x)
          (not (LeftOf4 ?x))
        )
      )
      (when
        (or
          (LeftOf1 ?x)
          (LeftOf2 ?x)
          (LeftOf4 ?x)
          (LeftOf3 ?x)
          (LeftOf5 ?x)
        )
        (and
          (LeftOf6 ?x)
          (not (LeftOf5 ?x))
        )
      )
      (when
        (or
          (LeftOf6 ?x)
          (LeftOf2 ?x)
          (LeftOf5 ?x)
          (LeftOf4 ?x)
          (LeftOf1 ?x)
          (LeftOf3 ?x)
        )
        (and
          (LeftOf7 ?x)
          (not (LeftOf6 ?x))
        )
      )
      (when
        (Column0 ?x)
        (and
          (Column1 ?x)
          (not (Column0 ?x))
        )
      )
      (when
        (Column1 ?x)
        (and
          (Column2 ?x)
          (not (Column1 ?x))
        )
      )
      (when
        (Column2 ?x)
        (and
          (Column3 ?x)
          (not (Column2 ?x))
        )
      )
      (when
        (Column3 ?x)
        (and
          (Column4 ?x)
          (not (Column3 ?x))
        )
      )
      (when
        (Column4 ?x)
        (and
          (Column5 ?x)
          (not (Column4 ?x))
        )
      )
      (when
        (Column5 ?x)
        (and
          (Column6 ?x)
          (not (Column5 ?x))
        )
      )
      (when
        (or
          (and
            (LeftOf1 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf2 ?x)
            (LeftOf1 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf1 ?x)
            (LeftOf1 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf0 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf1 ?x)
          )
        )
        (and
          (Column1 ?x)
        )
      )
      (when
        (or
          (and
            (RightOf6 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf1 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf2 ?x)
            (LeftOf2 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf2 ?x)
            (LeftOf1 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf1 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf1 ?x)
          )
        )
        (and
          (Column2 ?x)
        )
      )
      (when
        (or
          (and
            (RightOf6 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf2 ?x)
            (LeftOf2 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf2 ?x)
            (LeftOf1 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf4 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf6 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf2 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf3 ?x)
          )
          (and
            (RightOf2 ?x)
            (LeftOf3 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf1 ?x)
          )
        )
        (and
          (Column3 ?x)
        )
      )
      (when
        (or
          (and
            (RightOf6 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf4 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf4 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf4 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf6 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf4 ?x)
          )
          (and
            (LeftOf4 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf3 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf2 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf3 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf1 ?x)
          )
        )
        (and
          (Column4 ?x)
        )
      )
      (when
        (or
          (and
            (RightOf6 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf4 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf5 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf5 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf4 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf6 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf5 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf4 ?x)
          )
          (and
            (LeftOf4 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf4 ?x)
            (LeftOf1 ?x)
          )
        )
        (and
          (Column5 ?x)
        )
      )
      (when
        (or
          (and
            (RightOf6 ?x)
            (LeftOf1 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf2 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf4 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf5 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf6 ?x)
          )
          (and
            (RightOf5 ?x)
            (LeftOf5 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf6 ?x)
          )
          (and
            (LeftOf3 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf1 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf6 ?x)
            (RightOf6 ?x)
          )
          (and
            (LeftOf6 ?x)
            (RightOf5 ?x)
          )
          (and
            (LeftOf4 ?x)
            (RightOf5 ?x)
          )
          (and
            (RightOf6 ?x)
            (LeftOf2 ?x)
          )
        )
        (and
          (Column6 ?x)
        )
      )
    )
  )
  (:action moveUp
    :parameters ( ?x )
    :precondition ( and
      (not (CheckConsistency))
      (not (Error))
      (or
        (AboveOf5 ?x)
        (Rows ?x)
        (BelowOf5 ?x)
        (BelowOf7 ?x)
        (BelowOf6 ?x)
        (BelowOf4 ?x)
        (AboveOf4 ?x)
        (BelowOf2 ?x)
        (AboveOf3 ?x)
        (BelowOf1 ?x)
        (AboveOf1 ?x)
        (AboveOf6 ?x)
        (AboveOf2 ?x)
        (BelowOf3 ?x)
        (AboveOf0 ?x)
      )
    )
    :effect ( and
      (CheckConsistency)
      (when
        (or
          (AboveOf5 ?x)
          (AboveOf4 ?x)
          (AboveOf3 ?x)
          (AboveOf1 ?x)
          (AboveOf6 ?x)
          (AboveOf2 ?x)
          (AboveOf0 ?x)
        )
        (and
          (AboveOf1 ?x)
        )
      )
      (when
        (or
          (AboveOf5 ?x)
          (AboveOf4 ?x)
          (AboveOf3 ?x)
          (AboveOf1 ?x)
          (AboveOf6 ?x)
          (AboveOf2 ?x)
        )
        (and
          (AboveOf2 ?x)
        )
      )
      (when
        (or
          (AboveOf2 ?x)
          (AboveOf3 ?x)
          (AboveOf4 ?x)
          (AboveOf5 ?x)
          (AboveOf6 ?x)
        )
        (and
          (AboveOf3 ?x)
        )
      )
      (when
        (or
          (AboveOf3 ?x)
          (AboveOf4 ?x)
          (AboveOf5 ?x)
          (AboveOf6 ?x)
        )
        (and
          (AboveOf4 ?x)
        )
      )
      (when
        (or
          (AboveOf4 ?x)
          (AboveOf5 ?x)
          (AboveOf6 ?x)
        )
        (and
          (AboveOf5 ?x)
        )
      )
      (when
        (or
          (AboveOf5 ?x)
          (AboveOf6 ?x)
        )
        (and
          (AboveOf6 ?x)
        )
      )
      (when
        (BelowOf1 ?x)
        (and
          (BelowOf2 ?x)
          (not (BelowOf1 ?x))
        )
      )
      (when
        (or
          (BelowOf1 ?x)
          (BelowOf2 ?x)
        )
        (and
          (BelowOf3 ?x)
          (not (BelowOf2 ?x))
        )
      )
      (when
        (or
          (BelowOf3 ?x)
          (BelowOf1 ?x)
          (BelowOf2 ?x)
        )
        (and
          (BelowOf4 ?x)
          (not (BelowOf3 ?x))
        )
      )
      (when
        (or
          (BelowOf4 ?x)
          (BelowOf1 ?x)
          (BelowOf3 ?x)
          (BelowOf2 ?x)
        )
        (and
          (BelowOf5 ?x)
          (not (BelowOf4 ?x))
        )
      )
      (when
        (or
          (BelowOf2 ?x)
          (BelowOf4 ?x)
          (BelowOf1 ?x)
          (BelowOf3 ?x)
          (BelowOf5 ?x)
        )
        (and
          (BelowOf6 ?x)
          (not (BelowOf5 ?x))
        )
      )
      (when
        (or
          (BelowOf2 ?x)
          (BelowOf5 ?x)
          (BelowOf6 ?x)
          (BelowOf4 ?x)
          (BelowOf1 ?x)
          (BelowOf3 ?x)
        )
        (and
          (BelowOf7 ?x)
          (not (BelowOf6 ?x))
        )
      )
      (when
        (Row0 ?x)
        (and
          (Row1 ?x)
          (not (Row0 ?x))
        )
      )
      (when
        (Row1 ?x)
        (and
          (Row2 ?x)
          (not (Row1 ?x))
        )
      )
      (when
        (Row2 ?x)
        (and
          (Row3 ?x)
          (not (Row2 ?x))
        )
      )
      (when
        (Row3 ?x)
        (and
          (Row4 ?x)
          (not (Row3 ?x))
        )
      )
      (when
        (Row4 ?x)
        (and
          (Row5 ?x)
          (not (Row4 ?x))
        )
      )
      (when
        (Row5 ?x)
        (and
          (Row6 ?x)
          (not (Row5 ?x))
        )
      )
      (when
        (or
          (and
            (BelowOf1 ?x)
            (AboveOf3 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf1 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf2 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf5 ?x)
          )
          (and
            (AboveOf0 ?x)
            (BelowOf1 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row1 ?x)
        )
      )
      (when
        (or
          (and
            (BelowOf1 ?x)
            (AboveOf3 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf1 ?x)
          )
          (and
            (AboveOf4 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf2 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf1 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf2 ?x)
          )
          (and
            (AboveOf3 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row2 ?x)
        )
      )
      (when
        (or
          (and
            (BelowOf1 ?x)
            (AboveOf3 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf4 ?x)
          )
          (and
            (AboveOf4 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf2 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf3 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf2 ?x)
          )
          (and
            (AboveOf3 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf2 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row3 ?x)
        )
      )
      (when
        (or
          (and
            (BelowOf1 ?x)
            (AboveOf3 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf3 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf4 ?x)
          )
          (and
            (AboveOf4 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf3 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf3 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row4 ?x)
        )
      )
      (when
        (or
          (and
            (AboveOf5 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf4 ?x)
          )
          (and
            (AboveOf4 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf3 ?x)
          )
          (and
            (BelowOf5 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf4 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf5 ?x)
          )
          (and
            (AboveOf4 ?x)
            (BelowOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf4 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row5 ?x)
        )
      )
      (when
        (or
          (and
            (AboveOf5 ?x)
            (BelowOf2 ?x)
          )
          (and
            (BelowOf4 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf3 ?x)
          )
          (and
            (BelowOf5 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf5 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf6 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf1 ?x)
            (AboveOf6 ?x)
          )
          (and
            (AboveOf5 ?x)
            (BelowOf4 ?x)
          )
          (and
            (BelowOf6 ?x)
            (AboveOf5 ?x)
          )
          (and
            (BelowOf3 ?x)
            (AboveOf6 ?x)
          )
          (and
            (BelowOf2 ?x)
            (AboveOf6 ?x)
          )
        )
        (and
          (Row6 ?x)
        )
      )
    )
  )
  (:action CheckConsistencyAction
    :parameters ( )
    :precondition ( and
      (CheckConsistency)
      (not (Error))
    )
    :effect ( and
      (not (CheckConsistency))
      (when
        (or
          (exists (?x_8 )
            (and
              (RightOf4 ?x_8)
              (LeftOf2 ?x_8)
            )
          )
          (exists (?x_1 )
            (and
              (AboveOf5 ?x_1)
              (BelowOf1 ?x_1)
            )
          )
          (exists (?x_2 )
            (and
              (RightOf4 ?x_2)
              (LeftOf3 ?x_2)
            )
          )
          (exists (?x_7 )
            (and
              (AboveOf4 ?x_7)
              (BelowOf2 ?x_7)
            )
          )
          (exists (?x_9 )
            (and
              (RightOf6 ?x_9)
              (LeftOf2 ?x_9)
            )
          )
          (exists (?x_1 )
            (and
              (BelowOf3 ?x_1)
              (AboveOf5 ?x_1)
            )
          )
          (exists (?x_9 )
            (and
              (LeftOf2 ?x_9)
              (RightOf3 ?x_9)
            )
          )
          (exists (?x_0 )
            (and
              (BelowOf1 ?x_0)
              (AboveOf6 ?x_0)
            )
          )
          (exists (?x_2 )
            (and
              (LeftOf4 ?x_2)
              (RightOf6 ?x_2)
            )
          )
          (exists (?x_5 )
            (and
              (BelowOf4 ?x_5)
              (AboveOf6 ?x_5)
            )
          )
          (exists (?x_9 )
            (and
              (RightOf6 ?x_9)
              (LeftOf1 ?x_9)
            )
          )
          (exists (?x_0 )
            (and
              (AboveOf2 ?x_0)
              (BelowOf2 ?x_0)
            )
          )
          (exists (?x_4 )
            (and
              (BelowOf3 ?x_4)
              (AboveOf5 ?x_4)
            )
          )
          (exists (?x_11 )
            (and
              (RightOf6 ?x_11)
              (LeftOf3 ?x_11)
            )
          )
          (exists (?x_1 )
            (and
              (BelowOf5 ?x_1)
              (AboveOf6 ?x_1)
            )
          )
          (exists (?x_4 )
            (and
              (AboveOf4 ?x_4)
              (BelowOf3 ?x_4)
            )
          )
          (exists (?x_7 )
            (and
              (BelowOf1 ?x_7)
              (AboveOf5 ?x_7)
            )
          )
          (exists (?x_1 )
            (and
              (AboveOf6 ?x_1)
              (BelowOf4 ?x_1)
            )
          )
          (exists (?x_6 )
            (and
              (RightOf5 ?x_6)
              (LeftOf1 ?x_6)
            )
          )
          (exists (?x_1 )
            (and
              (BelowOf2 ?x_1)
              (AboveOf5 ?x_1)
            )
          )
          (exists (?x_6 )
            (and
              (LeftOf2 ?x_6)
              (RightOf6 ?x_6)
            )
          )
          (exists (?x_11 )
            (and
              (RightOf6 ?x_11)
              (LeftOf5 ?x_11)
            )
          )
          (exists (?x_5 )
            (and
              (BelowOf5 ?x_5)
              (AboveOf6 ?x_5)
            )
          )
          (exists (?x_11 )
            (and
              (RightOf6 ?x_11)
              (LeftOf6 ?x_11)
            )
          )
          (exists (?x_9 )
            (and
              (LeftOf3 ?x_9)
              (RightOf6 ?x_9)
            )
          )
          (exists (?x_7 )
            (and
              (AboveOf5 ?x_7)
              (BelowOf2 ?x_7)
            )
          )
          (exists (?x_4 )
            (and
              (AboveOf5 ?x_4)
              (BelowOf2 ?x_4)
            )
          )
          (exists (?x_8 )
            (and
              (RightOf6 ?x_8)
              (LeftOf1 ?x_8)
            )
          )
          (exists (?x_6 )
            (and
              (RightOf5 ?x_6)
              (LeftOf4 ?x_6)
            )
          )
          (exists (?x_0 )
            (and
              (BelowOf2 ?x_0)
              (AboveOf4 ?x_0)
            )
          )
          (exists (?x_5 )
            (and
              (BelowOf3 ?x_5)
              (AboveOf6 ?x_5)
            )
          )
          (exists (?x_4 )
            (and
              (AboveOf5 ?x_4)
              (BelowOf1 ?x_4)
            )
          )
          (exists (?x_9 )
            (and
              (LeftOf3 ?x_9)
              (RightOf5 ?x_9)
            )
          )
          (exists (?x_11 )
            (and
              (LeftOf1 ?x_11)
              (RightOf6 ?x_11)
            )
          )
          (exists (?x_8 )
            (and
              (RightOf2 ?x_8)
              (LeftOf2 ?x_8)
            )
          )
          (exists (?x_8 )
            (and
              (RightOf6 ?x_8)
              (LeftOf2 ?x_8)
            )
          )
          (exists (?x_9 )
            (and
              (LeftOf1 ?x_9)
              (RightOf5 ?x_9)
            )
          )
          (exists (?x_7 )
            (and
              (AboveOf6 ?x_7)
              (BelowOf2 ?x_7)
            )
          )
          (exists (?x_3 )
            (and
              (RightOf1 ?x_3)
              (LeftOf1 ?x_3)
            )
          )
          (exists (?x_10 )
            (and
              (AboveOf5 ?x_10)
              (BelowOf1 ?x_10)
            )
          )
          (exists (?x_4 )
            (and
              (AboveOf3 ?x_4)
              (BelowOf1 ?x_4)
            )
          )
          (exists (?x_9 )
            (and
              (LeftOf3 ?x_9)
              (RightOf3 ?x_9)
            )
          )
          (exists (?x_2 )
            (and
              (LeftOf4 ?x_2)
              (RightOf5 ?x_2)
            )
          )
          (exists (?x_7 )
            (and
              (AboveOf6 ?x_7)
              (BelowOf3 ?x_7)
            )
          )
          (exists (?x_0 )
            (and
              (BelowOf1 ?x_0)
              (AboveOf4 ?x_0)
            )
          )
          (exists (?x_2 )
            (and
              (RightOf5 ?x_2)
              (LeftOf2 ?x_2)
            )
          )
          (exists (?x_2 )
            (and
              (LeftOf3 ?x_2)
              (RightOf5 ?x_2)
            )
          )
          (exists (?x_0 )
            (and
              (BelowOf2 ?x_0)
              (AboveOf3 ?x_0)
            )
          )
          (exists (?x_7 )
            (and
              (AboveOf4 ?x_7)
              (BelowOf1 ?x_7)
            )
          )
          (exists (?x_7 )
            (and
              (BelowOf4 ?x_7)
              (AboveOf5 ?x_7)
            )
          )
          (exists (?x_4 )
            (and
              (AboveOf3 ?x_4)
              (BelowOf3 ?x_4)
            )
          )
          (exists (?x_7 )
            (and
              (AboveOf4 ?x_7)
              (BelowOf4 ?x_7)
            )
          )
          (exists (?x_9 )
            (and
              (LeftOf3 ?x_9)
              (RightOf4 ?x_9)
            )
          )
          (exists (?x_4 )
            (and
              (BelowOf3 ?x_4)
              (AboveOf6 ?x_4)
            )
          )
          (exists (?x_1 )
            (and
              (BelowOf2 ?x_1)
              (AboveOf6 ?x_1)
            )
          )
          (exists (?x_8 )
            (and
              (LeftOf1 ?x_8)
              (RightOf3 ?x_8)
            )
          )
          (exists (?x_9 )
            (and
              (LeftOf2 ?x_9)
              (RightOf4 ?x_9)
            )
          )
          (exists (?x_2 )
            (and
              (LeftOf2 ?x_2)
              (RightOf5 ?x_2)
            )
          )
          (exists (?x_0 )
            (and
              (BelowOf1 ?x_0)
              (AboveOf5 ?x_0)
            )
          )
          (exists (?x_3 )
            (and
              (RightOf3 ?x_3)
              (LeftOf1 ?x_3)
            )
          )
          (exists (?x_2 )
            (and
              (RightOf5 ?x_2)
              (LeftOf1 ?x_2)
            )
          )
          (exists (?x_1 )
            (and
              (BelowOf3 ?x_1)
              (AboveOf6 ?x_1)
            )
          )
          (exists (?x_8 )
            (and
              (RightOf2 ?x_8)
              (LeftOf1 ?x_8)
            )
          )
          (exists (?x_4 )
            (and
              (BelowOf2 ?x_4)
              (AboveOf6 ?x_4)
            )
          )
          (exists (?x_4 )
            (and
              (BelowOf1 ?x_4)
              (AboveOf6 ?x_4)
            )
          )
          (exists (?x_6 )
            (and
              (LeftOf5 ?x_6)
              (RightOf6 ?x_6)
            )
          )
          (exists (?x_3 )
            (and
              (RightOf5 ?x_3)
              (LeftOf1 ?x_3)
            )
          )
          (exists (?x_6 )
            (and
              (RightOf5 ?x_6)
              (LeftOf5 ?x_6)
            )
          )
          (exists (?x_0 )
            (and
              (AboveOf2 ?x_0)
              (BelowOf1 ?x_0)
            )
          )
          (exists (?x_4 )
            (and
              (AboveOf3 ?x_4)
              (BelowOf2 ?x_4)
            )
          )
          (exists (?x_8 )
            (and
              (RightOf5 ?x_8)
              (LeftOf1 ?x_8)
            )
          )
          (exists (?x_9 )
            (and
              (LeftOf2 ?x_9)
              (RightOf5 ?x_9)
            )
          )
          (exists (?x_6 )
            (and
              (RightOf5 ?x_6)
              (LeftOf3 ?x_6)
            )
          )
          (exists (?x_11 )
            (and
              (RightOf6 ?x_11)
              (LeftOf2 ?x_11)
            )
          )
          (exists (?x_1 )
            (and
              (AboveOf6 ?x_1)
              (BelowOf1 ?x_1)
            )
          )
          (exists (?x_4 )
            (and
              (AboveOf4 ?x_4)
              (BelowOf1 ?x_4)
            )
          )
          (exists (?x_5 )
            (and
              (AboveOf6 ?x_5)
              (BelowOf1 ?x_5)
            )
          )
          (exists (?x_2 )
            (and
              (RightOf6 ?x_2)
              (LeftOf2 ?x_2)
            )
          )
          (exists (?x_8 )
            (and
              (LeftOf2 ?x_8)
              (RightOf3 ?x_8)
            )
          )
          (exists (?x_9 )
            (and
              (LeftOf1 ?x_9)
              (RightOf3 ?x_9)
            )
          )
          (exists (?x_10 )
            (and
              (AboveOf3 ?x_10)
              (BelowOf1 ?x_10)
            )
          )
          (exists (?x_7 )
            (and
              (AboveOf6 ?x_7)
              (BelowOf1 ?x_7)
            )
          )
          (exists (?x_2 )
            (and
              (LeftOf4 ?x_2)
              (RightOf4 ?x_2)
            )
          )
          (exists (?x_8 )
            (and
              (RightOf5 ?x_8)
              (LeftOf2 ?x_8)
            )
          )
          (exists (?x_9 )
            (and
              (RightOf4 ?x_9)
              (LeftOf1 ?x_9)
            )
          )
          (exists (?x_5 )
            (and
              (BelowOf2 ?x_5)
              (AboveOf6 ?x_5)
            )
          )
          (exists (?x_3 )
            (and
              (RightOf2 ?x_3)
              (LeftOf1 ?x_3)
            )
          )
          (exists (?x_2 )
            (and
              (LeftOf1 ?x_2)
              (RightOf5 ?x_2)
            )
          )
          (exists (?x_2 )
            (and
              (RightOf6 ?x_2)
              (LeftOf1 ?x_2)
            )
          )
          (exists (?x_5 )
            (and
              (BelowOf6 ?x_5)
              (AboveOf6 ?x_5)
            )
          )
          (exists (?x_6 )
            (and
              (RightOf5 ?x_6)
              (LeftOf2 ?x_6)
            )
          )
          (exists (?x_3 )
            (and
              (RightOf4 ?x_3)
              (LeftOf1 ?x_3)
            )
          )
          (exists (?x_2 )
            (and
              (RightOf4 ?x_2)
              (LeftOf2 ?x_2)
            )
          )
          (exists (?x_2 )
            (and
              (RightOf4 ?x_2)
              (LeftOf1 ?x_2)
            )
          )
          (exists (?x_6 )
            (and
              (LeftOf3 ?x_6)
              (RightOf6 ?x_6)
            )
          )
          (exists (?x_11 )
            (and
              (RightOf6 ?x_11)
              (LeftOf4 ?x_11)
            )
          )
          (exists (?x_10 )
            (and
              (AboveOf4 ?x_10)
              (BelowOf1 ?x_10)
            )
          )
          (exists (?x_6 )
            (and
              (LeftOf1 ?x_6)
              (RightOf6 ?x_6)
            )
          )
          (exists (?x_0 )
            (and
              (BelowOf2 ?x_0)
              (AboveOf5 ?x_0)
            )
          )
          (exists (?x_7 )
            (and
              (AboveOf6 ?x_7)
              (BelowOf4 ?x_7)
            )
          )
          (exists (?x_1 )
            (and
              (AboveOf5 ?x_1)
              (BelowOf4 ?x_1)
            )
          )
          (exists (?x_0 )
            (and
              (BelowOf2 ?x_0)
              (AboveOf6 ?x_0)
            )
          )
          (exists (?x_10 )
            (and
              (AboveOf2 ?x_10)
              (BelowOf1 ?x_10)
            )
          )
          (exists (?x_7 )
            (and
              (BelowOf3 ?x_7)
              (AboveOf5 ?x_7)
            )
          )
          (exists (?x_7 )
            (and
              (BelowOf2 ?x_7)
              (AboveOf5 ?x_7)
            )
          )
          (exists (?x_6 )
            (and
              (LeftOf4 ?x_6)
              (RightOf6 ?x_6)
            )
          )
          (exists (?x_4 )
            (and
              (AboveOf4 ?x_4)
              (BelowOf2 ?x_4)
            )
          )
          (exists (?x_3 )
            (and
              (RightOf6 ?x_3)
              (LeftOf1 ?x_3)
            )
          )
          (exists (?x_8 )
            (and
              (RightOf4 ?x_8)
              (LeftOf1 ?x_8)
            )
          )
          (exists (?x_2 )
            (and
              (RightOf6 ?x_2)
              (LeftOf3 ?x_2)
            )
          )
          (exists (?x_10 )
            (and
              (AboveOf1 ?x_10)
              (BelowOf1 ?x_10)
            )
          )
          (exists (?x_1 )
            (and
              (BelowOf5 ?x_1)
              (AboveOf5 ?x_1)
            )
          )
          (exists (?x_10 )
            (and
              (AboveOf6 ?x_10)
              (BelowOf1 ?x_10)
            )
          )
          (exists (?x_0 )
            (and
              (BelowOf1 ?x_0)
              (AboveOf3 ?x_0)
            )
          )
          (exists (?x_7 )
            (and
              (BelowOf3 ?x_7)
              (AboveOf4 ?x_7)
            )
          )
        )
        (Error)
      )
    )
  )
)