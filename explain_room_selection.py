#!/usr/bin/env python3
"""
Script pour expliquer comment les chambres sont listées et choisies
"""
import random
from game1.game import Game
from core.game_objects import Direction

def main():
    print("=" * 80)
    print("📚 EXPLICATION: Comment les chambres sont listées et choisies")
    print("=" * 80)
    
    # Créer le jeu
    game = Game()
    
    print("\n🏗️  ÉTAPE 1: Liste complète du catalogue")
    print("-" * 80)
    all_rooms = game.catalog.get_all_rooms()
    print(f"Total de chambres dans le catalogue: {len(all_rooms)}")
    for i, room in enumerate(all_rooms, 1):
        doors = ', '.join([d.value for d in room.doors_directions])
        print(f"  {i:2}. {room.name:20} | Portes: {doors}")
    
    print("\n\n🔍 ÉTAPE 2: Filtrage initial")
    print("-" * 80)
    available_rooms = [r for r in all_rooms if r.name not in ["Entrance Hall", "Antechamber"]]
    print(f"Après avoir retiré Entrance Hall et Antechamber: {len(available_rooms)} chambres")
    print("Raison: Ces chambres sont déjà placées sur la grille")
    
    print("\n\n🧭 ÉTAPE 3: Filtrage par direction")
    print("-" * 80)
    
    # Simuler différentes directions
    test_cases = [
        (Direction.NORTH, "SOUTH"),
        (Direction.SOUTH, "NORTH"),
        (Direction.EAST, "WEST"),
        (Direction.WEST, "EAST")
    ]
    
    for selected_dir, opposite_name in test_cases:
        print(f"\n📍 CAS: Je choisis la direction {selected_dir.value.upper()}")
        print(f"   → Les chambres doivent avoir une porte {opposite_name}")
        
        opposite_direction = Direction[opposite_name]
        compatible_rooms = [r for r in available_rooms if opposite_direction in r.doors_directions]
        
        print(f"   ✅ Chambres compatibles trouvées: {len(compatible_rooms)}")
        for room in compatible_rooms[:5]:  # Montrer seulement 5 exemples
            doors = ', '.join([d.value for d in room.doors_directions])
            print(f"      • {room.name:20} | Portes: {doors}")
        if len(compatible_rooms) > 5:
            print(f"      ... et {len(compatible_rooms) - 5} autres")
    
    print("\n\n🎲 ÉTAPE 4: Sélection aléatoire")
    print("-" * 80)
    print("Le jeu utilise la fonction Python: random.sample(compatible_rooms, num_to_select)")
    print("Cette fonction:")
    print("  • Choisit ALÉATOIREMENT parmi les chambres compatibles")
    print("  • Ne choisit JAMAIS la même chambre deux fois")
    print("  • Sélectionne jusqu'à 3 chambres (ou moins si pas assez disponibles)")
    
    print("\n\nExemple avec Direction NORTH (besoin porte SOUTH):")
    game.selected_direction = Direction.NORTH
    
    print("\n  Essai 1:")
    game.generate_room_selection()
    print(f"    → {len(game.pending_room_selection)} chambre(s) proposée(s)")
    
    print("\n  Essai 2 (nouvelle sélection aléatoire):")
    game.generate_room_selection()
    print(f"    → {len(game.pending_room_selection)} chambre(s) proposée(s)")
    
    print("\n  Essai 3 (encore différent):")
    game.generate_room_selection()
    print(f"    → {len(game.pending_room_selection)} chambre(s) proposée(s)")
    
    print("\n\n📍 ÉTAPE 5: Placement sur la grille")
    print("-" * 80)
    print("Le code qui détermine OÙ placer la chambre se trouve dans:")
    print("  game1/game.py → select_room() méthode")
    print("\nLe processus:")
    print("  1. Vous êtes dans une chambre à la position (row, col)")
    print("  2. Vous choisissez une direction (W/A/S/D)")
    print("  3. Le jeu calcule la nouvelle position:")
    print("     • NORTH (W): nouvelle_row = row - 1")
    print("     • SOUTH (S): nouvelle_row = row + 1")
    print("     • EAST  (D): nouvelle_col = col + 1")
    print("     • WEST  (A): nouvelle_col = col - 1")
    print("  4. La chambre choisie est placée à cette nouvelle position")
    
    print("\n\n💡 RÉSUMÉ:")
    print("=" * 80)
    print("1. 📋 Liste: Toutes les chambres du catalogue SAUF Entrance & Antechamber")
    print("2. 🔍 Filtre: Garde seulement les chambres avec la porte opposée nécessaire")
    print("3. 🎲 Choix: Sélection ALÉATOIRE de 1 à 3 chambres compatibles")
    print("4. 📍 Position: Placée dans la direction choisie, adjacente à votre position")
    print("5. 🔄 Répète: À chaque fois que vous appuyez sur W/A/S/D + ESPACE")
    print("=" * 80)
    
    print("\n\n🎮 CODE CLÉS:")
    print("-" * 80)
    print("📁 Fichier: game1/game.py")
    print("   • Ligne 65-115: generate_room_selection() - Sélection des chambres")
    print("   • Ligne 38:     random.sample() - Choix aléatoire")
    print("   • Ligne 117-150: select_room() - Placement sur la grille")
    print("\n📁 Fichier: rooms/catalog.py")
    print("   • Ligne 27-180: _initialize_rooms() - Définition de toutes les chambres")
    print("   • Ligne 380:    get_all_rooms() - Retourne la liste complète")

if __name__ == "__main__":
    main()
