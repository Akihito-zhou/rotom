# modules/query/config.py

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "pokemon-dataset-zh", "data"))
IMAGE_DIR = os.path.join(BASE_DIR, "images", "home")
IMAGE_DIR_EVOLUTION = os.path.join(BASE_DIR, "images", "dream")
POKEMON_DIR = os.path.join(BASE_DIR, "pokemon")
MOVE_DIR = os.path.join(BASE_DIR, "move")
ABILITY_DIR = os.path.join(BASE_DIR, "ability")
