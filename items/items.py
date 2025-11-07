"""
Implémentation des objets consommables, permanents et nourriture
"""
import sys
import os
from abc import ABC

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.game_objects import ConsumableItem, PermanentItem, Food, InteractiveObject
import random


# ============ OBJETS CONSOMMABLES ============

class Steps(ConsumableItem):
    """Pas du joueur"""

    def __init__(self, quantity: int = 70):
        super().__init__("Pas", quantity)


class Gold(ConsumableItem):
    """Pièces d'or"""

    def __init__(self, quantity: int = 0):
        super().__init__("Or", quantity)


class Gems(ConsumableItem):
    """Gemmes"""

    def __init__(self, quantity: int = 2):
        super().__init__("Gemmes", quantity)


class Keys(ConsumableItem):
    """Clés"""

    def __init__(self, quantity: int = 0):
        super().__init__("Clés", quantity)


class Dice(ConsumableItem):
    """Dés pour retirer des pièces"""

    def __init__(self, quantity: int = 0):
        super().__init__("Dés", quantity)


# ============ OBJETS PERMANENTS ============

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


# ============ NOURRITURE ============

class Apple(Food):
    """Pomme - restaure 2 pas"""

    def __init__(self):
        super().__init__("Pomme", 2)


class Banana(Food):
    """Banane - restaure 3 pas"""

    def __init__(self):
        super().__init__("Banane", 3)


class Cake(Food):
    """Gâteau - restaure 10 pas"""

    def __init__(self):
        super().__init__("Gâteau", 10)


class Sandwich(Food):
    """Sandwich - restaure 15 pas"""

    def __init__(self):
        super().__init__("Sandwich", 15)


class Meal(Food):
    """Repas - restaure 25 pas"""

    def __init__(self):
        super().__init__("Repas", 25)


# ============ OBJETS INTERACTIFS ============

class Chest(InteractiveObject,ABC):
    """Coffre contenant des objets"""

    def __init__(self):
        # Génère un contenu aléatoire pour le coffre
        contents = self._generate_contents()
        super().__init__("Coffre", contents)

    def _generate_contents(self) -> list:
        """Génère un contenu aléatoire pour le coffre"""
        possible_contents = [
            Gold(random.randint(5, 20)),
            Keys(random.randint(1, 2)),
            Gems(1),
            Dice(1),
            Apple(),
            Banana()
        ]
        # Choisit 1-3 objets aléatoires
        num_items = random.randint(1, 3)
        return random.sample(possible_contents, num_items)

    def can_open(self, player: 'Player') -> bool:
        """Peut ouvrir avec une clé ou un marteau"""
        has_hammer = player.inventory.has_permanent_item("Marteau")
        has_key = player.inventory.keys.quantity > 0

        if has_hammer:
            print("Vous utilisez le marteau pour ouvrir le coffre.")
            return True
        elif has_key:
            player.inventory.keys.consume(1)
            print("Vous utilisez une clé pour ouvrir le coffre.")
            return True
        else:
            print("Vous avez besoin d'une clé ou d'un marteau pour ouvrir ce coffre.")
            return False


class DigSpot(InteractiveObject, ABC):
    """Endroit où creuser"""

    def __init__(self):
        contents = self._generate_contents()
        super().__init__("Endroit où creuser", contents)

    def _generate_contents(self) -> list:
        """Génère un contenu aléatoire pour le trou"""
        if random.random() < 0.3:  # 30% de chance de ne rien trouver
            return []

        possible_contents = [
            Gold(random.randint(3, 15)),
            Keys(1),
            Gems(1),
            Apple(),
            Banana()
        ]
        num_items = random.randint(1, 2)
        return random.sample(possible_contents, num_items)

    def can_open(self, player: 'Player') -> bool:
        """Nécessite une pelle"""
        if player.inventory.has_permanent_item("Pelle"):
            print("Vous utilisez la pelle pour creuser.")
            return True
        else:
            print("Vous avez besoin d'une pelle pour creuser ici.")
            return False


class Locker(InteractiveObject):
    """Casier dans le vestiaire"""

    def __init__(self):
        contents = self._generate_contents()
        super().__init__("Casier", contents)

    def _generate_contents(self) -> list:
        """Génère un contenu aléatoire pour le casier"""
        if random.random() < 0.2:  # 20% de chance de ne rien trouver
            return []

        possible_contents = [
            Gold(random.randint(5, 25)),
            Keys(1),
            Gems(1),
            Dice(1),
            Cake(),
            Sandwich()
        ]
        num_items = random.randint(1, 2)
        return random.sample(possible_contents, num_items)

    def can_open(self, player: 'Player') -> bool:
        """Nécessite toujours une clé"""
        if player.inventory.keys.quantity > 0:
            player.inventory.keys.consume(1)
            print("Vous utilisez une clé pour ouvrir le casier.")
            return True
        else:
            print("Vous avez besoin d'une clé pour ouvrir ce casier.")
            return False