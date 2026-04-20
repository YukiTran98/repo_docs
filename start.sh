#!/usr/bin/env bash
# start.sh — Khởi động Repo Docs Hub (live-scan mode)
# Usage: ./start.sh [port]
# Default port: 8080
#
# Live-scan: thêm repo mới vào docs/ → F5 là thấy ngay, không cần restart.

set -e

PORT="${1:-8080}"
DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$DIR"

# Kiểm tra Python
if ! command -v python3 &>/dev/null; then
  echo "python3 không tìm thấy. Cài Python 3 trước."
  exit 1
fi

# Khởi động live-scan server
python3 server.py "$PORT"
