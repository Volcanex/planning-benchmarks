#!/usr/bin/env python3
"""
PDDL Benchmark Script

This script runs benchmarks on PDDL domain and problem files using
pyperplan with different search algorithms and heuristics.
Results are saved to a CSV file for easy analysis.
"""

import os
import subprocess
import time
import csv
import re
import argparse
from collections import defaultdict
import glob

# Default search algorithms and heuristics to test
DEFAULT_SEARCHES = ["astar", "gbf"]
DEFAULT_HEURISTICS = ["hmax", "hadd", "hff", "blind"]

def run_benchmark(domain_file, problem_file, search, heuristic, timeout=5):
    """Run a single benchmark with the given parameters."""
    cmd = ["python", "-m", "pyperplan"]
    
    if search:
        cmd.extend(["--search", search])
    
    if heuristic:
        cmd.extend(["--heuristic", heuristic])
    
    cmd.extend([domain_file, problem_file])
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        elapsed = time.time() - start_time
        
        # Parse the output to extract stats
        stats = {
            "domain": os.path.basename(domain_file).replace(".pddl", ""),
            "problem": os.path.basename(problem_file).replace(".pddl", ""),
            "search": search or "breadth_first_search",
            "heuristic": heuristic or "None",
            "success": "Goal reached" in result.stdout,
            "runtime": elapsed,
            "expanded_nodes": 0,
            "plan_length": 0
        }
        
        # Extract expanded nodes
        nodes_match = re.search(r"(\d+) Nodes expanded", result.stdout)
        if nodes_match:
            stats["expanded_nodes"] = int(nodes_match.group(1))
        
        # Extract plan length
        length_match = re.search(r"Plan length: (\d+)", result.stdout)
        if length_match:
            stats["plan_length"] = int(length_match.group(1))

        print(f"STDERR: {result.stderr}")
            
        return stats
    
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        return {
            "domain": os.path.basename(domain_file).replace(".pddl", ""),
            "problem": os.path.basename(problem_file).replace(".pddl", ""),
            "search": search or "breadth_first_search",
            "heuristic": heuristic or "None",
            "success": False,
            "runtime": elapsed,
            "expanded_nodes": "timeout",
            "plan_length": "timeout"
        }
    except Exception as e:
        return {
            "domain": os.path.basename(domain_file).replace(".pddl", ""),
            "problem": os.path.basename(problem_file).replace(".pddl", ""),
            "search": search or "breadth_first_search",
            "heuristic": heuristic or "None",
            "success": False,
            "runtime": time.time() - start_time,
            "expanded_nodes": f"error: {str(e)}",
            "plan_length": f"error: {str(e)}"
        }

