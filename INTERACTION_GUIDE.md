# 🎮 Guide d'Interaction avec les Objets

## Vue d'ensemble
Le système d'interaction permet au joueur d'entrer dans une chambre et de ramasser des objets disponibles (nourriture, clés, gemmes, dés).

## Comment ça marche?

### 1️⃣ Entrer en mode interaction
- **Touche `E`**: Depuis n'importe quelle chambre, appuyez sur `E` pour entrer en mode "Walk-in Closet"
- Si la chambre contient des objets, l'interface d'interaction s'affiche
- Si la chambre est vide, un message vous informe qu'il n'y a rien à ramasser

### 2️⃣ Navigation dans les objets
Une fois en mode interaction, vous voyez:
- **Le titre**: "Walk-in Closet"
- **La liste des objets disponibles**:
  - `Take cake` - Restaure 10 pas
  - `Take gem` - +1 gemme
  - `Take key` - +1 clé
  - `Take dice` - +1 dé

**Navigation**:
- **Flèche ↑**: Sélectionner l'objet précédent
- **Flèche ↓**: Sélectionner l'objet suivant
- L'objet sélectionné est **surligné en bleu**

### 3️⃣ Ramasser un objet
- **Touche `R`** (pour "Ramasser"): Prend l'objet sélectionné
- L'objet est ajouté à votre inventaire
- L'objet disparaît de la liste
- Le compteur correspondant augmente (pas, gemmes, clés, dés)

### 4️⃣ Sortir du mode interaction
- **Touche `ESC`**: Quitte le mode interaction sans ramasser
- **Automatique**: Si vous ramassez tous les objets, vous revenez en mode jeu normal

## Chambres avec objets

### Veranda (configurée actuellement)
La **Veranda** contient:
- 🍰 **1 Cake** → +10 pas
- 💎 **1 Gem** → +1 gemme
- 🔑 **1 Key** → +1 clé
- 🎲 **1 Dice** → +1 dé

## Exemple de session

```
1. Vous êtes dans la Veranda
2. Appuyez sur E → Mode interaction activé
3. Liste affichée:
   - Take gem   (bleu = sélectionné)
   - Take key
   - Take dice
   - Take cake

4. Appuyez sur ↓ → "Take key" devient bleu
5. Appuyez sur R → Clé ramassée! (Total clés: 1)

6. Liste mise à jour:
   - Take gem   (bleu = sélectionné)
   - Take dice
   - Take cake

7. Continuez à naviguer et ramasser...
8. Quand tout est pris → Retour automatique en mode jeu
```

## États du jeu

### GameState.PLAYING (Mode normal)
- Se déplacer avec les flèches
- Choisir une direction avec W/A/S/D
- **Appuyer sur E pour entrer en mode interaction**

### GameState.ROOM_INTERACTION (Mode interaction)
- Naviguer avec ↑/↓
- Ramasser avec R
- Sortir avec ESC

## Objets et effets

| Objet | Nom affiché | Effet | Icône |
|-------|-------------|-------|-------|
| Cake | Take cake | +10 pas | 🍰 |
| Gems | Take gem | +1 gemme | 💎 |
| Keys | Take key | +1 clé | 🔑 |
| Dice | Take dice | +1 dé | 🎲 |

## Pour ajouter des objets à d'autres chambres

Dans `rooms/catalog.py`, modifiez la définition de la chambre:

```python
self.available_rooms.append(Room(
    name="Nom de la Chambre",
    color=RoomColor.BLUE,
    doors=[Direction.NORTH, Direction.SOUTH],
    gem_cost=0,
    rarity=1,
    objects=[Cake(), Gems(2), Keys(1)]  # ← Ajoutez les objets ici
))
```

**Objets disponibles**:
- `Cake()` - 10 pas
- `Apple()` - 2 pas
- `Banana()` - 3 pas
- `Sandwich()` - 15 pas
- `Gems(quantité)` - Gemmes
- `Keys(quantité)` - Clés
- `Dice(quantité)` - Dés
- `Gold(quantité)` - Or

## Récapitulatif des touches

| Touche | Mode | Action |
|--------|------|--------|
| E | PLAYING | Entrer en mode interaction |
| ↑ | ROOM_INTERACTION | Objet précédent |
| ↓ | ROOM_INTERACTION | Objet suivant |
| R | ROOM_INTERACTION | Ramasser l'objet sélectionné |
| ESC | ROOM_INTERACTION | Sortir sans ramasser |

---

🎯 **Note**: Seule la Veranda est configurée avec des objets pour le moment. Vous pouvez ajouter des objets à n'importe quelle chambre en modifiant `rooms/catalog.py`.
