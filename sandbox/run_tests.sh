#!/bin/bash
set -e

TESTS_DIR=${1:-tests}

echo "🚀 Running tests..."
pytest "$TESTS_DIR" --json-report --json-report-file=.test_report.json --tb=short -v

if [ -f .test_report.json ]; then
    echo "=== PYTEST SUMMARY ==="
    python3 -c "
import json
with open('.test_report.json','r') as f:
    report = json.load(f)
    summary = report.get('summary', {})
    print(f'total: {summary.get("total",0)} passed: {summary.get("passed",0)} failed: {summary.get("failed",0)}')
"
fi
