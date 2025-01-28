##SIMPLIFIED STRATEGO

**Project Overview**
This project is a Python-based simulation of the classic board game Stratego, designed with a simplified 8x8 board and 16 pieces per player. The primary objective was to create an engaging gameplay experience by incorporating Artificial Intelligence (AI) elements, leveraging a combination of genetic algorithms for AI setup and rule-based heuristics for decision-making during gameplay.

OBJECTIVE

The goal of this project is to:

- Develop a simplified digital version of Stratego for faster gameplay.
- Incorporate AI elements to provide a challenging opponent.
- Explore AI-driven strategic decision-making using genetic algorithms and rule-based heuristics.

GAME RULES

Board and Setup:

- An 8x8 board with 16 pieces per player.
- Pieces include special ranks such as Spy, Bombs, Soldiers, Generals, and a Flag.
- Players place pieces face down, keeping ranks hidden from the opponent.

Gameplay:

- Players take turns moving their pieces one square horizontally or vertically.
- Combat occurs when pieces occupy the same square; ranks are revealed, and the higher-ranked piece wins.
- Bombs are immobile and destroy any piece that moves onto their square, except for Miners.
- The game ends when a player captures the opponent's Flag or eliminates all movable pieces.

![Screenshot 2025-01-28 203514](https://github.com/user-attachments/assets/a3217367-0db9-4162-9a2e-e9d09b329337)

Special Rules:

- The Spy can defeat only the highest-ranked piece, the Marshal.
- Miners are the only pieces capable of defusing Bombs.

AI COMPONENTS

Combined Approach:

- Genetic algorithms handle static initial setup. It evaluates diverse setups and selects the best configurations.
- Rule-based heuristics manage real-time gameplay decisions and tactical responses to combat scenarios.

![Screenshot 2025-01-28 203422](https://github.com/user-attachments/assets/b38b6460-9f43-46a6-82f7-974f4d38346c)

