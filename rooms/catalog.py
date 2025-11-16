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

        # Apply a random rotation (0/90/180/270) to each room to increase directional variety.
        # Skip Entrance Hall and Antechamber to keep them stable.
        for room in self.available_rooms:
            if room.name in ["Entrance Hall", "Antechamber"]:
                continue
            # Only rotate if the room has doors defined
            if not getattr(room, 'doors_directions', None):
                continue
            deg = random.choice([0, 90, 180, 270])
            if deg != 0:
                room.rotate(deg)
                # Optional: annotate the name with rotation for debugging (kept commented)
                # room.name = f"{room.name} (rot{deg})"

    def _initialize_rooms(self):
        """Initialise le catalogue avec toutes les pièces du jeu - Correspondant aux images"""

        # ============ PIÈCES AVEC IMAGES ============

        # 1. Library (blue)
        self.available_rooms.append(Room(
            name="Library",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Keys(1)]
        ))
        
        # 2. Dining Room (blue)
        self.available_rooms.append(Room(
            name="Dining Room",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.EAST, Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Gems(1), Keys(1), Dice(1), Cake(),Gold(40)]
        ))

        # 3. Mail Room (blue)
        self.available_rooms.append(Room(
            name="Mail Room",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 4. Music Room (blue)
        self.available_rooms.append(Room(
            name="Music Room",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Gold(4)]
        ))

        # 5. Garage (blue)
        self.available_rooms.append(Room(
            name="Garage",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.SOUTH],
            gem_cost=1,
            rarity=1,
            objects=[]
        ))

        # 6. Courtyard (green)
        self.available_rooms.append(Room(
            name="Courtyard",
            color=RoomColor.GREEN,
            doors=[Direction.SOUTH, Direction.EAST, Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 7. Observatory (blue)
        self.available_rooms.append(Room(
            name="Observatory",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.SOUTH],
            gem_cost=1,
            rarity=2,
            objects=[Gems(1), Gold(40)]
        ))

        # 8. Rumpus Room (blue)
        self.available_rooms.append(Room(
            name="Rumpus Room",
            color=RoomColor.BLUE,
            doors=[Direction.NORTH, Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 9. Security (blue)
        self.available_rooms.append(Room(
            name="Security",
            color=RoomColor.BLUE,
            doors=[Direction.EAST, Direction.WEST, Direction.SOUTH],
            gem_cost=1,
            rarity=1,
            objects=[Keys(1)]
        ))

        # ============ PIÈCES VERTES (jardins) ============

        # 10. Veranda (green) - Walk-in Closet avec objets à ramasser
        self.available_rooms.append(Room(
            name="Veranda",
            color=RoomColor.GREEN,
            doors=[Direction.SOUTH, Direction.NORTH],
            gem_cost=0,
            rarity=1,
            objects=[Gems(1), Keys(1), Dice(1), Cake(),Gold(40)]
        ))

        # ============ PIÈCES SPÉCIALES ============

        # 11. The Pool
        self.available_rooms.append(Room(
            name="The Pool",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH, Direction.EAST, Direction.WEST],
            gem_cost=2,
            rarity=2,
            objects=[]
        ))

        # 12. Commissary (yellow)
        self.available_rooms.append(Room(
            name="Commissary",
            color=RoomColor.YELLOW,
            doors=[Direction.WEST, Direction.SOUTH],
            gem_cost=1,
            rarity=1,
            objects=[Apple(), Banana()]
        ))

        # ============ PIÈCES ROUGES ============

        # 13. Chapel (red)
        self.available_rooms.append(Room(
            name="Chapel",
            color=RoomColor.RED,
            doors=[Direction.SOUTH, Direction.EAST, Direction.WEST],
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

        # ============ NOUVELLES PIÈCES BLEUES ============

        # 16. Attic (blue)
        self.available_rooms.append(Room(
            name="Attic",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Keys(1), Dice(1)]
        ))

        # 17. Closet (blue)
        self.available_rooms.append(Room(
            name="Closet",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Cake()]
        ))

        # 18. Coat Check (blue)
        self.available_rooms.append(Room(
            name="Coat Check",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Keys(1)]
        ))

        # 19. Conference Room (blue)
        self.available_rooms.append(Room(
            name="Conference Room",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.EAST, Direction.SOUTH],
            gem_cost=1,
            rarity=2,
            objects=[Keys(2), Dice(1)]
        ))

        # 20. Drawing Room (blue)
        self.available_rooms.append(Room(
            name="Drawing Room",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.SOUTH, Direction.EAST],
            gem_cost=1,
            rarity=1,
            objects=[Apple()]
        ))

        # 21. Freezer (blue)
        self.available_rooms.append(Room(
            name="Freezer",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Cake(), Sandwich()]
        ))

        # 22. Gallery (blue)
        self.available_rooms.append(Room(
            name="Gallery",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH,Direction.NORTH],
            gem_cost=1,
            rarity=2,
            objects=[Gems(1)]
        ))

        # 23. Parlor (blue)
        self.available_rooms.append(Room(
            name="Parlor",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Keys(1)]
        ))

        # 24. Pump Room (blue)
        self.available_rooms.append(Room(
            name="Pump Room",
            color=RoomColor.BLUE,
            doors=[Direction.WEST, Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 25. Room 8 (blue)
        self.available_rooms.append(Room(
            name="Room 8",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH,Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[Keys(1)]
        ))

        # 26. Rotunda (blue)
        self.available_rooms.append(Room(
            name="Rotunda",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH,Direction.WEST],
            gem_cost=1,
            rarity=2,
            objects=[Gems(1), Keys(1)]
        ))

        # 27. Spare Room (blue)
        self.available_rooms.append(Room(
            name="Spare Room",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH,Direction.NORTH],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 28. Storeroom (blue)
        self.available_rooms.append(Room(
            name="Storeroom",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Keys(2)]
        ))

        # 29. The Foundation (blue)
        self.available_rooms.append(Room(
            name="The Foundation",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH,Direction.EAST,Direction.WEST],
            gem_cost=1,
            rarity=2,
            objects=[Gems(1)]
        ))

        # 30. Utility Closet (blue)
        self.available_rooms.append(Room(
            name="Utility Closet",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Keys(1)]
        ))

        # 31. Walk-in Closet (blue)
        self.available_rooms.append(Room(
            name="Walk-in Closet",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Cake(), Dice(1)]
        ))

        # 32. Workshop (blue)
        self.available_rooms.append(Room(
            name="Workshop",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH, Direction.NORTH],
            gem_cost=0,
            rarity=1,
            objects=[Keys(1)]
        ))

        
        # 34. Boiler Room (blue)
        self.available_rooms.append(Room(
            name="Boiler Room",
            color=RoomColor.BLUE,
            doors=[Direction.SOUTH,Direction.WEST,Direction.EAST],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # ============ NOUVELLES PIÈCES VERTES (JARDINS) ============

        # 35. Morning Room (green)
        self.available_rooms.append(Room(
            name="Morning Room",
            color=RoomColor.GREEN,
            doors=[Direction.SOUTH, Direction.EAST, Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[Gems(1), Apple()]
        ))

        # 36. Patio (green)
        self.available_rooms.append(Room(
            name="Patio",
            color=RoomColor.GREEN,
            doors=[Direction.SOUTH, Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[Gems(1)]
        ))

        # 37. Terrace (green)
        self.available_rooms.append(Room(
            name="Terrace",
            color=RoomColor.GREEN,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Gems(1), Keys(1)]
        ))

        # 38. Greenhouse (green/yellow/violet)
        self.available_rooms.append(Room(
            name="Greenhouse",
            color=RoomColor.GREEN,
            doors=[Direction.SOUTH],
            gem_cost=1,
            rarity=2,
            objects=[Gems(2), Apple(), Banana()]
        ))

        # ============ NOUVELLES PIÈCES ORANGE (COULOIRS) ============

        # 39. Corridor (orange)
        self.available_rooms.append(Room(
            name="Corridor",
            color=RoomColor.ORANGE,
            doors=[Direction.NORTH, Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 40. East Wing Hall (orange)
        self.available_rooms.append(Room(
            name="East Wing Hall",
            color=RoomColor.ORANGE,
            doors=[Direction.SOUTH, Direction.EAST, Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 41. Foyer (orange)
        self.available_rooms.append(Room(
            name="Foyer",
            color=RoomColor.ORANGE,
            doors=[Direction.NORTH, Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 42. Hallway (orange)
        self.available_rooms.append(Room(
            name="Hallway",
            color=RoomColor.ORANGE,
            doors=[Direction.WEST, Direction.SOUTH, Direction.EAST],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 43. Passageway (orange)
        self.available_rooms.append(Room(
            name="Passageway",
            color=RoomColor.ORANGE,
            doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 44. Secret Passage (orange)
        self.available_rooms.append(Room(
            name="Secret Passage",
            color=RoomColor.ORANGE,
            doors=[Direction.NORTH, Direction.SOUTH],# il doit depenser une cle pour pouvoir choir la porte de north
            gem_cost=2,
            rarity=1,
            objects=[Keys(1)],
            specific_door_locks={
                Direction.NORTH: 1  # ← AJOUT: Porte NORTH verrouillée
            }
            
            
        ))

        # 45. West Wing Hall (orange)
        self.available_rooms.append(Room(
            name="West Wing Hall",
            color=RoomColor.ORANGE,
            doors=[Direction.SOUTH, Direction.EAST, Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # ============ NOUVELLES PIÈCES ROUGES (DANGEREUSES) ============

        # 46. Archives (red)
        self.available_rooms.append(Room(
            name="Archives",
            color=RoomColor.RED,
            doors=[Direction.SOUTH, Direction.NORTH, Direction.EAST,Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[],
            specific_door_locks={
                Direction.NORTH: 1  # ← AJOUT: Porte NORTH verrouillée
            }
        ))

        # 47. Darkroom (red)
        self.available_rooms.append(Room(
            name="Darkroom",
            color=RoomColor.RED,
            doors=[Direction.SOUTH, Direction.EAST,Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[],
            specific_door_locks={
                Direction.EAST: 1  # ← AJOUT: Porte EAST verrouillée
            }
            
        ))

        # 48. Furnace (red)
        self.available_rooms.append(Room(
            name="Furnace",
            color=RoomColor.RED,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[],
            specific_door_locks={
                Direction.SOUTH: 2  # ← AJOUT: Porte SOUTH double tour!
          }
        ))

        # 49. Gymnasium (red)
        self.available_rooms.append(Room(
            name="Gymnasium",
            color=RoomColor.RED,
            doors=[Direction.SOUTH, Direction.EAST,Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 50. Lavatory (red)
        self.available_rooms.append(Room(
            name="Lavatory",
            color=RoomColor.RED,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 51. Maid Chamber (red)
        self.available_rooms.append(Room(
            name="Maid Chamber",
            color=RoomColor.RED,
            doors=[Direction.SOUTH,Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # 52. Weight Room (red)
        self.available_rooms.append(Room(
            name="Weight Room",
            color=RoomColor.RED,
            doors=[Direction.SOUTH, Direction.NORTH, Direction.EAST,Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[]
        ))

        # ============ NOUVELLES PIÈCES VIOLETTES (CHAMBRES) ============

        # 53. Bedroom (purple)
        self.available_rooms.append(Room(
            name="Bedroom",
            color=RoomColor.PURPLE,
            doors=[Direction.SOUTH,Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[Cake()]
        ))

        # 54. Boudoir (purple)
        self.available_rooms.append(Room(
            name="Boudoir",
            color=RoomColor.PURPLE,
            doors=[Direction.SOUTH, Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[Cake()]
        ))

        # 55. Bunk Room (purple)
        self.available_rooms.append(Room(
            name="Bunk Room",
            color=RoomColor.PURPLE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Cake()]
        ))

        # 56. Guest Bedroom (purple)
        self.available_rooms.append(Room(
            name="Guest Bedroom",
            color=RoomColor.PURPLE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Cake()]
        ))

        # 57. Her Lady's Chamber (purple)
        self.available_rooms.append(Room(
            name="Her Lady's Chamber",
            color=RoomColor.PURPLE,
            doors=[Direction.SOUTH],
            gem_cost=1,
            rarity=2,
            objects=[Cake(), Meal()],
            specific_door_locks={
                Direction.SOUTH: 1  # ← AJOUT: Chambre privée verrouillée
            }
        ))

        # 58. Master Bedroom (purple)
        self.available_rooms.append(Room(
            name="Master Bedroom",
            color=RoomColor.PURPLE,
            doors=[Direction.SOUTH],
            gem_cost=1,
            rarity=2,
            objects=[Cake(), Meal()],
            specific_door_locks={
                Direction.SOUTH: 1  # ← AJOUT: Chambre privée verrouillée
           }
        ))

        # 59. Nursery (purple)
        self.available_rooms.append(Room(
            name="Nursery",
            color=RoomColor.PURPLE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Cake()]
        ))

        # 60. Servant Quarters (purple)
        self.available_rooms.append(Room(
            name="Servant Quarters",
            color=RoomColor.PURPLE,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Cake()]
        ))

        # ============ NOUVELLES PIÈCES JAUNES (MAGASINS) ============

        # 61. Bookshop (yellow/violet)
        self.available_rooms.append(Room(
            name="Bookshop",
            color=RoomColor.YELLOW,
            doors=[Direction.SOUTH, Direction.WEST],
            gem_cost=1,
            rarity=1,
            objects=[Keys(2), Dice(1)]
        ))

        # 62. Kitchen (yellow/violet)
        self.available_rooms.append(Room(
            name="Kitchen",
            color=RoomColor.YELLOW,
            doors=[Direction.SOUTH, Direction.WEST],
            gem_cost=0,
            rarity=1,
            objects=[Apple(), Banana(), Cake()]
        ))

        # 63. Laundry Room (yellow/violet)
        self.available_rooms.append(Room(
            name="Laundry Room",
            color=RoomColor.YELLOW,
            doors=[Direction.SOUTH],
            gem_cost=0,
            rarity=1,
            objects=[Keys(1)]
        ))

        # 64. Locksmith (yellow/violet)
        self.available_rooms.append(Room(
            name="Locksmith",
            color=RoomColor.YELLOW,
            doors=[Direction.SOUTH],
            gem_cost=1,
            rarity=2,
            objects=[Keys(3)],
            specific_door_locks={
              Direction.SOUTH: 1  # ← AJOUT: Le serrurier se verrouille lui-même!
            }
            
        ))

        # 65. Mount Holly Gift Shop (yellow/violet)
        self.available_rooms.append(Room(
            name="Mount Holly Gift Shop",
            color=RoomColor.YELLOW,
            doors=[Direction.SOUTH, Direction.WEST,Direction.EAST],
            gem_cost=1,
            rarity=2,
            objects=[Keys(2), Gems(1), Dice(1)],
            specific_door_locks={
                Direction.EAST: 1  # ← AJOUT: Porte EST verrouillée
           }
            
        ))

        # 66. Showroom (yellow/violet)
        self.available_rooms.append(Room(
            name="Showroom",
            color=RoomColor.YELLOW,
            doors=[Direction.SOUTH, Direction.NORTH],
            gem_cost=1,
            rarity=1,
            objects=[Keys(1), Dice(1)]
        ))

        # 67. The Armory (yellow/violet)
        self.available_rooms.append(Room(
            name="The Armory",
            color=RoomColor.YELLOW,
            doors=[Direction.SOUTH, Direction.EAST,Direction.WEST,Direction.NORTH],#north and south must use a shovel
            gem_cost=2,
            rarity=2,
            objects=[Keys(2), Gems(1)],
            specific_door_locks={
                Direction.NORTH: 1,  # ← AJOUT: Portes NORTH et SOUTH verrouillées
                Direction.SOUTH: 1
         }
            
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
