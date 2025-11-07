"""Test de la décrémentation des pas"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game1.game import Game
from core.game_objects import Direction

# Créer le jeu
game = Game()

print(f"🎮 Début du test")
print(f"   Position: {game.player.position}")
print(f"   Pas: {game.player.inventory.steps.quantity}")

# Placer une pièce au nord pour pouvoir se déplacer
from rooms.catalog import RoomCatalog
catalog = RoomCatalog()
all_rooms = catalog.get_all_rooms()

# Trouver une pièce simple
test_room = None
for room in all_rooms:
    if room.name not in ["Entrance Hall", "Antechamber"] and room.gem_cost == 0:
        test_room = room
        break

if not test_room:
    test_room = all_rooms[1]  # N'importe quelle pièce

# Placer la pièce au nord
north_pos = game.manor.get_adjacent_position(game.player.position, Direction.NORTH)
if north_pos:
    game.manor.place_room(test_room, *north_pos)
    print(f"✓ Pièce '{test_room.name}' placée au nord en {north_pos}")
    
    # Passer en mode PLAYING
    game.state = game.GameState.PLAYING if hasattr(game, 'GameState') else game.state
    from game1.game import GameState
    game.state = GameState.PLAYING
    
    print(f"\n📍 Avant le mouvement:")
    print(f"   Position: {game.player.position}")
    print(f"   Pas: {game.player.inventory.steps.quantity}")
    
    # Essayer de se déplacer vers le nord
    success = game.try_move(Direction.NORTH)
    
    print(f"\n📍 Après le mouvement:")
    print(f"   Succès: {success}")
    print(f"   Position: {game.player.position}")
    print(f"   Pas: {game.player.inventory.steps.quantity}")
    
    if game.player.inventory.steps.quantity == 69:
        print("\n✅ TEST RÉUSSI! Les pas ont diminué de 70 à 69")
    else:
        print(f"\n❌ TEST ÉCHOUÉ! Les pas devraient être à 69, mais sont à {game.player.inventory.steps.quantity}")
