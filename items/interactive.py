"""
Objets interactifs du jeu
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from typing import TYPE_CHECKING
from core.game_objects import InteractiveObject
from items.consumables import Gold, Keys, Gems, Dice
from items.food import Apple, Banana, Cake, Sandwich

if TYPE_CHECKING:
    from game1.player import Player


class Chest(InteractiveObject):
    """Coffre contenant des objets"""

    def __init__(self):
        # Génère un contenu aléatoire pour le coffre
        contents = random.choice([[Gems(1)], [Keys(1)], [Apple()]])
        super().__init__("Coffre", contents)

    def can_open(self, player):
        return player.inventory.keys > 0 or any(obj.name == "Marteau" for obj in player.inventory.permanent_items)
    def _generate_contents(self) -> list:
        """Génère un contenu aléatoire pour le coffre"""
        possible_contents = [
            Gold(random.randint(5, 20)),
            Keys(random.randint(1, 2)),
            Gems(1),
            Dice(1),
            Apple(),
            Banana()
        ]
        # Choisit 1-3 objets aléatoires
        num_items = random.randint(1, 3)
        return random.sample(possible_contents, num_items)

    def can_open(self, player: 'Player') -> bool:
        """Peut ouvrir avec une clé ou un marteau"""
        has_hammer = player.inventory.has_permanent_item("Marteau")
        has_key = player.inventory.keys.quantity > 0

        if has_hammer:
            print("Vous utilisez le marteau pour ouvrir le coffre.")
            return True
        elif has_key:
            player.inventory.keys.consume(1)
            print("Vous utilisez une clé pour ouvrir le coffre.")
            return True
        else:
            print("Vous avez besoin d'une clé ou d'un marteau pour ouvrir ce coffre.")
            return False


class DigSpot(InteractiveObject):
    """Endroit où creuser"""

    def __init__(self):
        contents = self._generate_contents()
        super().__init__("Endroit où creuser", contents)

    def can_open(self, player):
        # vérifie si le joueur possède une pelle
        return any(obj.name == "Pelle" for obj in player.inventory.permanent_items)
    def _generate_contents(self) -> list:
        """Génère un contenu aléatoire pour le trou"""
        if random.random() < 0.3:  # 30% de chance de ne rien trouver
            return []

        possible_contents = [
            Gold(random.randint(3, 15)),
            Keys(1),
            Gems(1),
            Apple(),
            Banana()
        ]
        num_items = random.randint(1, 2)
        return random.sample(possible_contents, num_items)

    def can_open(self, player: 'Player') -> bool:
        """Nécessite une pelle"""
        if player.inventory.has_permanent_item("Pelle"):
            print("Vous utilisez la pelle pour creuser.")
            return True
        else:
            print("Vous avez besoin d'une pelle pour creuser ici.")
            return False


class Locker(InteractiveObject):
    """Casier dans le vestiaire"""

    def __init__(self):
        contents = self._generate_contents()
        super().__init__("Casier", contents)

    def _generate_contents(self) -> list:
        """Génère un contenu aléatoire pour le casier"""
        if random.random() < 0.2:  # 20% de chance de ne rien trouver
            return []

        possible_contents = [
            Gold(random.randint(5, 25)),
            Keys(1),
            Gems(1),
            Dice(1),
            Cake(),
            Sandwich()
        ]
        num_items = random.randint(1, 2)
        return random.sample(possible_contents, num_items)

    def can_open(self, player: 'Player') -> bool:
        """Nécessite toujours une clé"""
        if player.inventory.keys.quantity > 0:
            player.inventory.keys.consume(1)
            print("Vous utilisez une clé pour ouvrir le casier.")
            return True
        else:
            print("Vous avez besoin d'une clé pour ouvrir ce casier.")
            return False