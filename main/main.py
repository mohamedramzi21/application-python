"""
Fichier principal pour lancer le jeu Blue Prince
"""
from game import Game
from game_ui import GameUI


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