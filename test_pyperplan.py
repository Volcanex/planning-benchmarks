#!/usr/bin/env python3
import subprocess
import sys

def run_test():
    # Test with domain file named "blockworld.pddl"
    cmd1 = ["python", "-m", "pyperplan", 
           "--search", "astar", 
           "--heuristic", "hmax",
           "/home/gabriel/Desktop/planning-benchmarks/Benchmarks/Benchmarks/blockworld/blockworld.pddl",
           "/home/gabriel/Desktop/planning-benchmarks/Benchmarks/Benchmarks/blockworld/pb2.pddl"]
    
    print("\nRunning command 1:", " ".join(cmd1))
    
    try:
        result = subprocess.run(cmd1, capture_output=True, text=True)
        print("Return code:", result.returncode)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    except Exception as e:
        print("Error:", str(e))
    
    # Create a copy with the correct domain name
    try:
        with open("/home/gabriel/Desktop/planning-benchmarks/Benchmarks/Benchmarks/blockworld/blockworld.pddl", 'r') as f:
            content = f.read()
        with open("/home/gabriel/Desktop/planning-benchmarks/Benchmarks/Benchmarks/blockworld/blocksworld.pddl", 'w') as f:
            f.write(content)
        print("\nCreated blocksworld.pddl as a copy of blockworld.pddl")
    except Exception as e:
        print("\nError creating domain file:", str(e))
    
    # Test with domain file named "blocksworld.pddl"
    cmd2 = ["python", "-m", "pyperplan", 
           "--search", "astar", 
           "--heuristic", "hmax",
           "/home/gabriel/Desktop/planning-benchmarks/Benchmarks/Benchmarks/blockworld/blocksworld.pddl",
           "/home/gabriel/Desktop/planning-benchmarks/Benchmarks/Benchmarks/blockworld/pb2.pddl"]
    
    print("\nRunning command 2:", " ".join(cmd2))
    
    try:
        result = subprocess.run(cmd2, capture_output=True, text=True)
        print("Return code:", result.returncode)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    except Exception as e:
        print("Error:", str(e))
        
if __name__ == "__main__":
    run_test()
