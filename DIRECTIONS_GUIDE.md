# 🗺️ Guide des Directions des Chambres

## Comment modifier les directions dans `rooms/catalog.py`

Pour chaque chambre, modifiez la ligne `doors=[...]` avec les directions que vous voulez.

### Directions disponibles:
- `Direction.NORTH` = Nord (↑)
- `Direction.SOUTH` = Sud (↓)
- `Direction.EAST` = Est (→)
- `Direction.WEST` = Ouest (←)

---

## 📋 Liste des 15 chambres avec leurs directions actuelles

### 1. Library (blue)
```python
doors=[Direction.WEST, Direction.SOUTH]
```
- Portes: ← Ouest, ↓ Sud

### 2. Dining Room (blue)
```python
doors=[Direction.NORTH, Direction.SOUTH]
```
- Portes: ↑ Nord, ↓ Sud

### 3. Mail Room (blue)
```python
doors=[Direction.WEST, Direction.SOUTH, Direction.EAST]
```
- Portes: ← Ouest, ↓ Sud, → Est

### 4. Music Room (blue)
```python
doors=[Direction.NORTH, Direction.SOUTH]
```
- Portes: ↑ Nord, ↓ Sud

### 5. Garage (blue)
```python
doors=[Direction.WEST, Direction.SOUTH]
```
- Portes: ← Ouest, ↓ Sud

### 6. Courtyard (blue)
```python
doors=[Direction.SOUTH, Direction.EAST, Direction.WEST]
```
- Portes: ↓ Sud, → Est, ← Ouest

### 7. Observatory (blue)
```python
doors=[Direction.WEST, Direction.SOUTH]
```
- Portes: ← Ouest, ↓ Sud

### 8. Rumpus Room (blue)
```python
doors=[Direction.NORTH, Direction.SOUTH]
```
- Portes: ↑ Nord, ↓ Sud

### 9. Security (blue)
```python
doors=[Direction.NORTH, Direction.SOUTH]
```
- Portes: ↑ Nord, ↓ Sud

### 10. Veranda (green)
```python
doors=[Direction.SOUTH, Direction.EAST, Direction.WEST]
```
- Portes: ↓ Sud, → Est, ← Ouest

### 11. The Pool (blue)
```python
doors=[Direction.SOUTH, Direction.EAST, Direction.WEST]
```
- Portes: ↓ Sud, → Est, ← Ouest

### 12. Commissary (yellow)
```python
doors=[Direction.WEST, Direction.SOUTH]
```
- Portes: ← Ouest, ↓ Sud

### 13. Chapel (purple/red)
```python
doors=[Direction.SOUTH, Direction.EAST, Direction.WEST]
```
- Portes: ↓ Sud, → Est, ← Ouest

### 14. Antechamber (blue) - Point d'arrivée
```python
doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
```
- Portes: ↑ Nord, ↓ Sud, → Est, ← Ouest (toutes les directions)

### 15. Entrance Hall (blue) - Point de départ
```python
doors=[Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
```
- Portes: ↑ Nord, ↓ Sud, → Est, ← Ouest (toutes les directions)

---

## 💡 Conseils

1. **Regardez l'image de chaque chambre** dans `assets/images/rooms/`
2. **Comptez les portes visibles** sur l'image
3. **Modifiez la ligne `doors=[...]`** dans `catalog.py` en fonction des portes que vous voyez
4. **Testez le jeu** pour vérifier que les directions correspondent bien

### Exemple de modification:
Si la chambre "Library" a des portes au Nord et à l'Ouest seulement:
```python
# Avant
doors=[Direction.WEST, Direction.SOUTH]

# Après
doors=[Direction.NORTH, Direction.WEST]
```

---

## ✅ Système de filtrage automatique

Quand vous choisissez une direction (W/A/S/D) dans le jeu, le système propose automatiquement **SEULEMENT** les chambres qui ont une porte dans la direction **OPPOSÉE**.

Exemple:
- Vous êtes dans "Library" et appuyez sur **D** (Est)
- Le jeu propose 3 chambres qui ont toutes une porte **OUEST** (opposé de Est)
- Comme ça, vous pouvez toujours entrer dans la nouvelle chambre!

---

## 🎮 Comment jouer

1. **Lancez le jeu**: `python3 run_game_improved.py`
2. **Choisissez une direction**: W (Nord), A (Ouest), S (Sud), D (Est)
3. **Confirmez avec ESPACE**: Le jeu propose 3 chambres
4. **Choisissez une chambre**: Tapez 1, 2 ou 3
5. **Déplacez-vous**: Utilisez les flèches ↑↓←→

Bon jeu! 🎲
