"""
Classe Manor - Représente la grille du manoir
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, Tuple
from core.game_objects import Direction


class Manor:
    """Grille du manoir où les pièces sont placées"""

    def __init__(self, width: int = 5, height: int = 10):
        self.width = width
        self.height = height
        # Grille de pièces (None = case vide)
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def get_room(self, row: int, col: int):
        """Récupère une pièce à une position donnée"""
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return None

    def place_room(self, room, row: int, col: int) -> bool:
        """Place une pièce dans la grille"""
        if 0 <= row < self.height and 0 <= col < self.width:
            if self.grid[row][col] is None:
                self.grid[row][col] = room
                room.position = (row, col)
                print(f"Pièce '{room.name}' placée en ({row}, {col})")
                return True
        return False

    def get_adjacent_position(self, position: Tuple[int, int], direction: Direction) -> Optional[Tuple[int, int]]:
        """Calcule la position adjacente dans une direction"""
        row, col = position

        if direction == Direction.NORTH:
            row -= 1
        elif direction == Direction.SOUTH:
            row += 1
        elif direction == Direction.EAST:
            col += 1
        elif direction == Direction.WEST:
            col -= 1

        # Vérifier que la position est valide
        if 0 <= row < self.height and 0 <= col < self.width:
            return (row, col)
        return None

    def can_move_to(self, from_pos: Tuple[int, int], direction: Direction) -> bool:
        """Vérifie si on peut se déplacer dans une direction"""
        # Vérifier que la pièce actuelle existe
        current_room = self.get_room(*from_pos)
        if not current_room:
            return False

        # Vérifier que la pièce a une porte dans cette direction
        if not current_room.has_door(direction):
            return False

        # Vérifier la position de destination
        dest_pos = self.get_adjacent_position(from_pos, direction)
        if not dest_pos:
            return False

        # Vérifier qu'il y a une pièce à destination
        dest_room = self.get_room(*dest_pos)
        if not dest_room:
            return False

        return True

    def __str__(self):
        """Affichage du manoir"""
        result = "\n=== MANOIR ===\n"
        for row in range(self.height):
            for col in range(self.width):
                room = self.grid[row][col]
                if room:
                    result += f"[{room.name[:4]:4s}]"
                else:
                    result += "[ -- ]"
            result += "\n"
        return result
