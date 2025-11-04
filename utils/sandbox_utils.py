
import os, subprocess, json

def _docker_path(path):
    path = os.path.abspath(path)
    if path[1:3] == ":\\":
        drive = path[0].lower()
        path = path[2:].replace("\\", "/")
        return f"/{drive}{path}"
    return path

def run_in_sandbox(test_path="tests", image="devagent-sandbox:latest"):
    repo = os.path.abspath(".")
    docker_path = _docker_path(repo)
    cmd = [
        "docker", "run", "--rm", "--network", "none", "--memory", "512m",
        "-v", f"{docker_path}:/workspace", "-w", "/workspace",
        "-e", "PYTHONPATH=/workspace", image,
        "bash", "-c", f"bash sandbox/run_tests.sh {test_path}"
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    report = None
    if os.path.exists(".test_report.json"):
        try:
            report = json.load(open(".test_report.json", "r", encoding="utf-8"))
        except Exception:
            pass
    return {"stdout": p.stdout, "stderr": p.stderr, "report": report}

def apply_patch(patch_text, filename="agent_patch.diff"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(patch_text)
    r = subprocess.run(["git", "apply", filename], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git apply failed: {r.stderr}")
    os.remove(filename)
