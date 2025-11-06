"""
Classes de base pour le jeu Blue Prince
Contient les classes abstraites et les énumérations
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from enum import Enum


class Direction(Enum):
    """Énumération des directions possibles"""
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class RoomColor(Enum):
    """Énumération des couleurs de pièces"""
    YELLOW = "yellow"  # Magasins
    GREEN = "green"  # Jardins
    PURPLE = "purple"  # Chambres
    ORANGE = "orange"  # Couloirs
    RED = "red"  # Pièces indésirables
    BLUE = "blue"  # Pièces communes


class GameObject(ABC):
    """Classe abstraite pour tous les objets du jeu"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def interact(self, player: 'Player') -> bool:
        """Interaction avec l'objet. Retourne True si l'interaction réussit"""
        pass

    def __str__(self):
        return self.name


class ConsumableItem(GameObject):
    """Classe parent pour les objets consommables"""

    def __init__(self, name: str, quantity: int = 1):
        super().__init__(name)
        self.quantity = quantity

    def interact(self, player: 'Player') -> bool:
        """Ajoute l'objet à l'inventaire"""
        return player.inventory.add_item(self)

    def consume(self, amount: int = 1) -> bool:
        """Consomme une quantité de l'objet"""
        if self.quantity >= amount:
            self.quantity -= amount
            return True
        return False


class PermanentItem(GameObject):
    """Classe parent pour les objets permanents"""

    def __init__(self, name: str, description: str = ""):
        super().__init__(name)
        self.description = description
        self.is_active = True

    def interact(self, player: 'Player') -> bool:
        """Ajoute l'objet permanent à l'inventaire"""
        return player.inventory.add_permanent_item(self)

    @abstractmethod
    def apply_effect(self, context: dict) -> None:
        """Applique l'effet de l'objet permanent"""
        pass


class Food(GameObject):
    """Classe parent pour la nourriture"""

    def __init__(self, name: str, steps_restored: int):
        super().__init__(name)
        self.steps_restored = steps_restored

    def interact(self, player: 'Player') -> bool:
        """Mange la nourriture et restaure des pas"""
        player.inventory.steps.quantity += self.steps_restored
        print(f"Vous avez mangé {self.name} et récupéré {self.steps_restored} pas!")
        return True


class InteractiveObject(GameObject):
    """Classe parent pour les objets interactifs (coffres, trous, casiers)"""

    def __init__(self, name: str, contents: List[GameObject]):
        super().__init__(name)
        self.contents = contents
        self.is_opened = False

    def interact(self, player: 'Player') -> bool:
        """Interagit avec l'objet (essaye de l'ouvrir)"""
        return self.open(player)

    @abstractmethod
    def can_open(self, player: 'Player') -> bool:
        """Vérifie si le joueur peut ouvrir l'objet"""
        pass

    def open(self, player: 'Player') -> bool:
        """Ouvre l'objet et donne son contenu au joueur"""
        if self.is_opened:
            print(f"{self.name} est déjà ouvert.")
            return False

        if not self.can_open(player):
            print(f"Vous ne pouvez pas ouvrir {self.name}.")
            return False

        self.is_opened = True
        print(f"Vous avez ouvert {self.name}!")

        for item in self.contents:
            item.interact(player)

        return True


class RoomEffect(ABC):
    """Classe abstraite pour les effets de pièces"""

    def __init__(self, description: str):
        self.description = description

    @abstractmethod
    def apply(self, game: 'Game', room: 'Room') -> None:
        """Applique l'effet de la pièce"""
        pass

    def __str__(self):
        return self.description