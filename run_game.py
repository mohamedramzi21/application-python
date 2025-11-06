#!/usr/bin/env python3
"""
Script de lancement rapide pour Blue Prince
"""
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.game import Game
from ui.game_ui import GameUI


def main():
    """Point d'entrée du programme"""
    print("=" * 60)
    print(" " * 15 + "🏰 BLUE PRINCE 🏰")
    print("=" * 60)
    print("\nChargement du jeu...\n")

    try:
        # Créer le jeu
        game = Game()

        # Créer l'interface graphique
        ui = GameUI(game)

        # Afficher les contrôles
        print("\n📋 CONTRÔLES:")
        print("  Sélection: A/D + ESPACE")
        print("  Déplacement: Flèches ↑↓←→")
        print("  Inventaire: I")
        print("\nLe jeu est prêt! Bonne chance! 🎮\n")

        # Lancer le jeu
        ui.run()

    except KeyboardInterrupt:
        print("\n\nJeu interrompu. À bientôt! 👋")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
