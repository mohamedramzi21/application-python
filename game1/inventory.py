"""
Classe Inventory - Gestion de l'inventaire du joueur
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from items.consumables import Steps, Gold, Gems, Keys, Dice
from items.permanent import PermanentItem


class Inventory:
    """Gestion de l'inventaire du joueur"""

    def __init__(self):
        # Ressources consommables (selon la capture d'écran)
        self.steps = Steps(70)  # 70 pas au départ
        self.gold = Gold(0)     # 0 or au départ
        self.gems = Gems(2)     # 2 gemmes au départ
        self.keys = Keys(0)     # 0 clés au départ
        self.dice = Dice(0)     # 0 dés au départ

        # Objets permanents
        self.permanent_items = []

        # Nourriture
        self.food_items = []

        def spend_gold(self, amount: int) -> bool:
            if self.gold >= amount:
                self.gold -= amount
                return True
            print("Pas assez d’or !")
            return False

    def add_item(self, item):
        """Ajoute un objet consommable à l'inventaire"""
        if hasattr(item, 'quantity'):
            # C'est un objet consommable
            if item.name == "Steps":
                self.steps.quantity += item.quantity
            elif item.name == "Gold":
                self.gold.quantity += item.quantity
            elif item.name == "Gems":
                self.gems.quantity += item.quantity
            elif item.name == "Keys":
                self.keys.quantity += item.quantity
            elif item.name == "Dice":
                self.dice.quantity += item.quantity
            return True
        return False

    def add_permanent_item(self, item: PermanentItem):
        """Ajoute un objet permanent à l'inventaire"""
        if item not in self.permanent_items:
            self.permanent_items.append(item)
            print(f"✓ Objet permanent ajouté: {item.name}")
            return True
        return False

    def has_permanent_item(self, item_name: str) -> bool:
        """Vérifie si le joueur possède un objet permanent"""
        return any(item.name == item_name for item in self.permanent_items)

    def spend_key(self) -> bool:
        """Utilise une clé"""
        if self.keys.quantity > 0:
            self.keys.quantity -= 1
            return True
        return False

    def spend_gems(self, amount: int) -> bool:
        """Dépense des gemmes"""
        if self.gems.quantity >= amount:
            self.gems.quantity -= amount
            return True
        return False

    def spend_dice(self) -> bool:
        """Utilise un dé"""
        if self.dice.quantity > 0:
            self.dice.quantity -= 1
            return True
        return False

    def use_steps(self, amount: int = 1) -> bool:
        """Utilise des pas (pour se déplacer)"""
        if self.steps.quantity >= amount:
            self.steps.quantity -= amount
            return True
        return False

    def __str__(self):
        """Affichage de l'inventaire"""
        result = "\n=== INVENTAIRE ===\n"
        result += f"👣 Pas: {self.steps.quantity}\n"
        result += f"💰 Or: {self.gold.quantity}\n"
        result += f"💎 Gemmes: {self.gems.quantity}\n"
        result += f"🔑 Clés: {self.keys.quantity}\n"
        result += f"🎲 Dés: {self.dice.quantity}\n"

        if self.permanent_items:
            result += "\n🛠️  Objets permanents:\n"
            for item in self.permanent_items:
                result += f"  • {item.name}\n"

        if self.food_items:
            result += "\n🍎 Nourriture:\n"
            for item in self.food_items:
                result += f"  • {item.name}\n"

        return result
