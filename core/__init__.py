"""
Package core - Classes de base du jeu
"""
from .game_objects import (
    Direction,
    RoomColor,
    GameObject,
    ConsumableItem,
    PermanentItem,
    Food,
    InteractiveObject
)

__all__ = [
    'Direction',
    'RoomColor',
    'GameObject',
    'ConsumableItem',
    'PermanentItem',
    'Food',
    'InteractiveObject'
]
