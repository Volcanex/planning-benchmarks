# Benchmark Results Analysis

## Overall Statistics

Total problems tested: 16
Total domains tested: 6
Algorithms tested: astar, gbf
Heuristics tested: hmax, hadd, hff, blind

## Success Rates

Success rate by algorithm and heuristic:

search heuristic  success  success_percent
 astar     blind     0.6%            56.7%
 astar      hadd     0.7%            66.7%
 astar       hff     0.7%            66.7%
 astar      hmax     0.5%            50.0%
   gbf      hadd     0.7%            66.7%
   gbf       hff     0.7%            66.7%
   gbf      hmax     0.6%            63.3%


## A* vs GBFS with h_max (Key Comparison)

Success Rate: A*+h_max: 50.0%, GBFS+h_max: 63.3%
Average Runtime: A*+h_max: 0.367s, GBFS+h_max: 0.573s
Average Plan Length: A*+h_max: 9.5, GBFS+h_max: 10.6
Average Expanded Nodes: A*+h_max: 1215.4, GBFS+h_max: 1001.7

## Analysis

GBFS with h_max has a higher success rate than A* with h_max by 13.3 percentage points.
A* with h_max is faster than GBFS with h_max by 0.206 seconds on average.
A* with h_max produces shorter plans than GBFS with h_max by 1.2 steps on average.
GBFS with h_max expands fewer nodes than A* with h_max by 213.7 nodes on average.