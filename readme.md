# A* and GBFS Planning Algorithm Benchmarks

This repository contains benchmark experiments comparing A* Search and Greedy Best-First Search (GBFS) algorithms with various delete-relaxation heuristics across multiple PDDL planning domains.

## Overview

This project evaluates the performance characteristics of classic planning algorithms on standard Planning Domain Definition Language (PDDL) domains:
- Blocksworld
- Gripper
- Monkey
- Ferry
- Logistics
- Hanoi (Towers of Hanoi)
- Travel

The experiments systematically compare:
- A* Search with multiple heuristics (hmax, hadd, hff, blind)
- GBFS with the same heuristic combinations
- Key performance metrics: runtime, expanded nodes, and plan length

## Methodology

I used Anthropic's Claude 3.7 Sonnet in conjunction with the filesystem MCP protocol to help rapidly prototype and debug to benchmark and visualize the results of different heuristics on PDDLs. This AI assistance was instrumental for:

- Setting up experiments and configuring the PyPerPlan library
- Automating runs across multiple domains and problem instances
- Processing results data and generating visualizations
- Debugging PDDL parsing issues

## Key Findings

The experiments confirm several theoretical expectations about delete-relaxation heuristics:

- GBFS with hff consistently performed fastest across domains, often finding satisficing but non-optimal solutions
- A* with hmax guaranteed optimality but at significantly higher computational cost
- The "plateau problem" was evident in domains like Blocksworld where delete-relaxation heuristics struggle
- Surprisingly, blind search occasionally outperformed heuristic-guided search in the Gripper domain
- Higher plan lengths were observed with GBFS compared to A*, especially using hadd and hff

## Repository Structure

- `/Benchmarks/`: PDDL domain and problem files organized by planning domain
- `/benchmark-visualizer.py`: Python script for generating visualizations from benchmark results
- `/benchmark_pddl.py`: Main benchmarking script that runs planning algorithms on PDDL domains
- `/benchmark_results.csv`: Raw results data from all benchmark runs
- `/check_heuristics.py`: Script to validate heuristic implementations

## Setup and Usage

### Environment Setup

1. Clone the repository
2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Benchmarks

To run benchmarks on the provided domains:
```bash
python benchmark_pddl.py /path/to/Benchmarks_directory
```

### Visualizing Results

To generate visualizations from benchmark results:
```bash
python benchmark-visualizer.py benchmark_results.csv
```

Visualization outputs will be saved in the `benchmark_analysis` directory.
