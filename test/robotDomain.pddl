(define (domain robot)
	(:requirements :ekab)
	(:predicates
		(Columns ?x)
		(Rows ?x)
		(Column0 ?x)
		(Column1 ?x)
		(Column2 ?x)
		(Column3 ?x)
		(Column4 ?x)
		(Column5 ?x)
		(Column6 ?x)
		(RightOf0 ?x)
		(RightOf1 ?x)
		(RightOf2 ?x)
		(RightOf3 ?x)
		(RightOf4 ?x)
		(RightOf5 ?x)
		(RightOf6 ?x)
		(LeftOf1 ?x)
		(LeftOf2 ?x)
		(LeftOf3 ?x)
		(LeftOf4 ?x)
		(LeftOf5 ?x)
		(LeftOf6 ?x)
		(LeftOf7 ?x)
		(Row0 ?x)
		(Row1 ?x)
		(Row2 ?x)
		(Row3 ?x)
		(Row4 ?x)
		(Row5 ?x)
		(Row6 ?x)
		(AboveOf0 ?x)
		(AboveOf1 ?x)
		(AboveOf2 ?x)
		(AboveOf3 ?x)
		(AboveOf4 ?x)
		(AboveOf5 ?x)
		(AboveOf6 ?x)
		(BelowOf1 ?x)
		(BelowOf2 ?x)
		(BelowOf3 ?x)
		(BelowOf4 ?x)
		(BelowOf5 ?x)
		(BelowOf6 ?x)
		(BelowOf7 ?x)
	)
	(:axioms
		(isA RightOf0 Columns)
		(isA RightOf1 RightOf0)
		(isA RightOf2 RightOf1)
		(isA RightOf3 RightOf2)
		(isA RightOf4 RightOf3)
		(isA RightOf5 RightOf4)
		(isA RightOf6 RightOf5)
		(isA LeftOf7 Columns)
		(isA LeftOf6 LeftOf7)
		(isA LeftOf5 LeftOf6)
		(isA LeftOf4 LeftOf5)
		(isA LeftOf3 LeftOf4)
		(isA LeftOf2 LeftOf3)
		(isA LeftOf1 LeftOf2)
		(isA AboveOf0 Rows)
		(isA AboveOf1 AboveOf0)
		(isA AboveOf2 AboveOf1)
		(isA AboveOf3 AboveOf2)
		(isA AboveOf4 AboveOf3)
		(isA AboveOf5 AboveOf4)
		(isA AboveOf6 AboveOf5)
		(isA BelowOf7 Rows)
		(isA BelowOf6 BelowOf7)
		(isA BelowOf5 BelowOf6)
		(isA BelowOf4 BelowOf5)
		(isA BelowOf3 BelowOf4)
		(isA BelowOf2 BelowOf3)
		(isA BelowOf1 BelowOf2)
		(isA LeftOf1 (not RightOf1))
		(isA LeftOf2 (not RightOf2))
		(isA LeftOf3 (not RightOf3))
		(isA LeftOf4 (not RightOf4))
		(isA LeftOf5 (not RightOf5))
		(isA LeftOf6 (not RightOf6))
		(isA AboveOf1 (not BelowOf1))
		(isA AboveOf2 (not BelowOf2))
		(isA AboveOf3 (not BelowOf3))
		(isA AboveOf4 (not BelowOf4))
		(isA AboveOf5 (not BelowOf5))
		(isA AboveOf6 (not BelowOf6))
	)
	(:rule ruleRight
		:condition (mko(Columns ?x))
		:action moveRight
	)
	(:rule ruleLeft
		:condition (mko(Columns ?x))
		:action moveLeft
	)
	(:rule ruleUp
		:condition (mko(Rows ?x))
		:action moveUp
	)
	(:rule ruleDown
		:condition (mko(Rows ?x))
		:action moveDown
	)
	(:action moveRight
		:parameters (?x)
		:effects 
		(
		:condition (mko (RightOf0 ?x))
		:add ((RightOf1 ?x))
		)
		(
		:condition (mko (RightOf1 ?x))
		:add ((RightOf2 ?x))
		)
		(
		:condition (mko (RightOf2 ?x))
		:add ((RightOf3 ?x))
		)
		(
		:condition (mko (RightOf3 ?x))
		:add ((RightOf4 ?x))
		)
		(
		:condition (mko (RightOf4 ?x))
		:add ((RightOf5 ?x))
		)
		(
		:condition (mko (RightOf5 ?x))
		:add ((RightOf6 ?x))
		)
		(
		:condition (mko (LeftOf1 ?x))
		:add ((LeftOf2 ?x))
		:delete ((LeftOf1 ?x))
		)
		(
		:condition (mko (LeftOf2 ?x))
		:add ((LeftOf3 ?x))
		:delete ((LeftOf2 ?x))
		)
		(
		:condition (mko (LeftOf3 ?x))
		:add ((LeftOf4 ?x))
		:delete ((LeftOf3 ?x))
		)
		(
		:condition (mko (LeftOf4 ?x))
		:add ((LeftOf5 ?x))
		:delete ((LeftOf4 ?x))
		)
		(
		:condition (mko (LeftOf5 ?x))
		:add ((LeftOf6 ?x))
		:delete ((LeftOf5 ?x))
		)
		(
		:condition (mko (LeftOf6 ?x))
		:add ((LeftOf7 ?x))
		:delete ((LeftOf6 ?x))
		)
		(
		:condition (mko (Column0 ?x))
		:add ((Column1 ?x))
		:delete ((Column0 ?x))
		)
		(
		:condition (mko (Column1 ?x))
		:add ((Column2 ?x))
		:delete ((Column1 ?x))
		)
		(
		:condition (mko (Column2 ?x))
		:add ((Column3 ?x))
		:delete ((Column2 ?x))
		)
		(
		:condition (mko (Column3 ?x))
		:add ((Column4 ?x))
		:delete ((Column3 ?x))
		)
		(
		:condition (mko (Column4 ?x))
		:add ((Column5 ?x))
		:delete ((Column4 ?x))
		)
		(
		:condition (mko (Column5 ?x))
		:add ((Column6 ?x))
		:delete ((Column5 ?x))
		)
		(
		:condition (mko (and (RightOf0 ?x) (LeftOf1 ?x)))
		:add ((Column1 ?x))
		)
		(
		:condition (mko (and (RightOf1 ?x) (LeftOf2 ?x)))
		:add ((Column2 ?x))
		)
		(
		:condition (mko (and (RightOf2 ?x) (LeftOf3 ?x)))
		:add ((Column3 ?x))
		)
		(
		:condition (mko (and (RightOf3 ?x) (LeftOf4 ?x)))
		:add ((Column4 ?x))
		)
		(
		:condition (mko (and (RightOf4 ?x) (LeftOf5 ?x)))
		:add ((Column5 ?x))
		)
		(
		:condition (mko (and (RightOf5 ?x) (LeftOf6 ?x)))
		:add ((Column6 ?x))
		)
	)
	(:action moveLeft
		:parameters (?x)
		:effects 
		(
		:condition (mko (LeftOf2 ?x))
		:add ((LeftOf1 ?x))
		)
		(
		:condition (mko (LeftOf3 ?x))
		:add ((LeftOf2 ?x))
		)
		(
		:condition (mko (LeftOf4 ?x))
		:add ((LeftOf3 ?x))
		)
		(
		:condition (mko (LeftOf5 ?x))
		:add ((LeftOf4 ?x))
		)
		(
		:condition (mko (LeftOf6 ?x))
		:add ((LeftOf5 ?x))
		)
		(
		:condition (mko (LeftOf7 ?x))
		:add ((LeftOf6 ?x))
		)
		(
		:condition (mko (RightOf1 ?x))
		:add ((RightOf0 ?x))
		:delete ((RightOf1 ?x))
		)
		(
		:condition (mko (RightOf2 ?x))
		:add ((RightOf1 ?x))
		:delete ((RightOf2 ?x))
		)
		(
		:condition (mko (RightOf3 ?x))
		:add ((RightOf2 ?x))
		:delete ((RightOf3 ?x))
		)
		(
		:condition (mko (RightOf4 ?x))
		:add ((RightOf3 ?x))
		:delete ((RightOf4 ?x))
		)
		(
		:condition (mko (RightOf5 ?x))
		:add ((RightOf4 ?x))
		:delete ((RightOf5 ?x))
		)
		(
		:condition (mko (RightOf6 ?x))
		:add ((RightOf5 ?x))
		:delete ((RightOf6 ?x))
		)
		(
		:condition (mko (Column1 ?x))
		:add ((Column0 ?x))
		:delete ((Column1 ?x))
		)
		(
		:condition (mko (Column2 ?x))
		:add ((Column1 ?x))
		:delete ((Column2 ?x))
		)
		(
		:condition (mko (Column3 ?x))
		:add ((Column2 ?x))
		:delete ((Column3 ?x))
		)
		(
		:condition (mko (Column4 ?x))
		:add ((Column3 ?x))
		:delete ((Column4 ?x))
		)
		(
		:condition (mko (Column5 ?x))
		:add ((Column4 ?x))
		:delete ((Column5 ?x))
		)
		(
		:condition (mko (Column6 ?x))
		:add ((Column5 ?x))
		:delete ((Column6 ?x))
		)
		(
		:condition (mko (and (RightOf1 ?x) (LeftOf2 ?x)))
		:add ((Column0 ?x))
		)
		(
		:condition (mko (and (RightOf2 ?x) (LeftOf3 ?x)))
		:add ((Column1 ?x))
		)
		(
		:condition (mko (and (RightOf3 ?x) (LeftOf4 ?x)))
		:add ((Column2 ?x))
		)
		(
		:condition (mko (and (RightOf4 ?x) (LeftOf5 ?x)))
		:add ((Column3 ?x))
		)
		(
		:condition (mko (and (RightOf5 ?x) (LeftOf6 ?x)))
		:add ((Column4 ?x))
		)
		(
		:condition (mko (and (RightOf6 ?x) (LeftOf7 ?x)))
		:add ((Column5 ?x))
		)
	)
	(:action moveUp
		:parameters (?x)
		:effects 
		(
		:condition (mko (AboveOf0 ?x))
		:add ((AboveOf1 ?x))
		)
		(
		:condition (mko (AboveOf1 ?x))
		:add ((AboveOf2 ?x))
		)
		(
		:condition (mko (AboveOf2 ?x))
		:add ((AboveOf3 ?x))
		)
		(
		:condition (mko (AboveOf3 ?x))
		:add ((AboveOf4 ?x))
		)
		(
		:condition (mko (AboveOf4 ?x))
		:add ((AboveOf5 ?x))
		)
		(
		:condition (mko (AboveOf5 ?x))
		:add ((AboveOf6 ?x))
		)
		(
		:condition (mko (BelowOf1 ?x))
		:add ((BelowOf2 ?x))
		:delete ((BelowOf1 ?x))
		)
		(
		:condition (mko (BelowOf2 ?x))
		:add ((BelowOf3 ?x))
		:delete ((BelowOf2 ?x))
		)
		(
		:condition (mko (BelowOf3 ?x))
		:add ((BelowOf4 ?x))
		:delete ((BelowOf3 ?x))
		)
		(
		:condition (mko (BelowOf4 ?x))
		:add ((BelowOf5 ?x))
		:delete ((BelowOf4 ?x))
		)
		(
		:condition (mko (BelowOf5 ?x))
		:add ((BelowOf6 ?x))
		:delete ((BelowOf5 ?x))
		)
		(
		:condition (mko (BelowOf6 ?x))
		:add ((BelowOf7 ?x))
		:delete ((BelowOf6 ?x))
		)
		(
		:condition (mko (Row0 ?x))
		:add ((Row1 ?x))
		:delete ((Row0 ?x))
		)
		(
		:condition (mko (Row1 ?x))
		:add ((Row2 ?x))
		:delete ((Row1 ?x))
		)
		(
		:condition (mko (Row2 ?x))
		:add ((Row3 ?x))
		:delete ((Row2 ?x))
		)
		(
		:condition (mko (Row3 ?x))
		:add ((Row4 ?x))
		:delete ((Row3 ?x))
		)
		(
		:condition (mko (Row4 ?x))
		:add ((Row5 ?x))
		:delete ((Row4 ?x))
		)
		(
		:condition (mko (Row5 ?x))
		:add ((Row6 ?x))
		:delete ((Row5 ?x))
		)
		(
		:condition (mko (and (AboveOf0 ?x) (BelowOf1 ?x)))
		:add ((Row1 ?x))
		)
		(
		:condition (mko (and (AboveOf1 ?x) (BelowOf2 ?x)))
		:add ((Row2 ?x))
		)
		(
		:condition (mko (and (AboveOf2 ?x) (BelowOf3 ?x)))
		:add ((Row3 ?x))
		)
		(
		:condition (mko (and (AboveOf3 ?x) (BelowOf4 ?x)))
		:add ((Row4 ?x))
		)
		(
		:condition (mko (and (AboveOf4 ?x) (BelowOf5 ?x)))
		:add ((Row5 ?x))
		)
		(
		:condition (mko (and (AboveOf5 ?x) (BelowOf6 ?x)))
		:add ((Row6 ?x))
		)
	)
	(:action moveDown
		:parameters (?x)
		:effects 
		(
		:condition (mko (BelowOf2 ?x))
		:add ((BelowOf1 ?x))
		)
		(
		:condition (mko (BelowOf3 ?x))
		:add ((BelowOf2 ?x))
		)
		(
		:condition (mko (BelowOf4 ?x))
		:add ((BelowOf3 ?x))
		)
		(
		:condition (mko (BelowOf5 ?x))
		:add ((BelowOf4 ?x))
		)
		(
		:condition (mko (BelowOf6 ?x))
		:add ((BelowOf5 ?x))
		)
		(
		:condition (mko (BelowOf7 ?x))
		:add ((BelowOf6 ?x))
		)
		(
		:condition (mko (AboveOf1 ?x))
		:add ((AboveOf0 ?x))
		:delete ((AboveOf1 ?x))
		)
		(
		:condition (mko (AboveOf2 ?x))
		:add ((AboveOf1 ?x))
		:delete ((AboveOf2 ?x))
		)
		(
		:condition (mko (AboveOf3 ?x))
		:add ((AboveOf2 ?x))
		:delete ((AboveOf3 ?x))
		)
		(
		:condition (mko (AboveOf4 ?x))
		:add ((AboveOf3 ?x))
		:delete ((AboveOf4 ?x))
		)
		(
		:condition (mko (AboveOf5 ?x))
		:add ((AboveOf4 ?x))
		:delete ((AboveOf5 ?x))
		)
		(
		:condition (mko (AboveOf6 ?x))
		:add ((AboveOf5 ?x))
		:delete ((AboveOf6 ?x))
		)
		(
		:condition (mko (Row1 ?x))
		:add ((Row0 ?x))
		:delete ((Row1 ?x))
		)
		(
		:condition (mko (Row2 ?x))
		:add ((Row1 ?x))
		:delete ((Row2 ?x))
		)
		(
		:condition (mko (Row3 ?x))
		:add ((Row2 ?x))
		:delete ((Row3 ?x))
		)
		(
		:condition (mko (Row4 ?x))
		:add ((Row3 ?x))
		:delete ((Row4 ?x))
		)
		(
		:condition (mko (Row5 ?x))
		:add ((Row4 ?x))
		:delete ((Row5 ?x))
		)
		(
		:condition (mko (Row6 ?x))
		:add ((Row5 ?x))
		:delete ((Row6 ?x))
		)
		(
		:condition (mko (and (AboveOf1 ?x) (BelowOf2 ?x)))
		:add ((Row0 ?x))
		)
		(
		:condition (mko (and (AboveOf2 ?x) (BelowOf3 ?x)))
		:add ((Row1 ?x))
		)
		(
		:condition (mko (and (AboveOf3 ?x) (BelowOf4 ?x)))
		:add ((Row2 ?x))
		)
		(
		:condition (mko (and (AboveOf4 ?x) (BelowOf5 ?x)))
		:add ((Row3 ?x))
		)
		(
		:condition (mko (and (AboveOf5 ?x) (BelowOf6 ?x)))
		:add ((Row4 ?x))
		)
		(
		:condition (mko (and (AboveOf6 ?x) (BelowOf7 ?x)))
		:add ((Row5 ?x))
		)
	)

)