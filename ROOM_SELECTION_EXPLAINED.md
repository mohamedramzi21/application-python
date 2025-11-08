# 🎮 Comment les Chambres sont Listées et Choisies

## 📊 Vue d'ensemble du processus

```
┌─────────────────────────────────────────────────────────────────┐
│                    CATALOGUE COMPLET                             │
│  15 chambres au total (définies dans rooms/catalog.py)         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FILTRAGE INITIAL                               │
│  Retire: Entrance Hall & Antechamber (déjà placées)            │
│  Résultat: 13 chambres disponibles                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              FILTRAGE PAR DIRECTION OPPOSÉE                      │
│  Si direction = NORTH → garde chambres avec porte SOUTH         │
│  Si direction = SOUTH → garde chambres avec porte NORTH         │
│  Si direction = EAST  → garde chambres avec porte WEST          │
│  Si direction = WEST  → garde chambres avec porte EAST          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 SÉLECTION ALÉATOIRE                              │
│  random.sample(chambres_compatibles, min(3, nombre_dispo))     │
│  Résultat: 1, 2 ou 3 chambres proposées                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              CHOIX DU JOUEUR (1, 2 ou 3)                        │
│  Le joueur sélectionne une chambre parmi les proposées         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              PLACEMENT SUR LA GRILLE                             │
│  Position = position_actuelle + décalage_direction             │
│  • NORTH: row - 1                                               │
│  • SOUTH: row + 1                                               │
│  • EAST:  col + 1                                               │
│  • WEST:  col - 1                                               │
└─────────────────────────────────────────────────────────────────┘
```

## 🎲 Est-ce ALÉATOIRE?

**OUI!** ✅ La sélection est **totalement aléatoire**

### Fonction utilisée:
```python
random.sample(compatible_rooms, num_to_select)
```

### Ce que cela signifie:
- À chaque fois que vous appuyez sur **ESPACE**, de nouvelles chambres sont choisies
- **Même direction** → **Chambres différentes** à chaque fois
- Les chambres sont **mélangées aléatoirement**
- Aucun pattern prévisible

### Exemple avec Direction NORTH:
```
Essai 1: Garage, Commissary, Courtyard
Essai 2: Observatory, Library, Chapel
Essai 3: Library, Rumpus Room, Music Room
```
→ Toutes différentes!

## 📍 OÙ sont placées les chambres?

### Position de départ:
- **Entrance Hall**: Position (9, 2) - Dernière ligne, colonne 3
- **Antechamber**: Position (0, 2) - Première ligne, colonne 3

### Grille du manoir:
```
Largeur:  5 colonnes (0 à 4)
Hauteur: 10 lignes    (0 à 9)

     Col: 0    1    2    3    4
Row 0:   [ ]  [ ]  [A]  [ ]  [ ]    ← Antechamber (Objectif)
Row 1:   [ ]  [ ]  [ ]  [ ]  [ ]
Row 2:   [ ]  [ ]  [ ]  [ ]  [ ]
Row 3:   [ ]  [ ]  [ ]  [ ]  [ ]
Row 4:   [ ]  [ ]  [ ]  [ ]  [ ]
Row 5:   [ ]  [ ]  [ ]  [ ]  [ ]
Row 6:   [ ]  [ ]  [ ]  [ ]  [ ]
Row 7:   [ ]  [ ]  [ ]  [ ]  [ ]
Row 8:   [ ]  [ ]  [ ]  [ ]  [ ]
Row 9:   [ ]  [ ]  [E]  [ ]  [ ]    ← Entrance Hall (Départ)
```

### Calcul de la nouvelle position:
```python
# Code dans game1/game.py - Méthode get_adjacent_position()

if direction == Direction.NORTH:
    new_row = current_row - 1  # Monte d'une ligne
    new_col = current_col       # Même colonne

elif direction == Direction.SOUTH:
    new_row = current_row + 1  # Descend d'une ligne
    new_col = current_col       # Même colonne

elif direction == Direction.EAST:
    new_row = current_row       # Même ligne
    new_col = current_col + 1  # Colonne suivante

elif direction == Direction.WEST:
    new_row = current_row       # Même ligne
    new_col = current_col - 1  # Colonne précédente
```

### Exemple:
```
Vous êtes à (9, 2) - Entrance Hall
Vous choisissez NORTH (W)
Nouvelle position = (9-1, 2) = (8, 2)
La chambre sera placée en (8, 2)
```

## 🔍 Dans quel fichier/zone?

### 📁 **game1/game.py**
```python
# LIGNE 65-115: Sélection des chambres
def generate_room_selection(self):
    # 1. Obtenir toutes les chambres
    all_rooms = self.catalog.get_all_rooms()
    
    # 2. Filtrer
    available_rooms = [r for r in all_rooms 
                      if r.name not in ["Entrance Hall", "Antechamber"]]
    
    # 3. Filtrer par direction opposée
    compatible_rooms = [r for r in available_rooms 
                       if opposite_direction in r.doors_directions]
    
    # 4. Choisir aléatoirement
    self.pending_room_selection = random.sample(compatible_rooms, 
                                                 min(3, len(compatible_rooms)))

# LIGNE 117-150: Placement de la chambre
def select_room(self, index: int) -> bool:
    selected_room = self.pending_room_selection[index]
    
    # Calculer position
    new_pos = self.manor.get_adjacent_position(
        self.player.position, 
        self.selected_direction
    )
    
    # Placer la chambre
    self.manor.place_room(selected_room, *new_pos)
    
    # Déplacer le joueur
    self.player.position = new_pos
```

### 📁 **game1/manor.py**
```python
# Calcul des positions adjacentes
def get_adjacent_position(self, position, direction):
    row, col = position
    
    if direction == Direction.NORTH:
        return (row - 1, col)
    elif direction == Direction.SOUTH:
        return (row + 1, col)
    # etc...
```

### 📁 **rooms/catalog.py**
```python
# LIGNE 27-180: Définition de toutes les chambres
def _initialize_rooms(self):
    self.available_rooms.append(Room(
        name="Library",
        doors=[Direction.WEST, Direction.SOUTH],
        ...
    ))
    # ... 14 autres chambres
```

## 📊 Statistiques des Portes

D'après le test:
- **Chambres avec porte NORTH**: 2 (Rumpus Room, Veranda)
- **Chambres avec porte SOUTH**: 13 (presque toutes!)
- **Chambres avec porte EAST**: 5
- **Chambres avec porte WEST**: 10

→ Si vous allez vers le SOUTH, seulement **2 chambres** seront proposées!

## 🎯 Résumé Final

1. **Liste**: `catalog.get_all_rooms()` retourne toutes les chambres
2. **Filtre**: Retire Entrance & Antechamber + garde celles avec porte opposée
3. **Aléatoire**: `random.sample()` choisit 1-3 chambres
4. **Position**: Adjacente à votre position selon la direction choisie
5. **Zone**: Code dans `game1/game.py` lignes 65-150

**C'est totalement aléatoire et dynamique!** 🎲✨
