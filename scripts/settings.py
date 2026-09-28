from pathlib import Path

# A pasta do projeto é a pasta onde está o main.py.
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

WIDTH = 1152
HEIGHT = 720
FPS = 60

PLAYER_SPEED = 260
ANIMATION_SPEED = 0.10

# Cores usadas pela interface
WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
DARK = (35, 35, 50)
PURPLE = (110, 75, 150)
YELLOW = (255, 220, 70)
GREEN = (80, 170, 100)
RED = (210, 75, 75)
