# 🎨 Guide: Règles des couleurs des chambres

## 📋 Définition des rôles par couleur

### 🟡 YELLOW (Jaune) - Magasins
**Rôle**: Magasins où on peut échanger de l'or contre des objets

**Caractéristiques**:
- Contiennent souvent de l'or
- Permettent d'acheter des objets
- Effet: Commerce/Échange

**Exemple dans catalog.py**:
```python
# Commissary (Magasin)
self.available_rooms.append(Room(
    name="Commissary",
    color=RoomColor.YELLOW,
    doors=[Direction.NORTH, Direction.SOUTH],
    gem_cost=1,
    rarity=2,
    objects=[Gold(5)],  # Contient de l'or
    effect=ShopEffect()  # Effet pour acheter des objets
))
```

---

### 🟢 GREEN (Vert) - Jardins
**Rôle**: Jardins d'intérieur avec gemmes, trous à creuser, objets permanents

**Caractéristiques**:
- Contiennent souvent des gemmes
- Ont des endroits où creuser (Shovel)
- Objets permanents (outils, etc.)

**Exemple dans catalog.py**:
```python
# Veranda (Jardin)
self.available_rooms.append(Room(
    name="Veranda",
    color=RoomColor.GREEN,
    doors=[Direction.SOUTH, Direction.NORTH],
    gem_cost=2,
    rarity=2,
    objects=[Gems(2), Shovel(), Apple()],  # Gemmes + outils
    effect=GardenEffect()  # Effet de jardin
))

# Courtyard (Jardin)
self.available_rooms.append(Room(
    name="Courtyard",
    color=RoomColor.GREEN,
    doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST],
    gem_cost=1,
    rarity=1,
    objects=[Gems(1), Shovel()],
    effect=None
))
```

---

### 🟣 PURPLE (Violet) - Chambres
**Rôle**: Chambres avec effets permettant de regagner des pas

**Caractéristiques**:
- Effets de repos/récupération
- Restaurent des pas
- Espaces privés

**Exemple dans catalog.py**:
```python
# Bedroom (Chambre)
self.available_rooms.append(Room(
    name="Bedroom",
    color=RoomColor.PURPLE,
    doors=[Direction.NORTH, Direction.SOUTH],
    gem_cost=1,
    rarity=2,
    objects=[Cake()],  # Nourriture pour récupérer
    effect=RestEffect(steps_restored=5)  # Restaure 5 pas
))
```

---

### 🟠 ORANGE (Orange) - Couloirs
**Rôle**: Couloirs avec beaucoup de portes

**Caractéristiques**:
- Beaucoup de portes (3-4 directions)
- Facilitent la navigation
- Peu ou pas d'objets

**Exemple dans catalog.py**:
```python
# Corridor (Couloir)
self.available_rooms.append(Room(
    name="Corridor",
    color=RoomColor.ORANGE,
    doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST],  # 4 portes!
    gem_cost=0,
    rarity=1,
    objects=[],  # Peu d'objets
    effect=None
))
```

---

### 🔴 RED (Rouge) - Pièces indésirables
**Rôle**: Pièces avec caractéristiques négatives

**Caractéristiques**:
- Peu de portes (difficile de sortir)
- Retirent des pas
- Effets négatifs

**Exemple dans catalog.py**:
```python
# Chapel (Chapelle - indésirable)
self.available_rooms.append(Room(
    name="Chapel",
    color=RoomColor.RED,
    doors=[Direction.SOUTH],  # UNE SEULE porte!
    gem_cost=2,
    rarity=2,
    objects=[],
    effect=NegativeEffect(steps_lost=3)  # Perd 3 pas en entrant
))
```

---

### 🔵 BLUE (Bleu) - Pièces communes
**Rôle**: Pièces les plus communes avec effets variés

**Caractéristiques**:
- Variété d'objets
- Effets divers
- Les plus fréquentes

**Exemples dans catalog.py**:
```python
# Library
self.available_rooms.append(Room(
    name="Library",
    color=RoomColor.BLUE,
    doors=[Direction.WEST, Direction.SOUTH],
    gem_cost=0,
    rarity=1,
    objects=[Keys(1)],
    effect=None
))

# Dining Room
self.available_rooms.append(Room(
    name="Dining Room",
    color=RoomColor.BLUE,
    doors=[Direction.WEST, Direction.EAST, Direction.SOUTH],
    gem_cost=0,
    rarity=1,
    objects=[Apple()],
    effect=None
))
```

---

## 🔧 Comment implémenter ces règles

### 1. Dans `rooms/catalog.py`

Suivez les conventions de couleur lors de la création des chambres:

```python
# ✅ BON: Jardin vert avec gemmes
self.available_rooms.append(Room(
    name="Garden",
    color=RoomColor.GREEN,  # Vert = Jardin
    doors=[Direction.NORTH, Direction.SOUTH],
    gem_cost=1,
    rarity=1,
    objects=[Gems(2), Shovel()],  # Gemmes + outil
))

# ❌ MAUVAIS: Magasin vert (devrait être jaune)
self.available_rooms.append(Room(
    name="Shop",
    color=RoomColor.GREEN,  # ❌ Incohérent!
    objects=[Gold(10)],  # C'est un magasin!
))
```

