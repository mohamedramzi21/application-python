#!/usr/bin/env python3
"""
Lancement du jeu avec la nouvelle UI améliorée
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game1.game import Game
from ui.game_ui_new import ImprovedGameUI


def main():
    print("=" * 60)
    print(" " * 15 + "🏰 BLUE PRINCE 🏰")
    print("=" * 60)
    print("\nChargement du jeu avec images...\n")

    try:
        # Créer le jeu
        game = Game()

        # Créer l'interface améliorée
        ui = ImprovedGameUI(game)

        print("\n📋 CONTRÔLES:")
        print("  SÉLECTION DE PIÈCE:")
        print("    ← → : Naviguer entre les pièces")
        print("    ESPACE : Valider le choix")
        print("    R : Redraw (avec dé)")
        print("\n  EN JEU:")
        print("    W : Se déplacer/ouvrir porte NORD")
        print("    S : Se déplacer/ouvrir porte SUD")
        print("    A : Se déplacer/ouvrir porte OUEST")
        print("    D : Se déplacer/ouvrir porte EST")
        print("    I : Inventaire")
        print("\nLe jeu est prêt! 🎮\n")

        # Lancer
        ui.run()

    except KeyboardInterrupt:
        print("\n\nJeu interrompu. À bientôt! 👋")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
