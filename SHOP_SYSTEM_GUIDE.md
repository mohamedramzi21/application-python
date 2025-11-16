# 🛒 SYSTÈME DE MAGASIN - Guide Complet

## Vue d'ensemble

Les chambres **YELLOW (jaunes)** sont maintenant des **magasins** où le joueur peut dépenser des pièces d'or pour acheter des objets spéciaux.

## Fonctionnement

### 1. Entrer dans un magasin

Quand le joueur entre dans une chambre YELLOW avec un objet à vendre :
- Un message s'affiche dans le terminal : "💰 Vous entrez dans un magasin."
- L'objet disponible et son prix sont affichés
- Le nombre de pièces d'or du joueur est indiqué
- Un rappel apparaît : "⌨️ Appuyez sur G pour acheter"

### 2. Affichage dans l'interface

Dans le **panneau blanc d'information** (Current Room Panel), le jeu affiche :
- 🛒 Le nom de l'objet disponible
- 💰 Le prix en pièces d'or
- 💡 "Appuyez sur G pour acheter"

### 3. Acheter un objet

Pour acheter, le joueur doit :
1. **Appuyer sur la touche G**
2. Le jeu vérifie :
   - ✓ Le joueur a assez d'or ?
   - ✓ L'objet n'a pas déjà été acheté ?
3. Si les conditions sont remplies :
   - L'or est déduit
   - L'objet est ajouté à l'inventaire
   - Message de confirmation : "✅ Vous avez acheté: [objet] pour [prix] pièces!"
   - Le magasin est marqué comme "acheté"

### 4. Protection contre les achats multiples

- Chaque magasin ne permet qu'**un seul achat**
- Si le joueur essaie d'acheter à nouveau : "❌ Vous avez déjà acheté l'objet de ce magasin!"
- Le message change en : "✓ Objet déjà acheté"

## Liste des Magasins et Objets

| Magasin | Objet | Prix | Description |
|---------|-------|------|-------------|
| **Commissary** | Pelle (Shovel) | 10 pièces | Permet de creuser dans les jardins |
| **Bookshop** | Kit de crochetage | 15 pièces | Ouvre les portes verrouillées (niveau 1) |
| **Kitchen** | 5 pièces d'or | 8 pièces | Investissement rentable ! |
| **Laundry Room** | 3 clés | 12 pièces | Pour ouvrir les portes |
| **Locksmith** | 5 clés | 20 pièces | Pack premium de clés |
| **Mount Holly Gift Shop** | 2 gemmes | 18 pièces | Gemmes pour choisir des pièces rares |
| **Showroom** | 3 dés | 15 pièces | Pour retirer des pièces |
| **The Armory** | 20 pas | 25 pièces | Prolonge l'exploration |

## Messages d'erreur

- **"❌ Pas assez d'or!"** : Le joueur n'a pas suffisamment de pièces
- **"❌ Vous n'êtes pas dans un magasin!"** : Touche G pressée hors d'une chambre YELLOW
- **"❌ Vous avez déjà acheté l'objet de ce magasin!"** : Achat déjà effectué
- **"❌ Pas d'objet disponible dans ce magasin."** : Magasin vide (cas rare)

## Stratégie

### Objets prioritaires
1. **Pelle (10 pièces)** : Essentiel pour collecter des gemmes dans les jardins
2. **Clés (12-20 pièces)** : Nécessaires pour ouvrir les portes verrouillées
3. **Pas (25 pièces)** : Quand l'exploration devient difficile

### Quand acheter
- **Début du jeu** : Pelle + quelques clés
- **Milieu du jeu** : Kit de crochetage si vous avez beaucoup de portes verrouillées
- **Fin du jeu** : Pas supplémentaires pour atteindre l'Antechamber

## Code Technique

### Structure d'un shop_item

```python
shop_item = {
    'item': Shovel,  # Classe ou lambda: lambda: Keys(3)
    'name': 'Pelle (Shovel)',  # Nom affiché
    'price': 10  # Prix en pièces d'or
}
```

### Exemple d'ajout dans catalog.py

```python
Room(
    name="Commissary",
    color=RoomColor.YELLOW,
    doors=[Direction.WEST, Direction.SOUTH],
    gem_cost=1,
    rarity=1,
    objects=[Apple(), Banana()],
    shop_item={'item': Shovel, 'name': 'Pelle (Shovel)', 'price': 10}
)
```

### Méthode d'achat (room.py)

```python
def buy_shop_item(self, player: 'Player') -> bool:
    # Vérifications (magasin, objet disponible, pas déjà acheté, assez d'or)
    # Déduction de l'or
    # Ajout de l'objet à l'inventaire
    # Marquage du magasin comme "acheté"
    return True
```

## Contrôles

- **G** : Acheter l'objet du magasin
- **I** : Voir l'inventaire (vérifier l'or et les objets)

## Notes de développement

### Fichiers modifiés

1. **rooms/room.py**
   - Ajout attribut `shop_item` et `shop_purchased`
   - Méthode `buy_shop_item(player)`
   - Modification de `enter()` pour afficher les infos magasin

2. **rooms/catalog.py**
   - Ajout de `shop_item` à chaque chambre YELLOW

3. **ui/game_ui_new.py**
   - Ajout de l'import `RoomColor`
   - Gestion de la touche G dans `handle_playing_events()`
   - Affichage des infos magasin dans `draw_current_room_panel()`

4. **game1/inventory.py**
   - Correction de `add_item()` pour gérer les noms français (Clés, Dés, etc.)

### Tests

Exécuter `test_shop_system.py` pour tester :
- Achat réussi
- Achat avec or insuffisant
- Tentative d'achat multiple
- Ajout correct des objets à l'inventaire

## Améliorations futures possibles

- [ ] Prix variables selon la rareté de la pièce
- [ ] Réductions si le joueur a un certain objet permanent
- [ ] Magasins avec plusieurs objets (menu de sélection)
- [ ] Objets aléatoires dans certains magasins
- [ ] Système de troc (échanger gemmes contre or)
