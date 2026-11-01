import subprocess
import sys
import os
import time

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

print("=" * 65)
print("  WAF Week-8 Laboratory Applications Launcher")
print("=" * 65)
print("  Part (a) Student Info & Git Branching:    http://127.0.0.1:5001/")
print("  Part (b) Student Info & GitHub Workflow:  http://127.0.0.1:5002/")
print("  Part (c) Online Course Registration:      http://127.0.0.1:5003/")
print("=" * 65)
print("  Press Ctrl+C to terminate all servers.")
print("=" * 65)

py_exec = sys.executable

procs = [
    subprocess.Popen([py_exec, os.path.join(BASE_DIR, "part_a", "app.py")]),
    subprocess.Popen([py_exec, os.path.join(BASE_DIR, "part_b", "app.py")]),
    subprocess.Popen([py_exec, os.path.join(BASE_DIR, "part_c", "app.py")])
]

try:
    for p in procs:
        p.wait()
except KeyboardInterrupt:
    print("\nShutting down all applications...")
    for p in procs:
        p.terminate()
