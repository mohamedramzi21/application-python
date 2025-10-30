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
