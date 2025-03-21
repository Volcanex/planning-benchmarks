# A* and GBFS Planning Algorithm Benchmarks

This repository contains benchmark experiments comparing A* Search and Greedy Best-First Search (GBFS) algorithms with various delete-relaxation heuristics across multiple PDDL planning domains.

## Overview

This was used to create graphs as supporting evidence and exploration of claims to do with delete-relaxation heuristics and algorithms on standard Planning Domain Definition Language (PDDL) domains:

- Blocksworld
- Gripper
- Monkey
- Ferry

- Others were problematic perhaps due to PDDL formatting differences between them and the libary. 

## Methodology

I used Anthropic's Claude 3.7 Sonnet in conjunction with the filesystem MCP protocol to help rapidly prototype and debug to benchmark and visualize the results of different heuristics on PDDLs. I provided high-level guidence, ajusted paramters and made key edits however the majority of this code is AI written. 

## Repo Structure

- `/Benchmarks/`: PDDL domain and problem files organized by planning domain
- `/benchmark-visualizer.py`: Python script for generating visualizations from benchmark results
- `/benchmark_pddl.py`: Main benchmarking script that runs planning algorithms on PDDL domains
- `/benchmark_results.csv`: Raw results data from all benchmark runs
- `/check_heuristics.py`: Script to validate heuristic implementations
- `/benchmark_analysis/`: Output folder

## Usage

```bash
# Run benchmarks on a specific domain
python benchmark_pddl.py /path/to/Benchmarks_directory
# Visualize results
python benchmark-visualizer.py benchmark_results.csv
```