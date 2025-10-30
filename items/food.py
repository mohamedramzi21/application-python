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