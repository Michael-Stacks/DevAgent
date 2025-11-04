#!/usr/bin/env python3
import os, sys, subprocess, json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCKER_IMAGE = "devagent-sandbox:latest"
TESTS_PATH = "tests"

def to_docker_path(host_path: str) -> str:
    host = os.path.abspath(host_path)
    if os.name == "nt" or (len(host) > 1 and host[1:3] == ':\\'):
        drive = host[0].lower()
        path_part = host[2:].replace("\\","/")
        return f"/{drive}{path_part}"
    return host

def run_in_docker():
    docker_host = to_docker_path(REPO_ROOT)
    cmd = [
        "docker", "run", "--rm",
        "--network", "none",
        "--memory", "512m",
        "--pids-limit", "64",
        "-e", "PYTHONPATH=/workspace",
        "-v", f"{docker_host}:/workspace:rw",
        "-w", "/workspace",
        DOCKER_IMAGE,
        "bash", "-c", f"bash sandbox/run_tests.sh {TESTS_PATH}"
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc

def parse_report():
    report_path = os.path.join(REPO_ROOT, ".test_report.json")
    if not os.path.exists(report_path):
        return None
    with open(report_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    print("Running tests in sandbox (docker image:", DOCKER_IMAGE, ")")
    proc = run_in_docker()
    print(proc.stdout)
    if proc.stderr:
        print("=== STDERR ===", file=sys.stderr)
        print(proc.stderr, file=sys.stderr)

    report = parse_report()
    if report:
        s = report.get("summary", {})
        total = s.get("total", 0)
        passed = s.get("passed", 0)
        failed = s.get("failed", 0)
        print("TEST REPORT SUMMARY:", {"total": total, "passed": passed, "failed": failed})
        if total > 0 and failed == 0:
            print("All tests passed ✅")
            sys.exit(0)
        else:
            print("Some tests failed ❌", file=sys.stderr)
            sys.exit(2)
    else:
        # fallback: use returncode
        if proc.returncode == 0:
            print("No JSON report but docker returned 0 — assume success")
            sys.exit(0)
        else:
            print("No JSON report and docker returned code", proc.returncode, file=sys.stderr)
            sys.exit(2)

if __name__ == "__main__":
    main()
