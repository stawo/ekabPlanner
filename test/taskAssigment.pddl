(define (domain taskAssigment)
  (:requirements :ekab)

(:predicates 
	(Employee ?x)
	(Engineer ?x)
	(Designer ?x)
	(Developer ?x)
	(ElectronicEngineer ?x)
	(InformaticEngineer ?x)
	(MaterialsEngineer ?x)
	(TaskAgent ?x)
	(ElectronicsAgent ?x)
	(SoftwareAgent ?x)
	(DesignAgent ?x)
	(MaterialsAgent ?x)
	(TestingAgent ?x)
	(CodingAgent ?x)
	(SpecificationsAgent ?x)
	(FullName ?x)
	(hasPersonalInfo ?x ?y)
)

(:axioms
  (isA	Engineer Employee)
  (isA	Designer Employee)
  (isA	Developer Employee)
  (isA	ElectronicEngineer Engineer)
  (isA	InformaticEngineer Engineer)
  (isA	MaterialsEngineer Engineer)
  (isA	TaskAgent Employee)
  (isA	ElectronicsAgent TaskAgent)
  (isA	SoftwareAgent TaskAgent)
  (isA	DesignAgent TaskAgent)
  (isA	TestingAgent TaskAgent)
  (isA	MaterialsAgent DesignAgent)
  (isA	CodingAgent SoftwareAgent)
  (isA	SpecificationsAgent SoftwareAgent)
  (isA  (exists hasPersonalInfo) Employee)
  (isA  Employee (exists hasPersonalInfo))
  (isA  (exists (inverse hasPersonalInfo)) FullName)
  (isA	Designer (not ElectronicsAgent))
  (isA	Designer (not SoftwareAgent))
  (isA	MaterialsEngineer (not SoftwareAgent))
  (isA	MaterialsEngineer (not ElectronicsAgent))
  (isA	InformaticEngineer (not ElectronicsAgent))
  (isA	ElectronicEngineer (not CodingAgent))
  (isA	Developer (not SpecificationsAgent))
  (isA	FullName (not Employee))
  (isA	InformaticEngineer (not ElectronicEngineer))
  
)

(:rule rule_hireElectronicEng
:condition (:True)
:action hireElectronicEng
)

(:rule rule_hireInformaticEng
:condition (:True)
:action hireInformaticEng
)

(:rule rule_assignTaskAgent
:condition (mko (Employee ?x))
:action assignTaskAgent
)

(:rule rule_assignElectronicsAgent
:condition (mko (Employee ?x))
:action assignElectronicsAgent
)

(:rule rule_assignSoftwareAgent
:condition (mko (Employee ?x))
:action assignSoftwareAgent
)

(:rule rule_assignDesignAgent
:condition (mko (Employee ?x))
:action assignDesignAgent
)

(:rule rule_assignTestingAgent
:condition (mko (Employee ?x))
:action assignTestingAgent
)

(:rule rule_assignMaterialsAgent
:condition (mko (Employee ?x))
:action assignMaterialsAgent
)

(:rule rule_assignCodingAgent
:condition (mko (Employee ?x))
:action assignCodingAgent
)

(:rule rule_assignSpecificationsAgent
:condition (mko (Employee ?x))
:action assignSpecificationsAgent
)

(:rule rule_removePersonalInfo
:condition (mko (hasPersonalInfo ?x ?y))
:action removePersonalInfo
)


(:action hireElectronicEng
  :parameters (?n)
  :effects (
    :condition (not
		(exists (?x1 ?x2 ?x3) 
			(and
				(mko (ElectronicEngineer ?x1))
				(mko (ElectronicEngineer ?x2))
				(mko (ElectronicEngineer ?x3))
				(not (mko-eq ?x1 ?x2))
				(not (mko-eq ?x1 ?x3))
				(not (mko-eq ?x2 ?x3))
			)
		)
	)
    :add ((ElectronicEngineer ?n))
  )

)
  
(:action hireInformaticEng
  :parameters (?n)
  :effects (
    :condition (not
		(exists (?x1 ?x2 ?x3) 
			(and
				(mko (InformaticEngineer ?x1))
				(mko (InformaticEngineer ?x2))
				(mko (InformaticEngineer ?x3))
				(not (mko-eq ?x1 ?x2))
				(not (mko-eq ?x1 ?x3))
				(not (mko-eq ?x2 ?x3))
			)
		)
	)
    :add ((InformaticEngineer ?n))
  )

)
 
(:action assignTaskAgent
  :parameters (?x)
  :effects (
    :condition (:True)
    :add ((TaskAgent ?x))
  )

)
 
(:action assignElectronicsAgent
  :parameters (?x)
  :effects (
    :condition (:True)
    :add ((ElectronicsAgent ?x))
  )

)
 
(:action assignSoftwareAgent
  :parameters (?x)
  :effects (
    :condition (:True)
    :add ((SoftwareAgent ?x))
  )

)
 
(:action assignDesignAgent
  :parameters (?x)
  :effects (
    :condition (:True)
    :add ((DesignAgent ?x))
  )

)
 
(:action assignTestingAgent
  :parameters (?x)
  :effects (
    :condition (:True)
    :add ((TestingAgent ?x))
  )

)
 
(:action assignMaterialsAgent
  :parameters (?x)
  :effects (
    :condition (:True)
    :add ((MaterialsAgent ?x))
  )

)
 
(:action assignCodingAgent
  :parameters (?x)
  :effects (
    :condition (:True)
    :add ((CodingAgent ?x))
  )

)
 
(:action assignSpecificationsAgent
  :parameters (?x)
  :effects (
    :condition (:True)
    :add ((SpecificationsAgent ?x))
  )

)
 
(:action removePersonalInfo
  :parameters (?x ?y)
  :effects (
    :condition (:True)
    :delete ((hasPersonalInfo ?x ?y))
  )

)
 

)

