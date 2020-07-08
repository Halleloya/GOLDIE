"""
Starting scripts for running all directories all together.

"""
import subprocess

level_names = ["level1", "level2", "level3", "level4a", "level4b", "level5a", "level5b"]

processes = [subprocess.Popen(["python", "./run.py", "--level", level_name]) for level_name in level_names]

for p in processes:
    p.wait()

