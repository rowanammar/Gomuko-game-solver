# Gomoku (Five in a Row)

![g](https://github.com/user-attachments/assets/8a9a1262-6966-4058-8ab6-a5eb561245c3)

A complete implementation of the classic Gomoku (Five in a Row) game with multiple AI opponents and gameplay modes.

## Overview

Gomoku, also called Five in a Row, is a traditional strategy board game played on a 15×15 grid where players alternate placing black and white stones. The winner is the first player to form chain of five stones horizontally, vertically, or diagonally.

This implementation features:

- Clean, attractive GUI with Tkinter
- Multiple AI opponents with different difficulty levels
- Various game modes including Human vs AI, Human vs Human, and AI vs AI
- Console and GUI interfaces

## Features

- **Multiple Game Modes:**

  - Human vs Human
  - Human vs AI (with different AI strategies)
  - AI vs AI (watch different AI strategies compete)

- **AI Opponents:**

  - **RandomAgent**: Makes random legal moves
  - **MinimaxAgent**: Uses the minimax algorithm for moderate difficulty
  - **AlphaBetaAgent**: Uses alpha-beta pruning for smarter decision-making

- **User-Friendly Interface:**
  - Clear indicators showing which player's turn it is
  - Visual display of black and white stones
  - Game status messages

## How to Play

1. Run the game with `python gui.py`
2. Select a game mode from the welcome screen
3. If playing against an AI, select the AI difficulty
4. Place stones by clicking on the intersections of the grid
5. The first player to get five stones in a row (horizontally, vertically, or diagonally) wins

### Controls

- **Mouse**: Click on any intersection to place a stone
- The game automatically prevents illegal moves

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/rowanammar/Gomuko-game-solver.git
   ```

2. Navigate to the directory:

   ```
   cd go-moku
   ```

3. Run the game:
   ```
   python gui.py
   ```

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python installations)

## Technical Details

### Game Engine

The game logic is handled by the `GameEngine` class, which maintains the board state, validates moves, checks for wins, and manages player turns.

### AI Implementations

- **RandomAgent**: Selects random valid moves.
- **MinimaxAgent**: Uses the minimax algorithm to explore possible future board states and choose optimal moves. It has a customizable search depth.
- **AlphaBetaAgent**: Enhances the minimax algorithm with alpha-beta pruning to explore deeper into the game tree by eliminating branches that won't affect the final decision.

## License

MIT License

## Acknowledgments

- This project was created as a demonstration of game development and AI implementation