def read_domain_name_from_file(file_path):
    """Extract domain name from a PDDL file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            domain_match = re.search(r'\(:domain\s+([^)]+)\)', content)
            if domain_match:
                return domain_match.group(1).strip()
    except Exception:
        pass
    return None

def find_domain_file_for_problem(problem_file):
    """Find the domain file for a given problem file using the domain name in the problem file."""
    problem_dir = os.path.dirname(problem_file)
    
    # Try to read the domain name from the problem file
    domain_name = None
    try:
        with open(problem_file, 'r') as f:
            content = f.read()
            domain_match = re.search(r'\(:domain\s+([^)]+)\)', content)
            if domain_match:
                domain_name = domain_match.group(1).strip()
    except Exception:
        pass
        
    # Handle domain name variants/typos
    variants = [domain_name] if domain_name else []
    if domain_name == "blocksworld":
        variants.append("blockworld")
    elif domain_name == "blockworld":
        variants.append("blocksworld")
        
    # Try domain name variants first
    for variant in variants:
        file_path = os.path.join(problem_dir, f"{variant}.pddl")
        if os.path.exists(file_path):
            return file_path
            
    # Try standard patterns
    patterns = [
        "domain.pddl",
        f"{domain_name}.pddl" if domain_name else None,
        "*domain*.pddl",
        "*.domain.pddl",
        os.path.basename(problem_dir) + ".pddl"  # Named after directory
    ]
    
    # Filter out None values
    patterns = [p for p in patterns if p]
    
    # Try each pattern in the problem directory
    for pattern in patterns:
        candidates = glob.glob(os.path.join(problem_dir, pattern))
        if candidates:
            return candidates[0]
    
    # If still not found, look for any PDDL file that's not a problem file
    all_pddls = glob.glob(os.path.join(problem_dir, "*.pddl"))
    for pddl in all_pddls:
        if pddl != problem_file and os.path.isfile(pddl):
            # Check if it's a domain file by looking for :action definition
            try:
                with open(pddl, 'r') as f:
                    content = f.read()
                    if ":action" in content and "(:goal" not in content:
                        return pddl
            except Exception:
                pass
    
    # If still not found, try the parent directory
    parent_dir = os.path.dirname(problem_dir)
    for pattern in patterns:
        candidates = glob.glob(os.path.join(parent_dir, pattern))
        if candidates:
            return candidates[0]
            
    return None

def is_problem_file(file_path):
    """Check if a file is a PDDL problem file by checking content."""
    try:
        with open(file_path, 'r') as f:
            content = f.read(2000)  # Read enough to check format
            # Simple check for problem definition structure
            if "(:goal" in content and "(define" in content and "problem" in content:
                return True
    except Exception:
        pass
    return False



def find_problem_files(directory):
    """Find all problem files in a directory."""
    problem_files = []
    
    # Get all PDDL files in the directory
    all_pddls = glob.glob(os.path.join(directory, "*.pddl"))
    
    # Filter for problem files
    for pddl in all_pddls:
        if is_problem_file(pddl):
            problem_files.append(pddl)
            
    return problem_files

def main():
    parser = argparse.ArgumentParser(description="Run PDDL benchmarks with pyperplan")
    parser.add_argument("benchmark_dir", help="Directory containing benchmark domains")
    parser.add_argument("--searches", nargs="+", default=DEFAULT_SEARCHES, 
                        help="Search algorithms to benchmark")
    parser.add_argument("--heuristics", nargs="+", default=DEFAULT_HEURISTICS,
                        help="Heuristics to benchmark")
    parser.add_argument("--domains", nargs="+", default=None,
                        help="Specific domains to test (filter by name)")
    parser.add_argument("--timeout", type=int, default=5,
                        help="Timeout in seconds for each run")
    parser.add_argument("--output", default="benchmark_results.csv",
                        help="Output CSV file")
    parser.add_argument("--max-problems", type=int, default=10,
                        help="Maximum number of problems to test per domain")
    parser.add_argument("--test-invalid", action="store_true",
                        help="Test combinations that might be invalid (like blind with non-astar)")
    parser.add_argument("--debug", action="store_true",
                        help="Print additional debug information")
    
    args = parser.parse_args()
    
    # Check if benchmark_dir is a specific domain directory or a parent directory
    if os.path.isdir(args.benchmark_dir):
        if any(os.path.isfile(os.path.join(args.benchmark_dir, f)) and f.endswith('.pddl') 
               for f in os.listdir(args.benchmark_dir)):
            # This is a domain directory
            domain_dirs = [args.benchmark_dir]
        else:
            # This is a parent directory, find all subdirectories
            domain_dirs = [os.path.join(args.benchmark_dir, d) 
                         for d in os.listdir(args.benchmark_dir)
                         if os.path.isdir(os.path.join(args.benchmark_dir, d)) and not d.startswith('.')]
            
            # Filter by domain name if specified
            if args.domains:
                domain_dirs = [d for d in domain_dirs 
                              if any(domain.lower() in os.path.basename(d).lower() 
                                    for domain in args.domains)]
    else:
        print(f"Error: {args.benchmark_dir} is not a directory")
        return
        
    results = []
    
    for domain_dir in domain_dirs:
        domain_name = os.path.basename(domain_dir)
        print(f"\nProcessing domain directory: {domain_name}")
        
        # Find all problem files in this domain directory
        problem_files = find_problem_files(domain_dir)
        
        if not problem_files:
            print(f"  No problem files found in {domain_dir}")
            continue
            
        # Sort problem files based on numeric identifiers if present
        def problem_sort_key(path):
            filename = os.path.basename(path)
            numbers = re.findall(r'\d+', filename)
            if numbers:
                return int(numbers[0])
            return filename
            
        problem_files.sort(key=problem_sort_key)
        
        # Limit to max problems
        problem_files = problem_files[:args.max_problems]
        
        domain_problems_run = 0
        
        for problem_file in problem_files:
            # Find the domain file for this problem
            domain_file = find_domain_file_for_problem(problem_file)
            
            if not domain_file:
                # Try to create blocksworld file if problem states blocksworld but only blockworld file exists
                domain_name = read_domain_name_from_file(problem_file)
                if domain_name == "blocksworld" and os.path.exists(os.path.join(problem_dir, "blockworld.pddl")):
                    src = os.path.join(problem_dir, "blockworld.pddl")
                    dst = os.path.join(problem_dir, "blocksworld.pddl")
                    try:
                        with open(src, 'r') as f:
                            content = f.read()
                        with open(dst, 'w') as f:
                            f.write(content)
                        print(f"  Created {dst} as a copy of {src}")
                        domain_file = dst
                    except Exception as e:
                        print(f"  Warning: Could not create domain file: {e}")
                else:
                    print(f"  Warning: Could not find domain file for {os.path.basename(problem_file)}")
                    domain_name = read_domain_name_from_file(problem_file)
                    print(f"  Problem requires domain: {domain_name}")
                    
                continue
                
            print(f"\nBenchmarking domain: {domain_name}")
            print(f"  Problem: {os.path.basename(problem_file)}")
            print(f"  Domain file: {os.path.basename(domain_file)}")
            
            if args.debug:
                # Extract domain name from problem file
                with open(problem_file, 'r') as f:
                    content = f.read()
                    domain_match = re.search(r'\(:domain\s+([^)]+)\)', content)
                    if domain_match:
                        stated_domain = domain_match.group(1).strip()
                        print(f"  Stated domain name in problem: {stated_domain}")
            
            domain_problems_run += 1
            
            for search in args.searches:
                for heuristic in args.heuristics:
                    # Skip invalid combinations
                    if not args.test_invalid:
                        if heuristic == "blind" and search != "astar":
                            continue
                            
                    print(f"    Running {search} with {heuristic}...")
                    
                    stats = run_benchmark(
                        domain_file, 
                        problem_file, 
                        search, 
                        heuristic,
                        timeout=args.timeout
                    )
                    results.append(stats)
                    
                    if isinstance(stats["expanded_nodes"], int):
                        expanded = str(stats["expanded_nodes"])
                    else:
                        expanded = stats["expanded_nodes"]
                        
                    if isinstance(stats["plan_length"], int):
                        plan_len = str(stats["plan_length"])
                    else:
                        plan_len = stats["plan_length"]
                        
                    status = "✓" if stats["success"] else "✗"
                    print(f"      {status} Runtime: {stats['runtime']:.3f}s, "
                          f"Expanded: {expanded}, "
                          f"Plan length: {plan_len}")
    
    # Write results to CSV
    if results:
        with open(args.output, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"\nResults saved to {args.output}")
        
        # Print summary
        print("\nSummary:")
        by_search_heuristic = defaultdict(list)
        for r in results:
            key = (r["search"], r["heuristic"])
            by_search_heuristic[key].append(r)
        
        print(f"{'Search':<15} {'Heuristic':<10} {'Success Rate':<15} {'Avg Runtime':<15} {'Avg Plan Length':<15}")
        for (search, heuristic), runs in by_search_heuristic.items():
            success_rate = sum(1 for r in runs if r["success"]) / len(runs) if runs else 0
            successful = [r for r in runs if r["success"]]
            avg_runtime = sum(r["runtime"] for r in successful) / len(successful) if successful else float('inf')
            
            # Only count numeric plan lengths
            plan_lengths = [r["plan_length"] for r in successful if isinstance(r["plan_length"], int)]
            avg_plan_length = sum(plan_lengths) / len(plan_lengths) if plan_lengths else 'N/A'
            
            print(f"{search:<15} {heuristic:<10} {success_rate*100:.1f}%{' ':9} {avg_runtime:<15.3f} {avg_plan_length}")
    else:
        print("No results collected.")

if __name__ == "__main__":
    main()