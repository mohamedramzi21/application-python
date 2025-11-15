"""
Classes pour les pièces et les portes
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Optional, Tuple, TYPE_CHECKING
import random

from core.game_objects import Direction, RoomColor, RoomEffect, GameObject

if TYPE_CHECKING:
    from game1.player import Player


class Door:
    """Représente une porte entre deux pièces"""

    def __init__(self, direction: Direction, lock_level: int = 0, key_cost: int = 0):
        """
        direction: Direction de la porte
        lock_level: 0 = déverrouillée, 1 = verrouillée, 2 = verrouillée à double tour
        key_cost: Nombre de clés à dépenser pour traverser cette porte (0 = gratuit)
        """
        self.direction = direction
        self.lock_level = lock_level
        self.key_cost = key_cost  # Coût en clés pour traverser
        self.is_opened = False

    def can_open(self, player: 'Player', check_key_cost: bool = True) -> bool:
        """Vérifie si le joueur peut ouvrir la porte"""
        if self.is_opened:
            return True

        # Vérifier le coût en clés pour traverser (indépendant du verrouillage)
        if check_key_cost and self.key_cost > 0:
            if player.inventory.keys.quantity < self.key_cost:
                return False

        if self.lock_level == 0:
            return True

        # Vérifier si le joueur a un kit de crochetage pour niveau 1
        if self.lock_level == 1 and player.inventory.has_permanent_item("Kit de crochetage"):
            return True

        # Sinon, nécessite une clé pour le verrouillage
        if player.inventory.keys.quantity > 0:
            return True

        return False

    def open(self, player: 'Player', spend_key_cost: bool = True) -> bool:
        """Ouvre la porte et dépense les clés si nécessaire"""
        if self.is_opened:
            # Si la porte est déjà ouverte mais nécessite un coût pour traverser
            if spend_key_cost and self.key_cost > 0:
                if player.inventory.keys.quantity >= self.key_cost:
                    for _ in range(self.key_cost):
                        player.inventory.spend_key()
                    print(f"🔑 Vous dépensez {self.key_cost} clé(s) pour traverser cette porte.")
                    return True
                else:
                    print(f"❌ Vous avez besoin de {self.key_cost} clé(s) pour traverser cette porte.")
                    return False
            return True

        if self.lock_level == 0:
            self.is_opened = True
            # Dépenser les clés pour traverser si nécessaire
            if spend_key_cost and self.key_cost > 0:
                if player.inventory.keys.quantity >= self.key_cost:
                    for _ in range(self.key_cost):
                        player.inventory.spend_key()
                    print(f"🔑 Vous dépensez {self.key_cost} clé(s) pour traverser cette porte.")
                    return True
                else:
                    self.is_opened = False  # Annuler l'ouverture
                    print(f"❌ Vous avez besoin de {self.key_cost} clé(s) pour traverser cette porte.")
                    return False
            return True

        # Kit de crochetage pour niveau 1
        if self.lock_level == 1 and player.inventory.has_permanent_item("Kit de crochetage"):
            self.is_opened = True
            print("Porte crochetée!")
            # Dépenser les clés pour traverser si nécessaire
            if spend_key_cost and self.key_cost > 0:
                if player.inventory.keys.quantity >= self.key_cost:
                    for _ in range(self.key_cost):
                        player.inventory.spend_key()
                    print(f"🔑 Vous dépensez {self.key_cost} clé(s) pour traverser cette porte.")
                    return True
                else:
                    self.is_opened = False  # Annuler l'ouverture
                    print(f"❌ Vous avez besoin de {self.key_cost} clé(s) pour traverser cette porte.")
                    return False
            return True

        # Utiliser une clé pour le verrouillage
        if player.inventory.spend_key():
            self.is_opened = True
            print(f"Porte ouverte avec une clé! (Niveau {self.lock_level})")
            # Dépenser les clés supplémentaires pour traverser si nécessaire
            if spend_key_cost and self.key_cost > 0:
                if player.inventory.keys.quantity >= self.key_cost:
                    for _ in range(self.key_cost):
                        player.inventory.spend_key()
                    print(f"🔑 Vous dépensez {self.key_cost} clé(s) supplémentaires pour traverser cette porte.")
                    return True
                else:
                    print(f"❌ Porte ouverte mais vous avez besoin de {self.key_cost} clé(s) supplémentaires pour traverser.")
                    return False
            return True

        print(f"Vous avez besoin d'une clé pour ouvrir cette porte (niveau {self.lock_level}).")
        return False

    def get_lock_description(self) -> str:
        """Retourne une description du niveau de verrouillage"""
        if self.lock_level == 0:
            return "déverrouillée"
        elif self.lock_level == 1:
            return "verrouillée"
        else:
            return "verrouillée à double tour"


class Room:
    """Représente une pièce du manoir"""

    def __init__(
            self,
            name: str,
            color: RoomColor,
            doors: List[Direction],
            gem_cost: int = 0,
            rarity: int = 0,
            objects: Optional[List[GameObject]] = None,
            effect: Optional[RoomEffect] = None,
            image_path: Optional[str] = None,
            placement_condition: Optional[callable] = None,
            key_cost_doors: Optional[dict[Direction, int]] = None,
            specific_door_locks: Optional[dict[Direction, int]] = None
    ):
        """
        name: Nom de la pièce
        color: Couleur de la pièce
        doors: Liste des directions où il y a des portes
        gem_cost: Coût en gemmes pour choisir cette pièce
        rarity: Degré de rareté (0-3, plus élevé = plus rare)
        objects: Liste des objets dans la pièce
        effect: Effet spécial de la pièce
        image_path: Chemin vers l'image de la pièce
        placement_condition: Fonction qui vérifie si la pièce peut être placée à une position
        key_cost_doors: Dict {Direction: key_cost} - Portes qui nécessitent des clés pour traverser
        specific_door_locks: Dict {Direction: lock_level} - Verrouillage spécifique pour certaines portes
        """
        self.name = name
        self.color = color
        self.doors_directions = doors
        self.gem_cost = gem_cost
        self.rarity = rarity
        self.objects = objects if objects else []
        self.effect = effect
        self.image_path = image_path
        self.placement_condition = placement_condition
        self.key_cost_doors = key_cost_doors if key_cost_doors else {}
        self.specific_door_locks = specific_door_locks if specific_door_locks else {}

        # Portes réelles avec leur niveau de verrouillage (créées lors du placement)
        self.doors: dict[Direction, Door] = {}

        # Position dans la grille
        self.position: Optional[Tuple[int, int]] = None

        # Indique si le joueur a déjà visité la pièce
        self.visited = False

        # Rotation appliquée (0, 90, 180, 270). Affecte uniquement la logique des portes.
        self.rotation_degrees = 0

    def initialize_doors(self, row: int, total_rows: int):
        """Initialise les portes avec des niveaux de verrouillage aléatoires"""
        for direction in self.doors_directions:
            # Vérifier si cette porte a un verrouillage spécifique
            if direction in self.specific_door_locks:
                lock_level = self.specific_door_locks[direction]
            else:
                # Calculer le niveau de verrouillage en fonction de la progression
                lock_level = self._calculate_lock_level(row, total_rows)
            
            # Vérifier si cette porte a un coût en clés
            key_cost = self.key_cost_doors.get(direction, 0)
            self.doors[direction] = Door(direction, lock_level, key_cost)

    def _calculate_lock_level(self, row: int, total_rows: int) -> int:
        """Calcule le niveau de verrouillage en fonction de la position"""
        if row == 0:
            # Première rangée: toujours déverrouillé
            return 0
        elif row == total_rows - 1:
            # Dernière rangée: toujours verrouillé à double tour
            return 2
        else:
            # Probabilité croissante de verrouillage
            progress = row / total_rows
            rand = random.random()

            if rand < progress * 0.3:
                return 2  # Double tour
            elif rand < progress * 0.6:
                return 1  # Verrouillé
            else:
                return 0  # Déverrouillé

    def get_door(self, direction: Direction) -> Optional[Door]:
        """Récupère la porte dans une direction donnée"""
        return self.doors.get(direction)

    def has_door(self, direction: Direction) -> bool:
        """Vérifie si la pièce a une porte dans une direction"""
        return direction in self.doors_directions

    def enter(self, player: 'Player') -> None:
        """Appelé quand le joueur entre dans la pièce"""
        self.visited = True

        # ========================================
        # APPLIQUER LES RÈGLES PAR COULEUR
        # ========================================
        
        if self.color == RoomColor.YELLOW:
            # 🟡 MAGASINS: Échange d'or contre des objets
            print("💰 Vous entrez dans un magasin. Vous pouvez échanger de l'or contre des objets.")
            # TODO: Implémenter la logique d'achat
            
        elif self.color == RoomColor.GREEN:
            # 🟢 JARDINS: Gemmes, trous à creuser, objets permanents
            print("🌿 Vous entrez dans un jardin. Cherchez des gemmes et des endroits où creuser!")
            # Les jardins ont souvent des gemmes (déjà dans objects)
            
        elif self.color == RoomColor.PURPLE:
            # 🟣 CHAMBRES: Effets permettant de regagner des pas
            print("😴 Vous entrez dans une chambre. Un lieu de repos.")
            # TODO: Ajouter effet de récupération automatique
            # Exemple: player.inventory.steps.quantity += 2
            
        elif self.color == RoomColor.ORANGE:
            # 🟠 COULOIRS: Beaucoup de portes
            print("🚪 Vous êtes dans un couloir avec plusieurs portes.")
            # Les couloirs ont déjà beaucoup de portes (dans doors_directions)
            
        elif self.color == RoomColor.RED:
            # 🔴 INDÉSIRABLES: Caractéristiques négatives
            print("⚠️ Attention! Cette pièce semble dangereuse...")
            # TODO: Effet négatif (retirer des pas, etc.)
            # Exemple: player.inventory.steps.quantity -= 2
            
        elif self.color == RoomColor.BLUE:
            # 🔵 COMMUNES: Effets variés
            print(f"🏠 Vous entrez dans {self.name}.")
            # Les pièces bleues ont des effets variés (gérés par self.effect)

        # Appliquer l'effet de la pièce si elle en a un
        if self.effect and hasattr(self.effect, 'on_enter'):
            self.effect.on_enter(player, self)

    def get_probability_weight(self) -> float:
        """Calcule le poids de probabilité basé sur la rareté"""
        # Chaque niveau de rareté divise la probabilité par 3
        return 1.0 / (3 ** self.rarity)

    def can_be_placed(self, row: int, col: int, grid_height: int, grid_width: int) -> bool:
        """Vérifie si la pièce peut être placée à cette position"""
        # Vérifier la condition de placement personnalisée
        if self.placement_condition:
            return self.placement_condition(row, col, grid_height, grid_width)
        return True

    def interact_with_object(self, object_index: int, player: 'Player') -> bool:
        """Interagir avec un objet de la pièce"""
        if 0 <= object_index < len(self.objects):
            obj = self.objects[object_index]
            success = obj.interact(player)
            if success:
                from items import InteractiveObject, Food
                if isinstance(obj, (InteractiveObject, Food)):
                    # Retirer l'objet de la pièce après interaction réussie
                    self.objects.pop(object_index)
            return success
        return False

    def __str__(self):
        return f"{self.name} ({self.color.value})"

    def __repr__(self):
        return f"Room({self.name}, cost={self.gem_cost}, rarity={self.rarity})"

    def rotate(self, degrees: int) -> None:
        """Rotate the room's logical door directions clockwise by degrees (must be 0,90,180,270).
        This mutates self.doors_directions so later initialization reflects the rotation.
        """
        if degrees % 90 != 0:
            raise ValueError("degrees must be a multiple of 90")

        degrees = degrees % 360
        if degrees == 0:
            return

        # clockwise rotation mapping
        order = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        mapping = {}
        steps = (degrees // 90) % 4
        for i, d in enumerate(order):
            mapping[d] = order[(i + steps) % 4]

        # apply mapping to doors_directions
        rotated = [mapping.get(d, d) for d in self.doors_directions]
        # deduplicate while preserving order
        seen = set()
        new_doors = []
        for d in rotated:
            if d not in seen:
                seen.add(d)
                new_doors.append(d)

        self.doors_directions = new_doors
        
        # Rotate key_cost_doors
        if self.key_cost_doors:
            rotated_key_cost = {}
            for direction, cost in self.key_cost_doors.items():
                new_direction = mapping.get(direction, direction)
                rotated_key_cost[new_direction] = cost
            self.key_cost_doors = rotated_key_cost
        
        # Rotate specific_door_locks
        if self.specific_door_locks:
            rotated_locks = {}
            for direction, lock_level in self.specific_door_locks.items():
                new_direction = mapping.get(direction, direction)
                rotated_locks[new_direction] = lock_level
            self.specific_door_locks = rotated_locks
        
        self.rotation_degrees = degrees
        self.rotation_degrees = degrees