#!/usr/bin/env python3
import subprocess
import sys

def check_heuristic(name):
    cmd = ["python", "-m", "pyperplan", f"--heuristic", name, "--help"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if "error: argument --heuristic" in result.stderr:
        return False
    return True

def main():
    heuristics = ["blind", "goalcount", "hmax", "hadd", "hff", "hsa", "lmcut", "landmark"]
    print("Checking available heuristics in pyperplan:")
    for h in heuristics:
        if check_heuristic(h):
            print(f"✓ {h}")
        else:
            print(f"✗ {h}")

if __name__ == "__main__":
    main()
