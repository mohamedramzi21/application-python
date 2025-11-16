"""
Classe Game - Moteur principal du jeu
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enum import Enum
from typing import List, Optional
import random

from game1.player import Player
from game1.manor import Manor
from core.game_objects import Direction
from rooms.catalog import RoomCatalog





class GameState(Enum):
    """États possibles du jeu"""
    ROOM_SELECTION = "room_selection"  # Choix d'une pièce
    PLAYING = "playing"                 # En jeu normal
    ROOM_INTERACTION = "room_interaction"  # Interaction avec objets dans la pièce
    GAME_OVER = "game_over"            # Défaite
    GAME_WON = "game_won"              # Victoire


class Game:
    """Moteur principal du jeu Blue Prince"""

    def __init__(self):
        self.player = Player()
        self.manor = Manor(width=5, height=9)
        self.catalog = RoomCatalog()
        self.state = GameState.PLAYING  # Commencer en mode PLAYING pour choisir direction

        # Pièces proposées pour le choix
        self.pending_room_selection: List = []
        
        # Direction sélectionnée pour placer la nouvelle pièce
        self.selected_direction: Optional[Direction] = None
        
        # Variables pour l'interaction avec les objets
        self.room_objects: List = []  # Objets disponibles dans la pièce actuelle
        self.selected_object_index: int = 0  # Index de l'objet sélectionné
        
        # Track des chambres déjà utilisées (par nom)
        self.used_room_names: set = set()

        # Démarrer par l'Entrance Hall en dernière ligne, colonne 3
        entrance = self.catalog.get_entrance()
        if entrance:
            entrance_row = self.manor.height - 1  # Dernière ligne (4 pour un grid 5x5)
            entrance_col = 2  # Colonne 3 (index 2)
            self.manor.place_room(entrance, entrance_row, entrance_col)
            self.player.position = (entrance_row, entrance_col)
            self.used_room_names.add(entrance.name)  # Marquer comme utilisée
            print(f"🏰 Jeu démarré à l'Entrance Hall en position {self.player.position}")

        # Placer l'Antechamber comme point d'arrivée en ligne 2, colonne 3
        antechamber = self.catalog.get_room_by_name("Antechamber")
        if antechamber:
            goal_row = 0  # Ligne 2 (index 1)
            goal_col = 2  # Colonne 3 (index 2)
            self.manor.place_room(antechamber, goal_row, goal_col)
            self.used_room_names.add(antechamber.name)  # Marquer comme utilisée
            print(f"🎯 Objectif: Antechamber placée en position ({goal_row}, {goal_col})")

        # Message pour inviter à choisir une direction
        print("\n🧭 Choisissez une direction pour placer votre première pièce:")
        print("   W = Nord  |  A = Ouest  |  D = Est")

    def generate_room_selection(self):
        """Génère 3 pièces aléatoires pour le choix (version simplifiée)"""
        # Obtenir la direction opposée
        opposite_direction = None
        if self.selected_direction:
            opposite_map = {
                Direction.NORTH: Direction.SOUTH,
                Direction.SOUTH: Direction.NORTH,
                Direction.EAST: Direction.WEST,
                Direction.WEST: Direction.EAST
            }
            opposite_direction = opposite_map.get(self.selected_direction)
            print(f"🔄 Direction choisie: {self.selected_direction.value} → Les chambres doivent avoir une porte {opposite_direction.value}")
        
        # Calculer les portes interdites selon la position cible
        current_pos = self.player.position
        target_pos = self.manor.get_adjacent_position(current_pos, self.selected_direction) if self.selected_direction else None
        
        forbidden_doors = []
        if target_pos:
            row, col = target_pos
            # Interdire les portes qui donneraient sur l'extérieur du manoir
            if row == 0:
                forbidden_doors.append(Direction.NORTH)
            if row == self.manor.height - 1:
                forbidden_doors.append(Direction.SOUTH)
            if col == 0:
                forbidden_doors.append(Direction.WEST)
            if col == self.manor.width - 1:
                forbidden_doors.append(Direction.EAST)
            
            if forbidden_doors:
                forbidden_str = ', '.join([d.value for d in forbidden_doors])
                print(f"🚫 Portes interdites à cette position: {forbidden_str}")
        
        # Pour les tests: toujours proposer les mêmes pièces
        all_rooms = self.catalog.get_all_rooms()
        
        # Filtrer l'entrance, l'antechamber ET les chambres déjà utilisées
        available_rooms = [
            r for r in all_rooms 
            if r.name not in ["Entrance Hall", "Antechamber"] 
            and r.name not in self.used_room_names
        ]
        
        if len(available_rooms) == 0:
            print("❌ Plus aucune chambre disponible!")
            print("   Toutes les chambres ont été utilisées.")
            self.pending_room_selection = []
            return
        
        print(f"🏠 {len(available_rooms)} chambre(s) non utilisée(s) disponible(s)")
        
        # Filtrer les chambres qui ont une porte dans la direction OPPOSÉE
        if opposite_direction:
            compatible_rooms = [r for r in available_rooms if opposite_direction in r.doors_directions]
            
            if len(compatible_rooms) == 0:
                print(f"⚠️ Aucune chambre compatible avec porte {opposite_direction.value}!")
                print(f"   Proposition de chambres sans cette restriction...")
                compatible_rooms = available_rooms
            elif len(compatible_rooms) < 3:
                print(f"ℹ️  Seulement {len(compatible_rooms)} chambre(s) compatible(s) avec porte {opposite_direction.value}")
        else:
            compatible_rooms = available_rooms
        
        # Filtrer les chambres qui n'ont AUCUNE porte interdite
        if forbidden_doors:
            compatible_rooms = [
                r for r in compatible_rooms 
                if not any(door in forbidden_doors for door in r.doors_directions)
            ]
            print(f"✅ {len(compatible_rooms)} chambre(s) sans portes interdites")
        
        # Choisir jusqu'à 3 pièces (ou moins si pas assez disponibles)
        num_to_select = min(3, len(compatible_rooms))
        if num_to_select > 0:
            self.pending_room_selection = random.sample(compatible_rooms, num_to_select)
        else:
            self.pending_room_selection = []
            print("❌ Aucune chambre disponible!")
            return
        
        self.state = GameState.ROOM_SELECTION
        
        # Message adapté selon le nombre de chambres
        if len(self.pending_room_selection) == 1:
            print(f"\n🎲 1 chambre proposée:")
        elif len(self.pending_room_selection) == 2:
            print(f"\n🎲 2 chambres proposées:")
        else:
            print(f"\n🎲 3 chambres proposées:")
            
        for i, room in enumerate(self.pending_room_selection):
            cost = f"💎 {room.gem_cost}" if room.gem_cost > 0 else "Gratuit"
            doors_str = ', '.join([d.value for d in room.doors_directions])
            print(f"  {i+1}. {room.name} ({cost}) - Portes: {doors_str}")

    def select_room(self, index: int) -> bool:
        """Sélectionne une pièce parmi les choix"""
        if not (0 <= index < len(self.pending_room_selection)):
            return False

        selected_room = self.pending_room_selection[index]

        # Vérifier le coût en gemmes
        if selected_room.gem_cost > 0:
            if not self.player.inventory.spend_gems(selected_room.gem_cost):
                print(f"❌ Pas assez de gemmes! (besoin: {selected_room.gem_cost})")
                return False

        # Utiliser la direction sélectionnée pour placer la pièce
        current_pos = self.player.position
        
        if self.selected_direction:
            # Placer dans la direction choisie
            new_pos = self.manor.get_adjacent_position(current_pos, self.selected_direction)
            if new_pos and self.manor.get_room(*new_pos) is None:
                # Dépenser 1 pas pour placer la pièce
                if not self.player.inventory.use_steps(1):
                    print("❌ Plus de pas disponibles!")
                    self.state = GameState.GAME_OVER
                    return False
                
                # Place la pièce
                self.manor.place_room(selected_room, *new_pos)
                print(f"✓ Pièce '{selected_room.name}' placée en {new_pos} ({self.selected_direction.value})")
                
                # Marquer la chambre comme utilisée
                self.used_room_names.add(selected_room.name)
                print(f"📝 Chambre '{selected_room.name}' marquée comme utilisée ({len(self.used_room_names)} chambres utilisées au total)")
                
                # Déplacer le joueur dans la nouvelle pièce
                self.player.position = new_pos
                print(f"✓ Vous entrez dans {selected_room.name} (pas restants: {self.player.inventory.steps.quantity})")
                
                # Si c'est une pièce rouge, retirer automatiquement 2-10 pas
                from core.game_objects import RoomColor
                if selected_room.color == RoomColor.RED:
                    import random
                    steps_lost = random.randint(2, 10)
                    self.player.inventory.steps.quantity -= steps_lost
                    print(f"⚠️ DANGER! Cette pièce vous fait perdre {steps_lost} pas! (pas restants: {self.player.inventory.steps.quantity})")
                
                # Réinitialiser la direction
                self.selected_direction = None
                
                # Passer en mode jeu
                self.state = GameState.PLAYING
                
                # Activer automatiquement le mode interaction si la chambre a des objets
                if len(selected_room.objects) > 0:
                    self.enter_room_interaction()
                
                return True
            else:
                print(f"❌ Position {new_pos} occupée ou invalide")
                return False
        else:
            # Fallback: chercher n'importe quelle position adjacente
            directions = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
            for direction in directions:
                new_pos = self.manor.get_adjacent_position(current_pos, direction)
                if new_pos and self.manor.get_room(*new_pos) is None:
                    # Dépenser 1 pas pour placer la pièce
                    if not self.player.inventory.use_steps(1):
                        print("❌ Plus de pas disponibles!")
                        self.state = GameState.GAME_OVER
                        return False
                    
                    self.manor.place_room(selected_room, *new_pos)
                    print(f"✓ Pièce '{selected_room.name}' placée en {new_pos}")
                    
                    self.player.position = new_pos
                    print(f"✓ Vous entrez dans {selected_room.name} (pas restants: {self.player.inventory.steps.quantity})")
                    
                    self.state = GameState.PLAYING
                    return True

        print("❌ Impossible de placer la pièce")
        return False

    def reroll_rooms(self) -> bool:
        """Relancer le choix de pièces avec un dé"""
        if self.player.inventory.spend_dice():
            print("🎲 Relance avec un dé!")
            self.generate_room_selection()
            return True
        else:
            print("❌ Pas de dés disponibles!")
            return False

    def try_move(self, direction: Direction) -> bool:
        """Tente de se déplacer dans une direction"""
        print(f"🚶 try_move() appelé: direction={direction.value}, état={self.state.value}")
        
        if self.state != GameState.PLAYING:
            print(f"❌ État incorrect: {self.state.value}")
            return False

        current_pos = self.player.position
        current_room = self.manor.get_room(*current_pos)

        if not current_room:
            print("❌ Pas de pièce actuelle!")
            return False

        # Calculer la nouvelle position
        new_pos = self.manor.get_adjacent_position(current_pos, direction)
        if not new_pos:
            print("❌ Hors limites du manoir!")
            return False

        # Vérifier s'il y a une pièce à destination
        dest_room = self.manor.get_room(*new_pos)
        if not dest_room:
            # Pas de pièce dans cette direction - ne rien faire
            print(f"❌ Aucune pièce au {direction.value}. Utilisez W/A/S/D + ESPACE pour ouvrir une nouvelle porte.")
            return False

        # Vérifier si la chambre actuelle a une porte dans cette direction
        if not current_room.has_door(direction):
            print(f"❌ Pas de porte au {direction.value} dans {current_room.name}")
            return False

        # NOUVEAU: Vérifier si la chambre de destination a une porte dans la direction opposée
        opposite_direction = direction.opposite()
        if not dest_room.has_door(opposite_direction):
            print(f"❌ La chambre {dest_room.name} n'a pas de porte au {opposite_direction.value} (direction opposée)")
            print(f"   Vous ne pouvez pas entrer dans cette chambre depuis {direction.value}")
            return False

        door = current_room.get_door(direction)
        
        # Vérifier si la porte est verrouillée
        if door and not door.can_open(self.player):
            print(f"🔒 La porte est verrouillée (niveau {door.lock_level})!")
            return False
        
        # Ouvrir la porte si elle n'est pas encore ouverte
        if door and not door.is_opened:
            if not door.open(self.player):
                return False
            print(f"🚪 Porte ouverte vers {direction.value}")
        else:
            print(f"🚪 Passage par la porte déjà ouverte au {direction.value}")

        # Déplacement avec consommation de 1 pas
        if not self.player.inventory.use_steps(1):
            print("💀 YOU LOSE! HARD LUCK, NEXT TIME!")
            print("❌ Plus de pas disponibles!")
            self.state = GameState.GAME_OVER
            return False
            
        self.player.position = new_pos
        print(f"✓ Déplacement vers {dest_room.name} (pas restants: {self.player.inventory.steps.quantity})")
        
        # Si c'est une pièce rouge, retirer automatiquement 2-10 pas
        from core.game_objects import RoomColor
        if dest_room.color == RoomColor.RED:
            import random
            steps_lost = random.randint(2, 10)
            self.player.inventory.steps.quantity -= steps_lost
            print(f"⚠️ DANGER! Cette pièce vous fait perdre {steps_lost} pas! (pas restants: {self.player.inventory.steps.quantity})")
        
        # Appeler la méthode enter() de la pièce pour appliquer les effets (magasin, etc.)
        dest_room.enter(self.player)
        
        # Vérifier si c'est l'Antechamber (victoire)
        if dest_room.name == "Antechamber":
            self.state = GameState.GAME_WON
            print("🎉 VICTOIRE! Vous avez atteint l'Antechamber!")
            return True
        
        # Activer automatiquement le mode interaction si la chambre a des objets
        if len(dest_room.objects) > 0:
            self.enter_room_interaction()
        
        return True

    def interact_with_object(self, object_index: int):
        """Interagit avec un objet dans la pièce actuelle"""
        current_room = self.manor.get_room(*self.player.position)
        if not current_room:
            return

        if 0 <= object_index < len(current_room.objects):
            obj = current_room.objects[object_index]
            print(f"🔍 Interaction avec: {obj.name}")
            obj.interact(self.player)
        else:
            print(f"❌ Pas d'objet à l'index {object_index}")

    def enter_room_interaction(self):
        """Entre en mode interaction avec les objets de la pièce actuelle"""
        current_room = self.manor.get_room(*self.player.position)
        if current_room and len(current_room.objects) > 0:
            self.room_objects = current_room.objects.copy()
            self.selected_object_index = 0
            self.state = GameState.ROOM_INTERACTION
            print(f"🚪 Entrée dans {current_room.name} - {len(self.room_objects)} objets disponibles")
            return True
        return False
    
    def navigate_objects(self, direction: int):
        """Navigue dans la liste d'objets (direction: -1 pour haut, +1 pour bas)"""
        if self.state != GameState.ROOM_INTERACTION or len(self.room_objects) == 0:
            return
        
        self.selected_object_index = (self.selected_object_index + direction) % len(self.room_objects)
        print(f"📍 Objet sélectionné: {self.room_objects[self.selected_object_index].name}")
    
    def take_selected_object(self):
        """Prend l'objet sélectionné"""
        if self.state != GameState.ROOM_INTERACTION or len(self.room_objects) == 0:
            return False
        
        if 0 <= self.selected_object_index < len(self.room_objects):
            obj = self.room_objects[self.selected_object_index]
            
            # Vérifier si c'est un objet interactif (coffret, coffre, etc.)
            from core.game_objects import InteractiveObject
            if isinstance(obj, InteractiveObject):
                # Vérifier si on peut l'ouvrir (comme Gold avec Shovel)
                if obj.can_open(self.player):
                    # OUVRIR LE COFFRET : remplacer par son contenu dans la liste
                    print(f"✅ {obj.name} ouvert!")
                    print(f"📦 Contenu du coffret:")
                    for content_item in obj.contents:
                        print(f"   - {content_item.name}")
                    
                    # Retirer le coffret de la liste
                    self.room_objects.pop(self.selected_object_index)
                    current_room = self.manor.get_room(*self.player.position)
                    if current_room:
                        try:
                            current_room.objects.remove(obj)
                        except ValueError:
                            pass
                    
                    # AJOUTER les objets du coffret à la liste des objets disponibles
                    for content_item in obj.contents:
                        self.room_objects.insert(self.selected_object_index, content_item)
                        if current_room:
                            current_room.objects.append(content_item)
                    
                    print("💡 Vous pouvez maintenant ramasser les objets un par un avec R")
                    
                    # Ajuster l'index pour pointer sur le premier objet du coffret
                    if len(self.room_objects) > 0:
                        self.selected_object_index = min(self.selected_object_index, len(self.room_objects) - 1)
                    
                    return True
                else:
                    # Ne peut pas ouvrir - Comme Gold sans Shovel, on peut ESC et revenir
                    return False
            
            # Objet normal (non-interactif) - Vérifier d'abord si c'est ramassable
            can_take = self._add_to_inventory(obj)
            
            # Si on ne peut pas prendre (ex: Gold sans Shovel), ne pas retirer
            if can_take == False:
                return False
            
            # Retirer de la liste et de la pièce
            self.room_objects.pop(self.selected_object_index)
            current_room = self.manor.get_room(*self.player.position)
            if current_room:
                try:
                    current_room.objects.remove(obj)
                except ValueError:
                    pass
            
            # Ajuster l'index si nécessaire
            if self.selected_object_index >= len(self.room_objects) and self.selected_object_index > 0:
                self.selected_object_index -= 1
            
            # Si plus d'objets, sortir du mode interaction
            if len(self.room_objects) == 0:
                self.exit_room_interaction()
            
            return True
        return False
    
    def _add_to_inventory(self, obj):
        """Ajoute un objet à l'inventaire du joueur"""
        if obj.name == "Gâteau" or obj.name == "Cake":
            self.player.inventory.steps.quantity += 10
            print(f"🍰 Cake ramassé! +10 pas (Total: {self.player.inventory.steps.quantity})")
        elif obj.name == "Gold" or obj.name == "Or":
            # Tout l'or nécessite la pelle (Shovel)
            if self.player.inventory.has_permanent_item("Shovel"):
                self.player.inventory.gold.quantity += obj.quantity
                print(f"💰 Gold ramassé! +{obj.quantity} pièces d'or (Total: {self.player.inventory.gold.quantity})")
            else:
                print("❗ Vous devez d'abord trouver la pelle (Shovel). Revenez ensuite pour récupérer l'or.")
                return False
        elif obj.name == "Gemmes" or obj.name == "Gems":
            self.player.inventory.gems.quantity += obj.quantity
            print(f"💎 Gem ramassée! (Total: {self.player.inventory.gems.quantity})")
        elif obj.name == "Clés" or obj.name == "Keys":
            self.player.inventory.keys.quantity += obj.quantity
            print(f"🔑 Key ramassée! (Total: {self.player.inventory.keys.quantity})")
        elif obj.name == "Dés" or obj.name == "Dice":
            self.player.inventory.dice.quantity += obj.quantity
            print(f"🎲 Dice ramassé! (Total: {self.player.inventory.dice.quantity})")
        elif obj.name == "Shovel" or obj.name == "Pelle":
            added = self.player.inventory.add_permanent_item(obj)
            if added:
                print(f"🛠️  Vous avez trouvé la pelle! ({obj.name})")
            else:
                print(f"ℹ️  Vous possédez déjà l'objet permanent: {obj.name}")
        elif obj.name == "Marteau" or obj.name == "Hammer":
            added = self.player.inventory.add_permanent_item(obj)
            if added:
                print(f"🔨 Vous avez trouvé le marteau! ({obj.name})")
            else:
                print(f"ℹ️  Vous possédez déjà l'objet permanent: {obj.name}")
        else:
            print(f"✅ {obj.name} ramassé!")
        
        return True
    
    def exit_room_interaction(self):
        """Sort du mode interaction"""
        self.state = GameState.PLAYING
        self.room_objects = []
        self.selected_object_index = 0
        print("🚪 Sortie du mode interaction")

    def is_game_over(self) -> bool:
        """Vérifie si le jeu est terminé"""
        if not self.player.is_alive():
            self.state = GameState.GAME_OVER
            return True
        return self.state in [GameState.GAME_OVER, GameState.GAME_WON]

    def __str__(self):
        return f"{self.manor}\n{self.player}\nÉtat: {self.state.value}"
