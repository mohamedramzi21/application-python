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
    GAME_OVER = "game_over"            # Défaite
    GAME_WON = "game_won"              # Victoire


class Game:
    """Moteur principal du jeu Blue Prince"""

    def __init__(self):
        self.player = Player()
        self.manor = Manor(width=5, height=5)
        self.catalog = RoomCatalog()
        self.state = GameState.ROOM_SELECTION

        # Pièces proposées pour le choix
        self.pending_room_selection: List = []
        
        # Direction sélectionnée pour placer la nouvelle pièce
        self.selected_direction: Optional[Direction] = None

        # Démarrer par l'Entrance Hall au centre
        entrance = self.catalog.get_entrance()
        if entrance:
            center_row = self.manor.height // 2
            center_col = self.manor.width // 2
            self.manor.place_room(entrance, center_row, center_col)
            self.player.position = (center_row, center_col)
            print(f"🏰 Jeu démarré à l'Entrance Hall en position {self.player.position}")

        # Proposer 3 pièces pour commencer
        self.generate_room_selection()

    def generate_room_selection(self):
        """Génère 3 pièces aléatoires pour le choix (version simplifiée)"""
        # Pour les tests: toujours proposer les mêmes pièces
        all_rooms = self.catalog.get_all_rooms()
        
        # Filtrer l'entrance et l'antechamber
        available_rooms = [r for r in all_rooms if r.name not in ["Entrance Hall", "Antechamber"]]
        
        # Choisir 3 pièces aléatoires
        if len(available_rooms) >= 3:
            self.pending_room_selection = random.sample(available_rooms, 3)
        else:
            self.pending_room_selection = available_rooms[:3]
        
        self.state = GameState.ROOM_SELECTION
        print(f"\n🎲 3 nouvelles pièces proposées:")
        for i, room in enumerate(self.pending_room_selection):
            cost = f"💎 {room.gem_cost}" if room.gem_cost > 0 else "Gratuit"
            print(f"  {i+1}. {room.name} ({cost}) - {len(room.doors_directions)} portes")

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
                
                # Déplacer le joueur dans la nouvelle pièce
                self.player.position = new_pos
                print(f"✓ Vous entrez dans {selected_room.name} (pas restants: {self.player.inventory.steps.quantity})")
                
                # Réinitialiser la direction
                self.selected_direction = None
                
                # Passer en mode jeu
                self.state = GameState.PLAYING
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

        # Vérifier si la pièce a une porte dans cette direction
        if not current_room.has_door(direction):
            print(f"❌ Pas de porte au {direction.value}!")
            return False

        # Vérifier si la porte peut être ouverte
        door = current_room.get_door(direction)
        if door and not door.can_open(self.player):
            print(f"🔒 La porte est verrouillée (niveau {door.lock_level})!")
            return False

        # Calculer la nouvelle position
        new_pos = self.manor.get_adjacent_position(current_pos, direction)
        if not new_pos:
            print("❌ Hors limites du manoir!")
            return False

        # Vérifier s'il y a une pièce à destination
        dest_room = self.manor.get_room(*new_pos)
        if not dest_room:
            print("❌ Aucune pièce dans cette direction! Choisissez une nouvelle pièce.")
            self.generate_room_selection()
            return False

        # Ouvrir la porte si nécessaire
        if door and not door.is_opened:
            if not door.open(self.player):
                return False

        # Déplacer le joueur SANS dépenser de pas (les pas sont dépensés au placement de pièce)
        self.player.position = new_pos
        print(f"✓ Déplacement vers {dest_room.name} (pas restants: {self.player.inventory.steps.quantity})")
        
        # Vérifier si c'est l'Antechamber (victoire)
        if dest_room.name == "Antechamber":
            self.state = GameState.GAME_WON
            print("🎉 VICTOIRE! Vous avez atteint l'Antechamber!")
        
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

    def is_game_over(self) -> bool:
        """Vérifie si le jeu est terminé"""
        if not self.player.is_alive():
            self.state = GameState.GAME_OVER
            return True
        return self.state in [GameState.GAME_OVER, GameState.GAME_WON]

    def __str__(self):
        return f"{self.manor}\n{self.player}\nÉtat: {self.state.value}"
