"""
Classe Player - Représente le joueur
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game1.inventory import Inventory
from typing import Tuple


class Player:
    """Classe représentant le joueur"""

    def __init__(self):
        self.inventory = Inventory()
        self.position = (0, 0)  # Position (row, col) dans le manoir

    def is_alive(self) -> bool:
        """Vérifie si le joueur est toujours vivant (a des pas)"""
        return self.inventory.steps.quantity > 0

    def move(self, new_position: Tuple[int, int]) -> bool:
        """Déplace le joueur vers une nouvelle position"""
        if self.inventory.use_steps(1):
            self.position = new_position
            print(f"Déplacement vers {new_position}. Pas restants: {self.inventory.steps.quantity}")
            return True
        else:
            print("Plus de pas disponibles!")
            return False

    def can_afford_room(self, gem_cost: int) -> bool:
        """Vérifie si le joueur peut payer le coût en gemmes d'une pièce"""
        return self.inventory.gems.quantity >= gem_cost

    def __str__(self):
        return f"Player at {self.position}\n{self.inventory}"
