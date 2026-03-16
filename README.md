# Potager contre Cimetière 🌻🧟

A tower defense game inspired by *Plants vs Zombies*, built in Python with tkinter. This project implements data structures (stacks and queues) for managing game events and entities.

## 🎮 Overview

In **Potager contre Cimetière**, you defend your garden against waves of zombies by strategically planting defensive plants. Manage your sun resources wisely to place the right plants in the right lanes before the zombies reach your house.

## ✨ Features

- **Tower Defense Gameplay**: Place plants to defend against advancing zombie waves
- **Resource Management**: Collect suns and spend them strategically on plants
- **Event System**: Manage game events using stack and queue data structures
- **Multiple Plant Types**: Different plants with unique abilities
- **Zombie Waves**: Progressive difficulty as waves increase
- **Interactive GUI**: Tkinter-based user interface with real-time gameplay

## 📋 Project Structure

```
src/
├── main.py                    # Entry point
├── gameClass.py               # Core game loop and logic
├── playerClass.py             # Player state and resources
├── entities/                  # Static entity definitions
│   ├── plantsClass.py         # Plant types and properties
│   ├── zombiesClass.py        # Zombie types and properties
│   └── lawnmoyersClass.py     # Lawn mower entities
├── livingentities/            # Dynamic game entities
│   ├── livingplants/          # Active plant instances
│   ├── livingzombies/         # Active zombie instances
│   └── livinglawnmoyers/      # Active lawn mower instances
├── events/                    # Event management system
│   ├── eventClass.py          # Base event class
│   ├── event_waves.py         # Wave management
│   ├── event_invoke_zombie.py
│   ├── event_seizure.py
│   └── event_display_text.py
└── ui/                        # User interface components
    ├── lane.py                # Game lanes
    ├── slot.py                # Plant placement slots
    ├── plantselector.py       # Plant selection menu
    └── houseslot.py           # House/goal slot
```

## 🚀 Quick Start

### Requirements
- Python 3.7+
- tkinter (usually included with Python)

### Installation & Running

1. Navigate to the project directory:
   ```bash
   cd Potager-contre-Cimetiere
   ```

2. Run the game:
   ```bash
   python3 src/main.py
   ```

## 🎯 How to Play

1. **Select Plants**: Choose from available plants using the plant selector
2. **Place & Deploy**: Click on slots in your lanes to place plants
3. **Defend**: Overcome zombie waves to protect your house
4. **Manage Resources**: Use suns wisely - different plants cost different amounts
5. **Survive**: Reach the end without letting zombies breach your defenses

## 🏗️ Technical Details

- **GUI Framework**: tkinter
- **Data Structures**: Event queuing system for game events
- **Architecture**: Object-oriented design with entity and event systems
- **Game Loop**: Real-time rendering and update cycle

## 📚 Educational Purpose

This project demonstrates:
- Implementation of stacks and queues for event management
- Object-oriented programming principles
- GUI development with tkinter
- Game state management and entity systems

## 📝 License

School project for Terminale (French final year Baccalauréat)

## 👨‍💻 Author

Created as a coursework project
