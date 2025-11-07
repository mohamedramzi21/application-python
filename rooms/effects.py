"""
Implémentation des effets spéciaux des pièces
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import TYPE_CHECKING
import random

from core.game_objects import RoomEffect, RoomColor

if TYPE_CHECKING:
    from game1.game import Game
    from rooms.room import Room
    from game1.player import Player


class ResourceEffect(RoomEffect):
    """Effet qui donne ou retire des ressources"""

    def __init__(self, description: str, resource_type: str, amount: int, on_enter: bool = True):
        """
        resource_type: 'steps', 'gold', 'gems', 'keys', 'dice'
        amount: quantité (positive = gain, négative = perte)
        on_enter: si True, effet appliqué en entrant, sinon lors du tirage
        """
        super().__init__(description)
        self.resource_type = resource_type
        self.amount = amount
        self.on_enter_flag = on_enter

    def apply(self, game: 'Game', room: 'Room') -> None:
        """Applique l'effet lors du tirage de la pièce"""
        if not self.on_enter_flag:
            self._apply_resource_change(game.player)

    def on_enter(self, player: 'Player', room: 'Room') -> None:
        """Applique l'effet quand le joueur entre dans la pièce"""
        if self.on_enter_flag:
            self._apply_resource_change(player)

    def _apply_resource_change(self, player: 'Player'):
        """Applique le changement de ressource"""
        inventory = player.inventory

        if self.resource_type == 'steps':
            inventory.steps.quantity += self.amount
            action = "récupéré" if self.amount > 0 else "perdu"
            print(f"Vous avez {action} {abs(self.amount)} pas!")
        elif self.resource_type == 'gold':
            inventory.gold.quantity += self.amount
            action = "récupéré" if self.amount > 0 else "perdu"
            print(f"Vous avez {action} {abs(self.amount)} pièces d'or!")
        elif self.resource_type == 'gems':
            inventory.gems.quantity += self.amount
            action = "récupéré" if self.amount > 0 else "perdu"
            print(f"Vous avez {action} {abs(self.amount)} gemmes!")
        elif self.resource_type == 'keys':
            inventory.keys.quantity += self.amount
            action = "récupéré" if self.amount > 0 else "perdu"
            print(f"Vous avez {action} {abs(self.amount)} clés!")
        elif self.resource_type == 'dice':
            inventory.dice.quantity += self.amount
            action = "récupéré" if self.amount > 0 else "perdu"
            print(f"Vous avez {action} {abs(self.amount)} dés!")


class ProbabilityModifierEffect(RoomEffect):
    """Effet qui modifie les probabilités de tirage"""

    def __init__(self, description: str, target_color: RoomColor, multiplier: float = 2.0):
        """
        target_color: couleur des pièces dont la probabilité est modifiée
        multiplier: multiplicateur de probabilité
        """
        super().__init__(description)
        self.target_color = target_color
        self.multiplier = multiplier

    def apply(self, game: 'Game', room: 'Room') -> None:
        """Enregistre l'effet dans le contexte du jeu"""
        if not hasattr(game, 'probability_modifiers'):
            game.probability_modifiers = {}

        game.probability_modifiers[self.target_color] = self.multiplier
        print(f"Les pièces {self.target_color.value} sont maintenant plus probables!")


class ItemProbabilityEffect(RoomEffect):
    """Effet qui modifie les probabilités de trouver des objets"""

    def __init__(self, description: str, item_types: list, multiplier: float = 1.5):
        """
        item_types: types d'objets affectés (ex: ['gems', 'permanent_items'])
        multiplier: multiplicateur de probabilité
        """
        super().__init__(description)
        self.item_types = item_types
        self.multiplier = multiplier

    def apply(self, game: 'Game', room: 'Room') -> None:
        """Enregistre l'effet dans le contexte du jeu"""
        if not hasattr(game, 'item_probability_modifiers'):
            game.item_probability_modifiers = {}

        for item_type in self.item_types:
            game.item_probability_modifiers[item_type] = self.multiplier

        print(f"Vous avez plus de chances de trouver certains objets!")


class DispersionEffect(RoomEffect):
    """Effet qui disperse des objets dans d'autres pièces"""

    def __init__(self, description: str, object_type: str, quantity: int, target_color: RoomColor = None):
        """
        object_type: type d'objet à disperser ('gold', 'gems', 'keys', etc.)
        quantity: nombre d'objets à disperser
        target_color: couleur des pièces cibles (None = toutes les pièces)
        """
        super().__init__(description)
        self.object_type = object_type
        self.quantity = quantity
        self.target_color = target_color

    def apply(self, game: 'Game', room: 'Room') -> None:
        """Disperse des objets dans des pièces aléatoires"""
        from items import Gold, Gems, Keys, Dice

        # Récupérer les pièces éligibles
        eligible_rooms = []
        for row in game.manor.grid:
            for cell_room in row:
                if cell_room and cell_room != room:
                    if self.target_color is None or cell_room.color == self.target_color:
                        eligible_rooms.append(cell_room)

        if not eligible_rooms:
            print("Aucune pièce disponible pour la dispersion.")
            return

        # Disperser les objets
        rooms_to_use = random.sample(eligible_rooms, min(self.quantity, len(eligible_rooms)))

        for target_room in rooms_to_use:
            if self.object_type == 'gold':
                target_room.objects.append(Gold(random.randint(3, 10)))
            elif self.object_type == 'gems':
                target_room.objects.append(Gems(1))
            elif self.object_type == 'keys':
                target_room.objects.append(Keys(1))
            elif self.object_type == 'dice':
                target_room.objects.append(Dice(1))

        print(f"{self.quantity} {self.object_type} dispersé(s) dans d'autres pièces!")


class AddRoomsToCatalogEffect(RoomEffect):
    """Effet qui ajoute de nouvelles pièces au catalogue"""

    def __init__(self, description: str, room_names: list):
        """
        room_names: noms des pièces à ajouter au catalogue
        """
        super().__init__(description)
        self.room_names = room_names

    def apply(self, game: 'Game', room: 'Room') -> None:
        """Ajoute des pièces au catalogue"""
        added = game.manor.room_catalog.add_special_rooms(self.room_names)
        if added:
            print(f"{added} nouvelles pièces ajoutées au catalogue!")
        else:
            print("Aucune nouvelle pièce ajoutée.")


class ConditionalEffect(RoomEffect):
    """Effet qui s'active sous certaines conditions"""

    def __init__(self, description: str, condition: callable, effect: RoomEffect):
        """
        condition: fonction qui retourne True si l'effet doit s'activer
        effect: effet à appliquer si la condition est vraie
        """
        super().__init__(description)
        self.condition = condition
        self.effect = effect

    def apply(self, game: 'Game', room: 'Room') -> None:
        """Applique l'effet si la condition est remplie"""
        if self.condition(game, room):
            self.effect.apply(game, room)