"""
Script pour tester la structure actuelle du projet
"""
import os
import sys

print("=" * 60)
print("ANALYSE DU PROJET BLUE PRINCE")
print("=" * 60)
print()

# Structure du projet
print("📁 STRUCTURE DU PROJET:")
print("-" * 60)

base_path = "/Users/adham/Documents/sorbonne manhag/MASTER ISI/Adham/PYTHON/projet_python/application-python"
os.chdir(base_path)

folders = ["core", "game", "items", "main", "rooms", "ui"]

for folder in folders:
    if os.path.exists(folder):
        print(f"\n📂 {folder}/")
        files = [f for f in os.listdir(folder) if f.endswith('.py')]
        for file in files:
            file_path = os.path.join(folder, file)
            size = os.path.getsize(file_path)
            print(f"   ├─ {file} ({size} bytes)")

print("\n" + "=" * 60)
print("📋 RÉSUMÉ DES FICHIERS IMPLÉMENTÉS:")
print("-" * 60)

implemented_files = {
    "core/game_objects.py": "Classes de base (GameObject, Food, ConsumableItem, etc.)",
    "items/consumables.py": "Ressources consommables (Steps, Gold, Gems, Keys, Dice)",
    "items/food.py": "Nourriture (Apple, Banana, Cake, Sandwich, Meal)",
    "items/permanent.py": "Objets permanents (Shovel, Hammer, LockpickKit, etc.)",
    "items/interactive.py": "Objets interactifs (Chest, DigSpot, Locker)",
    "rooms/room.py": "Classes Room et Door",
    "rooms/effects.py": "Effets spéciaux des pièces",
    "rooms/catalog.py": "Catalogue de pièces disponibles",
    "ui/game_ui.py": "Interface graphique Pygame",
    "main/main.py": "Point d'entrée du programme"
}

for file, description in implemented_files.items():
    status = "✅" if os.path.exists(file) else "❌"
    print(f"{status} {file}")
    print(f"   → {description}")
    print()

print("=" * 60)
print("⚠️  FICHIERS MANQUANTS:")
print("-" * 60)

missing_files = [
    "game/game.py - Classe principale Game",
    "game/player.py - Classe Player",
    "game/inventory.py - Classe Inventory",
    "game/manor.py - Classe Manor (grille du manoir)",
    "game/game_state.py - Enum GameState"
]

for missing in missing_files:
    print(f"❌ {missing}")

print("\n" + "=" * 60)
print("📝 CONCLUSION:")
print("-" * 60)
print("""
Le projet Blue Prince est actuellement INCOMPLET.

✅ CE QUI EST IMPLÉMENTÉ:
   - Classes de base pour les objets du jeu
   - Système d'objets (consommables, permanents, interactifs)
   - Système de pièces et leurs effets
   - Catalogue de pièces
   - Interface graphique Pygame (structure)

❌ CE QUI MANQUE:
   - Classe Game (moteur du jeu)
   - Classe Player (gestion du joueur)
   - Classe Inventory (inventaire du joueur)
   - Classe Manor (grille du manoir)
   - Enum GameState
   - Fichiers __init__.py pour les imports

PROCHAINES ÉTAPES:
   1. Créer les classes manquantes (Game, Player, Inventory, Manor)
   2. Ajouter les fichiers __init__.py
   3. Tester les imports
   4. Lancer le jeu
""")
print("=" * 60)
