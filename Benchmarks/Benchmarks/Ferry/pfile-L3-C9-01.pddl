


(define (problem ferry-l3-c9)
(:domain ferry)
(:objects l0 l1 l2 
          c0 c1 c2 c3 c4 c5 c6 c7 c8 
)
(:init
(location l0)
(location l1)
(location l2)
(car c0)
(car c1)
(car c2)
(car c3)
(car c4)
(car c5)
(car c6)
(car c7)
(car c8)
(not-eq l0 l1)
(not-eq l1 l0)
(not-eq l0 l2)
(not-eq l2 l0)
(not-eq l1 l2)
(not-eq l2 l1)
(empty-ferry)
(at c0 l1)
(at c1 l2)
(at c2 l1)
(at c3 l2)
(at c4 l1)
(at c5 l2)
(at c6 l2)
(at c7 l0)
(at c8 l0)
(at-ferry l0)
)
(:goal
(and
(at c0 l0)
(at c1 l1)
(at c2 l1)
(at c3 l0)
(at c4 l0)
(at c5 l1)
(at c6 l1)
(at c7 l2)
(at c8 l0)
)
)
)


