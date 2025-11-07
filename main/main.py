"""
Fichier principal pour lancer le jeu Blue Prince
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game1.game import Game
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