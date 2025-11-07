"""
Fichier principal pour lancer le jeu Blue Prince
"""
import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game import Game
from ui.game_ui import GameUI


def main():
    """Point d'entrée du programme"""
    print("=== Blue Prince - Version Simplifiee ===")
    print("Chargement du jeu...\n")

    # Créer le jeu
    game = Game()

    # Créer l'interface graphique
    ui = GameUI(game)

    # Lancer le jeu
    print("Jeu lance! Bonne chance!\n")
    ui.run()


if __name__ == "__main__":
    main()