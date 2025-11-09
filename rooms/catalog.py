"""
Catalogue de pièces disponibles pour le jeu
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from typing import List, Optional

from rooms.room import Room
from core.game_objects import Direction, RoomColor
from rooms.effects import *
from items.consumables import *
from items.food import *
from items.interactive import *
from items.permanent import *


class RoomCatalog:
    """Catalogue contenant toutes les pièces disponibles"""

    def __init__(self):
        self.available_rooms: List[Room] = []
        self._initialize_rooms()

    def _initialize_rooms(self):
        """Initialise le catalogue avec toutes les pièces du jeu - Correspondant aux images"""

        # ============ PIÈCES AVEC IMAGES ============

        # 1. Library (blue)
        self.available_rooms.append(Room(
            name="Library",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.SOUTH],  # À MODIFIER
            gem_cost=0,
            rarity=1,
            objects=[Keys(1)]
        ))
        """
        Ajout de nouvelles pièces avec effets spéciaux
        À ajouter dans rooms/catalog.py dans la méthode _initialize_rooms()
        """

        # ============ NOUVELLES PIÈCES AVEC EFFETS SPÉCIAUX ============

        # Weight Room - Perd des pas lors du tirage mais gagne des clés
        self.available_rooms.append(Room(
            name="Weight Room",
            color=RoomColor.RED,
            doors=[Direction.NORTH, Direction.SOUTH],
            gem_cost=0,
            rarity=2,
            objects=[Keys(2)],
            effect=ResourceEffect(
                "Vous perdez 5 pas en tirant cette pièce mais gagnez 2 clés",
                'steps',
                -5,
                on_enter=False  # Effet lors du TIRAGE, pas en entrant
            )
        ))

        # Maid's Chamber - Augmente probabilité objets permanents
        self.available_rooms.append(Room(
            name="Maid's Chamber",
            color=RoomColor.PURPLE,
            doors=[Direction.NORTH, Direction.EAST],
            gem_cost=1,
            rarity=2,
            objects=[Shovel(), RabbitFoot()],  # Plus de chance d'objets permanents
            effect=ItemProbabilityEffect(
                "Augmente les chances de trouver des objets permanents",
                ['permanent_items'],
                3.0  # Triple la probabilité
            )
        ))

        # Solarium - Augmente probabilité pièces oranges (couloirs)
        self.available_rooms.append(Room(
            name="Solarium",
            color=RoomColor.ORANGE,
            doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST],
            gem_cost=2,
            rarity=2,
            objects=[Gems(1)],
            effect=ProbabilityModifierEffect(
                "Augmente la probabilité de tirer des pièces oranges (couloirs)",
                RoomColor.ORANGE,
                2.0
            )
        ))

        # Chamber of Mirrors - Ajoute des pièces spéciales au catalogue
        self.available_rooms.append(Room(
            name="Chamber of Mirrors",
            color=RoomColor.BLUE,
            doors=[Direction.NORTH, Direction.SOUTH],
            gem_cost=3,
            rarity=3,
            objects=[Gems(2)],
            effect=AddRoomsToCatalogEffect(
                "Ajoute 2 pièces spéciales rares au catalogue",
                ['Secret Room', 'Treasure Vault']
            )
        ))

        # Pool - Ajoute pièces au catalogue et disperse gemmes
        self.available_rooms.append(Room(
            name="Pool",
            color=RoomColor.BLUE,
            doors=[Direction.NORTH, Direction.EAST, Direction.WEST],
            gem_cost=2,
            rarity=3,
            objects=[Meal()],
            effect=DispersionEffect(
                "Disperse 4 gemmes dans les pièces vertes",
                'gems',
                4,
                RoomColor.GREEN
            )
        ))

        # Secret Room - Pièce rare avec beaucoup de ressources
        self.available_rooms.append(Room(
            name="Secret Room",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=3,
            objects=[Gold(50), Keys(3), Gems(3), Meal()],
            effect=ResourceEffect(
                "Vous gagnez 20 pas en entrant !",
                'steps',
                20,
                on_enter=True
            )
        ))

        # Treasure Vault - Contient objets permanents rares
        self.available_rooms.append(Room(
            name="Treasure Vault",
            color=RoomColor.YELLOW,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=3,
            objects=[
                Gold(100),
                Hammer(),
                MetalDetector(),
                LockpickKit(),
                Chest(),
                Chest()
            ]
        ))

        # Study - Donne des dés pour retirer
        self.available_rooms.append(Room(
            name="Study",
            color=RoomColor.BLUE,
            doors=[Direction.NORTH, Direction.SOUTH],
            gem_cost=1,
            rarity=1,
            objects=[Dice(2), Keys(1)],
            effect=ResourceEffect(
                "Vous gagnez 1 dé supplémentaire en tirant cette pièce",
                'dice',
                1,
                on_enter=False
            )
        ))

        # Armory - Disperse des clés dans pièces rouges
        self.available_rooms.append(Room(
            name="Armory",
            color=RoomColor.RED,
            doors=[Direction.NORTH, Direction.SOUTH],
            gem_cost=1,
            rarity=2,
            objects=[Keys(3), LockpickKit()],
            effect=DispersionEffect(
                "Disperse 3 clés dans les pièces rouges",
                'keys',
                3,
                RoomColor.RED
            )
        ))

        # Treasury - Disperse de l'or partout
        self.available_rooms.append(Room(
            name="Treasury",
            color=RoomColor.YELLOW,
            doors=[Direction.NORTH, Direction.EAST],
            gem_cost=2,
            rarity=3,
            objects=[Gold(30)],
            effect=DispersionEffect(
                "Disperse 50 pièces d'or dans 5 pièces aléatoires",
                'gold',
                5,
                None  # Toutes les pièces
            )
        ))
        # 2. Dining Room (blue)
        self.available_rooms.append(Room(
            name="Dining Room",
            color=RoomColor.BLUE,
            doors=[Direction.WEST,Direction.EAST, Direction.SOUTH],  # À MODIFIER
            gem_cost=0,
            rarity=1,
            objects=[Apple()]
        ))

        # 3. Mail Room (blue)
        self.available_rooms.append(Room(
            name="Mail Room",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH],  # À MODIFIER
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 4. Music Room (blue)
        self.available_rooms.append(Room(
            name="Music Room",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.SOUTH],  # À MODIFIER
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 5. Garage (blue)
        self.available_rooms.append(Room(
            name="Garage",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.SOUTH],  # À MODIFIER
            gem_cost=1,
            rarity=1,
            objects=[]
        ))

        # 6. Courtyard (blue)
        self.available_rooms.append(Room(
            name="Courtyard",
            color=RoomColor.BLUE,
            doors=[ Direction.SOUTH, Direction.EAST, Direction.WEST],  # À MODIFIER
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 7. Observatory (blue)
        self.available_rooms.append(Room(
            name="Observatory",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.SOUTH],  # À MODIFIER
            gem_cost=1,
            rarity=2,
            objects=[Gems(1)]
        ))

        # 8. Rumpus Room (blue)
        self.available_rooms.append(Room(
            name="Rumpus Room",
            color=RoomColor.BLUE,
            doors=[Direction.NORTH, Direction.SOUTH],  # À MODIFIER
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 9. Security (blue)
        self.available_rooms.append(Room(
            name="Security",
            color=RoomColor.BLUE,
            doors=[Direction.EAST, Direction.WEST, Direction.SOUTH],  # À MODIFIER
            gem_cost=1,
            rarity=1,
            objects=[Keys(1)]
        ))

        # ============ PIÈCES VERTES (jardins) ============

        # 10. Veranda (green)
        self.available_rooms.append(Room(
            name="Veranda",
            color=RoomColor.GREEN,
            doors=[Direction.SOUTH, Direction.NORTH],  # À MODIFIER
            gem_cost=2,
            rarity=2,
            objects=[Gems(1)]
        ))

        # ============ PIÈCES SPÉCIALES ============

        # 11. The Pool
        self.available_rooms.append(Room(
            name="The Pool",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH, Direction.EAST, Direction.WEST],  # À MODIFIER
            gem_cost=2,
            rarity=2,
            objects=[]
        ))

        # 12. Commissary (yellow)
        self.available_rooms.append(Room(
            name="Commissary",
            color=RoomColor.YELLOW,
            doors=[Direction.WEST, Direction.SOUTH],  # À MODIFIER
            gem_cost=1,
            rarity=1,
            objects=[Apple(), Banana()]
        ))

        # ============ PIÈCES ROUGES ============

        # 13. Chapel (red)
        self.available_rooms.append(Room(
            name="Chapel",
            color=RoomColor.PURPLE,
            doors=[Direction.SOUTH, Direction.EAST,Direction.WEST],  # À MODIFIER
            gem_cost=2,
            rarity=2,
            objects=[],
            effect=ResourceEffect(
                "Restaure 15 pas en entrant",
                'steps',
                15,
                on_enter=True
            )
        ))

        # 14. Antechamber (blue) - Point d'arrivée
        self.available_rooms.append(Room(
            name="Antechamber",
            color=RoomColor.BLUE,
            doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST],
            gem_cost=0,
            rarity=0,
            objects=[]
        ))

        # 15. Entrance Hall (blue) - Point de départ
        # Note: Créé automatiquement par get_entrance() si nécessaire

    def draw_rooms(self, count: int, position: tuple, context: dict = None) -> List[Room]:
        """
        Tire des pièces aléatoires du catalogue
        count: nombre de pièces à tirer
        position: (row, col) position où la pièce sera placée
        context: dictionnaire contenant les modificateurs de probabilité
        """
        if context is None:
            context = {}

        row, col = position

        # Filtrer les pièces disponibles et compatibles avec la position
        eligible_rooms = [
            room for room in self.available_rooms
            if room.can_be_placed(row, col, 9, 5)
        ]

        if not eligible_rooms:
            return []

        # Calculer les poids de probabilité
        weights = []
        for room in eligible_rooms:
            weight = room.get_probability_weight()

            # Appliquer les modificateurs de probabilité
            if hasattr(context, 'probability_modifiers') and room.color in context.probability_modifiers:
                weight *= context.probability_modifiers[room.color]

            weights.append(weight)

        # Normaliser les poids
        total_weight = sum(weights)
        if total_weight == 0:
            weights = [1.0] * len(weights)
            total_weight = len(weights)

        probabilities = [w / total_weight for w in weights]

        # Tirer les pièces
        drawn = []
        available_for_draw = eligible_rooms.copy()
        available_probs = probabilities.copy()

        for _ in range(min(count, len(available_for_draw))):
            room = random.choices(available_for_draw, weights=available_probs)[0]
            drawn.append(room)

            # Retirer la pièce pour ne pas la tirer deux fois
            idx = available_for_draw.index(room)
            available_for_draw.pop(idx)
            available_probs.pop(idx)

            # Renormaliser
            if available_probs:
                total = sum(available_probs)
                available_probs = [p / total for p in available_probs]

        # S'assurer qu'au moins une pièce a un coût de 0 gemmes
        if drawn and all(room.gem_cost > 0 for room in drawn):
            # Remplacer la pièce la plus rare par une pièce gratuite
            free_rooms = [r for r in eligible_rooms if r.gem_cost == 0]
            if free_rooms:
                drawn[-1] = random.choice(free_rooms)

        return drawn

    def remove_room(self, room: Room) -> bool:
        """Retire une pièce du catalogue (elle a été utilisée)"""
        if room in self.available_rooms:
            self.available_rooms.remove(room)
            return True
        return False

    def add_special_rooms(self, room_names: List[str]) -> int:
        """Ajoute des pièces spéciales au catalogue"""
        # Cette méthode peut être étendue pour ajouter des pièces spécifiques
        # Pour l'instant, retourne 0
        return 0

    def get_room_count(self) -> int:
        """Retourne le nombre de pièces disponibles"""
        return len(self.available_rooms)

    def get_all_rooms(self) -> List[Room]:
        """Retourne toutes les pièces disponibles"""
        return self.available_rooms.copy()

    def get_entrance(self) -> Optional[Room]:
        """Retourne la pièce Entrance Hall"""
        for room in self.available_rooms:
            if room.name == "Entrance Hall":
                return room
        
        # Si pas trouvé, créer une entrance basique
        entrance = Room(
            name="Entrance Hall",
            color=RoomColor.ORANGE,
            doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST],
            gem_cost=0,
            rarity=0,
            objects=[]
        )
        self.available_rooms.append(entrance)
        return entrance
    def get_room_by_name(self, room_name: str) -> Optional[Room]:
        """Retourne une pièce par son nom"""
        for room in self.available_rooms:
            if room.name == room_name:
                return room
        return None