### 2. Créer des effets spéciaux dans `rooms/effects.py`

```python
# Effet de magasin (jaune)
class ShopEffect(RoomEffect):
    def on_enter(self, player, room):
        print(f"💰 Bienvenue au magasin! Vous pouvez échanger de l'or.")
        # Logique d'achat ici

# Effet de jardin (vert)
class GardenEffect(RoomEffect):
    def on_enter(self, player, room):
        print(f"🌿 Vous entrez dans un jardin paisible.")
        # Peut donner des gemmes bonus

# Effet de repos (violet)
class RestEffect(RoomEffect):
    def __init__(self, steps_restored: int):
        super().__init__("Repos")
        self.steps_restored = steps_restored
    
    def on_enter(self, player, room):
        player.inventory.steps.quantity += self.steps_restored
        print(f"😴 Vous vous reposez. +{self.steps_restored} pas!")

# Effet négatif (rouge)
class NegativeEffect(RoomEffect):
    def __init__(self, steps_lost: int):
        super().__init__("Effet négatif")
        self.steps_lost = steps_lost
    
    def on_enter(self, player, room):
        player.inventory.steps.quantity -= self.steps_lost
        print(f"⚠️ Pièce dangereuse! -{self.steps_lost} pas!")
```

### 3. Appliquer automatiquement les règles

Dans `rooms/room.py`, méthode `enter()`:

```python
def enter(self, player: 'Player') -> None:
    """Appelé quand le joueur entre dans la pièce"""
    self.visited = True
    
    # Appliquer les règles par couleur
    if self.color == RoomColor.YELLOW:
        print("💰 Magasin: Échangez de l'or contre des objets!")
    elif self.color == RoomColor.GREEN:
        print("🌿 Jardin: Cherchez des gemmes et des objets!")
    elif self.color == RoomColor.PURPLE:
        print("😴 Chambre: Lieu de repos.")
    elif self.color == RoomColor.ORANGE:
        print("🚪 Couloir: Beaucoup de portes disponibles.")
    elif self.color == RoomColor.RED:
        print("⚠️ Attention: Pièce indésirable!")
    
    # Appliquer l'effet de la pièce
    if self.effect and hasattr(self.effect, 'on_enter'):
        self.effect.on_enter(player, self)
```

---

## 📊 Résumé des correspondances

| Couleur | Type | Caractéristiques | Objets typiques | Effet typique |
|---------|------|------------------|-----------------|---------------|
| 🟡 YELLOW | Magasin | Échange or/objets | Gold, Keys | ShopEffect |
| 🟢 GREEN | Jardin | Gemmes, creuser | Gems, Shovel | GardenEffect |
| 🟣 PURPLE | Chambre | Repos, récupération | Cake, Apple | RestEffect |
| 🟠 ORANGE | Couloir | 3-4 portes | Peu d'objets | Aucun |
| 🔴 RED | Indésirable | 1 porte, négatif | Peu d'objets | NegativeEffect |
| 🔵 BLUE | Commune | Varié | Varié | Varié |

---

## ✅ Checklist pour créer une nouvelle chambre

1. ☐ Choisir la couleur appropriée selon le type
2. ☐ Ajouter les objets correspondant à la couleur
3. ☐ Définir le nombre de portes approprié
4. ☐ Créer un effet si nécessaire
5. ☐ Tester dans le jeu

---

## 🎯 Exemple complet

```python
# Dans rooms/catalog.py

# 🟡 MAGASIN (Yellow)
self.available_rooms.append(Room(
    name="Gift Shop",
    color=RoomColor.YELLOW,
    doors=[Direction.NORTH, Direction.SOUTH],
    gem_cost=1,
    rarity=2,
    objects=[Gold(10), Keys(2)],
    effect=ShopEffect()
))

# 🟢 JARDIN (Green)
self.available_rooms.append(Room(
    name="Greenhouse",
    color=RoomColor.GREEN,
    doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST],
    gem_cost=2,
    rarity=2,
    objects=[Gems(3), Shovel(), Apple()],
    effect=GardenEffect()
))

# 🟣 CHAMBRE (Purple)
self.available_rooms.append(Room(
    name="Master Bedroom",
    color=RoomColor.PURPLE,
    doors=[Direction.NORTH, Direction.WEST],
    gem_cost=1,
    rarity=2,
    objects=[Cake(), Sandwich()],
    effect=RestEffect(steps_restored=10)
))

# 🟠 COULOIR (Orange)
self.available_rooms.append(Room(
    name="Main Hallway",
    color=RoomColor.ORANGE,
    doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST],
    gem_cost=0,
    rarity=1,
    objects=[],
    effect=None
))

# 🔴 INDÉSIRABLE (Red)
self.available_rooms.append(Room(
    name="Dungeon",
    color=RoomColor.RED,
    doors=[Direction.SOUTH],  # Une seule porte!
    gem_cost=2,
    rarity=3,
    objects=[],
    effect=NegativeEffect(steps_lost=5)
))

# 🔵 COMMUNE (Blue)
self.available_rooms.append(Room(
    name="Study Room",
    color=RoomColor.BLUE,
    doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST],
    gem_cost=0,
    rarity=1,
    objects=[Keys(1), Apple()],
    effect=None
))
```
