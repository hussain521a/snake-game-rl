# Snake Game with Reinforcement Learning

This project implements the classic Snake game with a Reinforcement Learning agent that learns to play the game.

You can either:
- Play the game yourself
- Train and watch the RL agent learn in real time

## Requirements

Before setting up the project, make sure you have Conda installed (Anaconda or Miniconda).

If you do not have Conda installed:

1. Download Miniconda (recommended) or Anaconda from:
   https://docs.conda.io/en/latest/miniconda.html

2. Follow the installation instructions for your operating system.

3. After installation, verify Conda is installed by running:

```bash
conda --version
```
If a version number is printed, Conda is installed correctly

## Setup and Run Instructions

### 1. Create the Conda environment

The project includes an `environment.yml` file with all required dependencies to run using conda

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

```bash
conda activate snake_rl
```

*snake_rl is the environment name defined inside `environment.yml`.

### 3. Play the game manually

```bash
python snake_game.py
```

This launches the playable version of Snake.
Use arrow keys to control the movement.

### 4. Train the Reinforcement Learning agent

```bash
python agent.py
```

This will:
- Start training the RL model
- Launch the game window
- Display the training progression graph
