"""
Objets permanents du jeu
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game_objects import PermanentItem
from items.permanent import PermanentItem

class Shovel(PermanentItem):
    """Pelle pour creuser"""

    def __init__(self):
        super().__init__("Pelle", "Permet de creuser pour trouver des objets")

    def apply_effect(self, context: dict) -> None:
        """La pelle permet de creuser les DigSpot"""
        context['can_dig'] = True


class Hammer(PermanentItem):
    """Marteau pour ouvrir les coffres"""

    def __init__(self):
        super().__init__("Marteau", "Permet d'ouvrir les coffres sans clé")

    def apply_effect(self, context: dict) -> None:
        """Le marteau permet d'ouvrir les coffres sans clé"""
        context['can_break_chests'] = True


class LockpickKit(PermanentItem):
    """Kit de crochetage pour ouvrir les portes niveau 1"""

    def __init__(self):
        super().__init__("Kit de crochetage", "Permet d'ouvrir les portes verrouillées sans clé")

    def apply_effect(self, context: dict) -> None:
        """Permet d'ouvrir les portes de niveau 1 sans clé"""
        context['can_lockpick'] = True


class MetalDetector(PermanentItem):
    """Détecteur de métaux"""

    def __init__(self):
        super().__init__("Détecteur de métaux", "Augmente les chances de trouver clés et or")

    def apply_effect(self, context: dict) -> None:
        """Augmente la probabilité de trouver des clés et de l'or"""
        context['metal_detection_bonus'] = context.get('metal_detection_bonus', 0) + 0.3


class RabbitFoot(PermanentItem):
    """Patte de lapin"""

    def __init__(self):
        super().__init__("Patte de lapin", "Augmente les chances de trouver des objets")

    def apply_effect(self, context: dict) -> None:
        """Augmente la probabilité de trouver tous types d'objets"""
        context['luck_bonus'] = context.get('luck_bonus', 0) + 0.2