# BCM Platform

A modular CAN telemetry, replay, and dashboard platform built for learning, experimentation, and future automotive BCM integration.

---

# Overview

This project started as a way to learn:

- CAN bus parsing
- Telemetry decoding
- Real-time dashboards
- Backend/frontend architecture
- Replay systems
- Signal validation
- Automotive-style telemetry pipelines

The long-term goal is to evolve this into a complete modular BCM ecosystem capable of:

- Live CAN monitoring
- Vehicle telemetry dashboards
- Alert systems
- Historical replay
- Data logging
- Signal editing/configuration
- Hardware integration
- Custom infotainment/vehicle control systems

---

# Current Features

## CAN Parsing
- Parse candump-style logs
- Decode CAN IDs into human-readable telemetry
- Support for:
  - scaling
  - signed values
  - enums
  - validation
  - alerts
  - units

## Replay System
- Replay CAN logs in real time
- Adjustable replay speed
- Simulated live telemetry updates

## Telemetry Dashboard
- Terminal-based dashboard
- System grouping
- Status indicators
- Signal ordering
- Live updates

## Backend API
Built with FastAPI.

Features:
- Live telemetry endpoint
- Replay control endpoint
- Signal metadata endpoint
- Hidden/displayed signal handling

## Frontend
Built with React + TypeScript + Vite.

Features:
- Live telemetry dashboard
- System-based telemetry grouping
- Signal hiding
- Signal metadata page
- Modular page/component structure

---

# Project Structure

```text
bcm/
├── bcm-can/
│   ├── backend/
│   ├── dashboards/
│   ├── logs/
│   ├── src/
│   └── tools/
│
├── bcm-frontend/
│   ├── src/
│   └── public/
│
├── README.md
└── .gitignore
