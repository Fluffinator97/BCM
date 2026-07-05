# CAN Parser Starter

Minimal Linux VM starter project for parsing candump-style CAN logs.

## Recommended VM
Use Ubuntu Server/Desktop, Debian, EndeavourOS, or Arch.

## Setup
```bash
chmod +x setup.sh
./setup.sh
source .venv/bin/activate
python main.py logs/sample.log
pytest
```

## Sample candump format
```text
(1719672101.123456) can0 123#DEADBEEF
```

