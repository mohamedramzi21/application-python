"""
Catalogue de pièces disponibles pour le jeu
"""
from rooms.room import Room
from core.game_objects import Direction, RoomColor
from items.items import Gems, Chest, Gold, Keys, Apple, DigSpot, Banana, Cake, Sandwich, Locker, Dice
from rooms.effects import (
    ResourceEffect,
    ProbabilityModifierEffect,
    ItemProbabilityEffect,
    DispersionEffect,
)
import random
from typing import List, Optional


class RoomCatalog:
    """Catalogue contenant toutes les pièces disponibles"""

    def __init__(self):
        self.available_rooms: List[Room] = []
        self._initialize_rooms()

    def _initialize_rooms(self):
        """Initialise le catalogue avec toutes les pièces du jeu"""

        # ============ PIÈCES BLEUES (communes) ============

        # Vault - Contient beaucoup d'or
        self.available_rooms.append(
            Room(name="Vault",
                 color=RoomColor.BLUE,
                 doors=[Direction.SOUTH],
                 gem_cost=3,
                 rarity=3,
                 objects=[Gold(40)]
            )
        )


        # Den - Contient une gemme et parfois un coffre
        den_objects = [Gems(1)]
        if random.random() < 0.4:
            den_objects.append(Chest())

        self.available_rooms.append(
            Room(
                name="Den",
                color=RoomColor.BLUE,
                doors=[Direction.NORTH, Direction.SOUTH],
                gem_cost=0,
                rarity=1,
                objects=den_objects
            )
        )

        # Library - Plusieurs portes
        self.available_rooms.append(
            Room(
                name="Library",
                color=RoomColor.BLUE,
                doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST],
                gem_cost=0,
                rarity=1,
                objects=[Keys(1)]
            )
        )

        # Lavatory (plusieurs exemplaires)
        for i in range(2):
            self.available_rooms.append(
                Room(
                    name="Lavatory",
                    color=RoomColor.BLUE,
                    doors=[Direction.NORTH, Direction.SOUTH],
                    gem_cost=0,
                    rarity=0,
                    objects=[Apple()]
                )
            )

        # ============ PIÈCES VERTES (jardins) ============

        # Veranda - Augmente la probabilité de pièces vertes
        veranda_objects = []
        if random.random() < 0.6:
            veranda_objects.append(Gems(1))
        if random.random() < 0.5:
            veranda_objects.append(DigSpot())

        self.available_rooms.append(
            Room(
                name="Veranda",
                color=RoomColor.GREEN,
                doors=[Direction.SOUTH, Direction.EAST],
                gem_cost=2,
                rarity=2,
                objects=veranda_objects,
                effect=ProbabilityModifierEffect(
                "Augmente la probabilité de tirer des pièces vertes",
                RoomColor.GREEN,
                2.5
                   ),
                placement_condition=lambda r, c, h, w: c == 0 or c == w - 1  # Bordure
            )
        )

        # Greenhouse - Modifie les probabilités
        self.available_rooms.append(
            Room(
                name="Greenhouse",
                color=RoomColor.GREEN,
                doors=[Direction.NORTH, Direction.SOUTH],
                gem_cost=1,
                rarity=2,
                objects=[Gems(2), DigSpot()],
                effect=ItemProbabilityEffect(
                "Augmente la probabilité de trouver des objets",
                ['gems', 'permanent_items'],
                2.0
                )
            )
        )

        # Garden
        self.available_rooms.append(Room(
            name="Garden",
            color=RoomColor.GREEN,
            doors=[Direction.NORTH, Direction.EAST],
            gem_cost=1,
            rarity=1,
            objects=[Gems(1), DigSpot(), Banana()]
        ))

        # ============ PIÈCES VIOLETTES (chambres) ============

        # Bedroom - Restaure des pas en entrant
        self.available_rooms.append(Room(
            name="Bedroom",
            color=RoomColor.PURPLE,
            doors=[Direction.NORTH, Direction.SOUTH],
            gem_cost=1,
            rarity=1,
            objects=[Cake()],
            effect=ResourceEffect(
                "Restaure 5 pas en entrant",
                'steps',
                5,
                on_enter=True
            )
        ))

        # Master Bedroom - Donne des ressources lors du tirage
        self.available_rooms.append(Room(
            name="Master Bedroom",
            color=RoomColor.PURPLE,
            doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST],
            gem_cost=2,
            rarity=2,
            objects=[Sandwich(), Keys(1)],
            effect=ResourceEffect(
                "Vous gagnez 1 gemme en tirant cette pièce",
                'gems',
                1,
                on_enter=False
            )
        ))

        # Chapel - Restaure beaucoup de pas
        self.available_rooms.append(Room(
            name="Chapel",
            color=RoomColor.PURPLE,
            doors=[Direction.SOUTH, Direction.EAST],
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

        # ============ PIÈCES ORANGES (couloirs) ============

        # Hallway (plusieurs exemplaires)
        for i in range(3):
            self.available_rooms.append(Room(
                name="Hallway",
                color=RoomColor.ORANGE,
                doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST],
                gem_cost=0,
                rarity=0,
                objects=[]
            ))

        # Corridor
        self.available_rooms.append(Room(
            name="Corridor",
            color=RoomColor.ORANGE,
            doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST],
            gem_cost=0,
            rarity=0,
            objects=[Keys(1)]
        ))

        # ============ PIÈCES JAUNES (magasins) ============

        # Shop - Permet d'acheter des objets
        self.available_rooms.append(Room(
            name="Shop",
            color=RoomColor.YELLOW,
            doors=[Direction.NORTH, Direction.SOUTH],
            gem_cost=1,
            rarity=2,
            objects=[Gold(10)]
        ))

        # Market
        self.available_rooms.append(Room(
            name="Market",
            color=RoomColor.YELLOW,
            doors=[Direction.NORTH, Direction.EAST],
            gem_cost=2,
            rarity=2,
            objects=[Gold(15)]
        ))

        # ============ PIÈCES ROUGES (indésirables) ============

        # Furnace - Retire des pas mais modifie les probabilités
        self.available_rooms.append(Room(
            name="Furnace",
            color=RoomColor.RED,
            doors=[Direction.NORTH],
            gem_cost=0,
            rarity=1,
            objects=[Keys(2)],
            effect=ResourceEffect(
                "Vous perdez 10 pas en entrant",
                'steps',
                -10,
                on_enter=True
            )
        ))

        # Dead End
        self.available_rooms.append(Room(
            name="Dead End",
            color=RoomColor.RED,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Gold(5)]
        ))

        # ============ PIÈCES SPÉCIALES ============

        # Locker Room - Contient des casiers
        locker_room_objects = [Locker() for _ in range(random.randint(2, 4))]
        self.available_rooms.append(Room(
            name="Locker Room",
            color=RoomColor.BLUE,
            doors=[Direction.NORTH, Direction.SOUTH],
            gem_cost=1,
            rarity=2,
            objects=locker_room_objects
        ))

        # Patio - Disperse des gemmes
        self.available_rooms.append(Room(
            name="Patio",
            color=RoomColor.GREEN,
            doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST],
            gem_cost=2,
            rarity=2,
            objects=[],
            effect=DispersionEffect(
                "Disperse 3 gemmes dans d'autres pièces",
                'gems',
                3,
                None
            )
        ))

        # Office - Disperse des clés dans les pièces bleues
        self.available_rooms.append(Room(
            name="Office",
            color=RoomColor.BLUE,
            doors=[Direction.NORTH, Direction.SOUTH],
            gem_cost=1,
            rarity=2,
            objects=[Dice(1)],
            effect=DispersionEffect(
                "Disperse 2 clés dans les pièces bleues",
                'keys',
                2,
                RoomColor.BLUE
            )
        ))

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