# Benchmark Results Analysis

## Overall Statistics

Total problems tested: 10
Total domains tested: 2
Algorithms tested: astar, gbf
Heuristics tested: hmax, hadd, hff, blind, landmark, lmcut

## Success Rates

Success rate by algorithm and heuristic:

search heuristic  success  success_percent
 astar     blind     0.7%            70.0%
 astar      hadd     0.8%            80.0%
 astar       hff     0.7%            70.0%
 astar      hmax     0.6%            60.0%
 astar  landmark     0.8%            80.0%
 astar     lmcut     0.4%            40.0%
   gbf      hadd     0.5%            50.0%
   gbf       hff     0.5%            50.0%
   gbf      hmax     0.4%            40.0%
   gbf  landmark     0.5%            50.0%
   gbf     lmcut     0.5%            50.0%


## A* vs GBFS with h_max (Key Comparison)

Success Rate: A*+h_max: 60.0%, GBFS+h_max: 40.0%
Average Runtime: A*+h_max: 0.738s, GBFS+h_max: 0.113s
Average Plan Length: A*+h_max: 12.5, GBFS+h_max: 9.5
Average Expanded Nodes: A*+h_max: 1235.5, GBFS+h_max: 461.5

## Analysis

A* with h_max has a higher success rate than GBFS with h_max by 20.0 percentage points.
GBFS with h_max is faster than A* with h_max by 0.625 seconds on average.
GBFS with h_max produces shorter plans than A* with h_max by 3.0 steps on average.
GBFS with h_max expands fewer nodes than A* with h_max by 774.0 nodes on average.