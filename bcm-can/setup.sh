#!/usr/bin/env bash
set -e

echo "[1/4] Installing system packages..."
if command -v apt >/dev/null 2>&1; then
  sudo apt update
  sudo apt install -y python3 python3-venv python3-pip git can-utils
elif command -v pacman >/dev/null 2>&1; then
  sudo pacman -Sy --needed python python-pip git can-utils
else
  echo "Unsupported package manager. Install python3, pip, git, can-utils manually."
fi

echo "[2/4] Creating Python virtual environment..."
python3 -m venv .venv

echo "[3/4] Installing Python packages..."
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[4/4] Done."
echo "Run: source .venv/bin/activate && python main.py logs/sample.log"
