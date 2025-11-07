#!/usr/bin/env python3
"""
Test rapide pour vérifier que tous les modules fonctionnent
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🧪 TEST DES MODULES BLUE PRINCE")
print("=" * 60)

# Test 1: Import des modules de base
print("\n[1/8] Test imports core...")
try:
    from core.game_objects import Direction, RoomColor, GameObject
    print("✅ core.game_objects OK")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Test 2: Import items
print("\n[2/8] Test imports items...")
try:
    from items.consumables import Steps, Gold, Gems, Keys, Dice
    from items.food import Apple, Banana, Cake
    from items.permanent import Shovel, Hammer
    from items.interactive import Chest, DigSpot
    print("✅ items OK")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Test 3: Import rooms
print("\n[3/8] Test imports rooms...")
try:
    from rooms.room import Room, Door
    from rooms.catalog import RoomCatalog
    print("✅ rooms OK")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Test 4: Import game
print("\n[4/8] Test imports game...")
try:
    from game1.inventory import Inventory
    from game1.player import Player
    from game1.manor import Manor
    from game1.game import Game, GameState
    print("✅ game OK")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Test 5: Création d'un inventaire
print("\n[5/8] Test création inventaire...")
try:
    inv = Inventory()
    assert inv.steps.quantity == 70, "Pas devrait être 70"
    assert inv.gems.quantity == 2, "Gemmes devrait être 2"
    assert inv.gold.quantity == 0, "Or devrait être 0"
    print(f"✅ Inventaire créé: {inv.steps.quantity} pas, {inv.gems.quantity} gemmes")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Test 6: Création d'un joueur
print("\n[6/8] Test création joueur...")
try:
    player = Player()
    assert player.position == (0, 0), "Position initiale devrait être (0, 0)"
    assert player.is_alive(), "Joueur devrait être vivant"
    print(f"✅ Joueur créé à position {player.position}")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Test 7: Création du manoir
print("\n[7/8] Test création manoir...")
try:
    manor = Manor(5, 5)
    assert manor.width == 5, "Largeur devrait être 5"
    assert manor.height == 5, "Hauteur devrait être 5"
    print(f"✅ Manoir créé: {manor.width}x{manor.height}")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Test 8: Création du jeu
print("\n[8/8] Test création jeu...")
try:
    game = Game()
    assert game.player is not None, "Player devrait exister"
    assert game.manor is not None, "Manor devrait exister"
    assert game.state == GameState.ROOM_SELECTION, "État devrait être ROOM_SELECTION"
    assert len(game.pending_room_selection) == 3, "Devrait avoir 3 pièces proposées"
    print(f"✅ Jeu créé en état {game.state.value}")
    print(f"   Position: {game.player.position}")
    print(f"   Pièces proposées: {len(game.pending_room_selection)}")
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test bonus: Vérifier pygame
print("\n[BONUS] Test pygame...")
try:
    import pygame
    print(f"✅ Pygame installé: version {pygame.version.ver}")
except Exception as e:
    print(f"⚠️  Pygame non installé (requis pour l'interface graphique)")

print("\n" + "=" * 60)
print("✅ TOUS LES TESTS PASSÉS!")
print("=" * 60)
print("\n🎮 Le jeu est prêt à être lancé avec:")
print("   python3 run_game.py")
print()
