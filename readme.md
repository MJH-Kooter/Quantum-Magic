# Welcome to Quantum Magic!

Quantum magic is a simple puzzle game, where the player creates quantum logical circuits in the form of potion recipes.
These recipes are required to fulfill specific tasks. Based on the performance a score is calculated.
As a bonus, this score corresponds to certain performance metrics of the quantum hardware used in the backend. 

# To setup a virtual environment with the required files, run:

```
$ python -m venv QuantumMagic
$ source QuantumMagic/bin/activate
$ pip install -r requirements.txt
```

# Or for Windows users:

```
c:\> python -m venv QuantumMagic
C:\> QuantumMagic\Scripts\activate.bat
C:\> pip install -r requirements.txt
```

# Play command:

```
python main.py
```

# Goal and controls:

The goal of the player is to help the wizard brew potions by dragging and dropping ingredients on a recipe line.
When starting the player should go to the table page to prepare a recipe. When the recipe is done the player returns
to the main menu and clicks the kettle to start the calculations.

Only the mouse (LMB) is required to navigate and play the game.
Optionally Spacebar can be used to skip animations.


# Known bugs/issues:


- On some devices the "\n" character might be handled wrongly, resulting in unreadable strings in animations and the almanac.
- The backend might be offline (often in weekends) or very busy which causes very long waiting times.
- Dragging an ingredient over an existing ingredient erases the first one from the backend list.
- Multi-item ingredient can be buggy, when constantly replacing the first and/or second element.
- Multi-item ingredients should force the second element on a different row in the backend, but this might not happen correctly.
- The scoring function in level 2 does not account for random guesses, so the results might not be representative.
- Level 4 is not compatible with the backend, so trying to play will most likely result in an error.

