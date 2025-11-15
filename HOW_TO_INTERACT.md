# 🎮 GUIDE: Comment ramasser des objets dans les chambres

## 📝 Instructions pas à pas

### 1️⃣ Entrer dans une chambre avec objets

Quand vous entrez dans une chambre qui contient des objets (comme la **Veranda**), vous verrez:

```
🎁 4 items available
Press E to interact
```

### 2️⃣ Activer le mode "Walk-in Closet"

**Appuyez sur la touche E** pour entrer en mode interaction.

L'écran affichera:
- **Walk-in Closet** (titre)
- Liste des objets disponibles:
  - Take gem
  - Take key
  - Take dice
  - Take cake

### 3️⃣ Naviguer dans la liste

Utilisez les **flèches ↑ et ↓** pour naviguer:
- **↑** : Objet précédent (vers le haut)
- **↓** : Objet suivant (vers le bas)

L'objet sélectionné sera **surligné en bleu**.

### 4️⃣ Ramasser un objet

Appuyez sur **R** (pour "Ramasser" ou "Take") pour prendre l'objet sélectionné.

L'objet sera:
- ✅ Ajouté à votre inventaire
- ✅ Retiré de la liste
- ✅ Les quantités à droite seront mises à jour

### 5️⃣ Sortir du mode interaction

**Option 1**: Appuyez sur **ESC** pour sortir sans ramasser plus d'objets

**Option 2**: Ramassez tous les objets → Sortie automatique

---

## 🎯 Résumé des touches

| Touche | Action |
|--------|--------|
| **E** | Entrer en mode "Walk-in Closet" |
| **↑** | Objet précédent |
| **↓** | Objet suivant |
| **R** | Ramasser l'objet sélectionné |
| **ESC** | Sortir du mode interaction |

---

## 🏠 Chambres avec objets

Pour le moment, seule la **Veranda** contient des objets:
- 💎 Gem (+1 gemme)
- 🔑 Key (+1 clé)
- 🎲 Dice (+1 dé)
- 🍰 Cake (+10 pas)

---

## ⚠️ Note importante

**Vous DEVEZ appuyer sur E** quand vous êtes dans une chambre pour voir les objets!

Le jeu ne les affiche pas automatiquement - vous devez **activer le mode interaction** avec la touche E.

---

## 🔧 Ajouter des objets à d'autres chambres

Pour ajouter des objets à d'autres chambres, modifiez `rooms/catalog.py`:

```python
self.available_rooms.append(Room(
    name="Nom de la Chambre",
    color=RoomColor.BLUE,
    doors=[Direction.NORTH, Direction.SOUTH],
    gem_cost=0,
    rarity=1,
    objects=[Gems(1), Keys(1), Cake()]  # ← Ajoutez vos objets ici
))
```

Objets disponibles:
- `Cake()` → +10 pas
- `Apple()` → +2 pas
- `Gems(1)` → +1 gemme
- `Keys(1)` → +1 clé
- `Dice(1)` → +1 dé
- `Gold(5)` → +5 or
