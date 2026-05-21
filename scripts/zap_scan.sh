#!/usr/bin/env bash
# OWASP ZAP baseline security scan against the AIOpsCare API.
# Usage: bash scripts/zap_scan.sh [target_url]

TARGET=${1:-"http://localhost:8000"}
REPORT_DIR="docs/security"
REPORT_FILE="$REPORT_DIR/zap-report.html"

mkdir -p "$REPORT_DIR"

echo "Running OWASP ZAP baseline scan against $TARGET ..."

docker run --rm \
  --network host \
  -v "$(pwd)/$REPORT_DIR:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
    -t "$TARGET" \
    -r "zap-report.html" \
    -I

echo "Report saved to $REPORT_FILE"
