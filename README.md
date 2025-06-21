# 🧹 Goal-Based Vacuum Cleaner Agent 

This project simulates a **goal-based agent** (like a robot vacuum) that navigates a 2D grid and cleans dirty cells one by one. It's built using Python and Pygame and is ideal for students learning basic artificial intelligence concepts like agent-environment interaction and pathfinding.

---

## 📌 Features

- 9x9 grid of rooms (randomly clean or dirty)
- Agent remembers previously visited cells
- Agent uses BFS (Breadth-First Search) to find the nearest dirty cell
- Simple visual display with colors:
  - 🔴 Red = Dirty
  - 🟢 Green = Clean
  - 🔵 Blue Border = Agent's position
- Action log and memory shown in the UI
- Runs step-by-step with Enter key

---

## 🚀 How to Run

### 1. Install Python

Make sure Python is installed. You can download it from: https://www.python.org/

### 2. Install Required Libraries

This project uses `pygame`. Install it using pip:

```bash
pip install pygame
