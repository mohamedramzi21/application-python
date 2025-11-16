# 🔨 Système de Coffrets Verrouillés et Marteaux

## ✅ Résumé
Système de **coffrets verrouillés** qui nécessitent un **marteau** pour être ouverts, fonctionnant **exactement comme le Gold avec le Shovel**.

## 🎯 Fonctionnement

### Comme Gold/Shovel :
- ❌ **Sans marteau** : Impossible d'ouvrir, message affiché, possibilité de faire ESC et revenir plus tard
- ✅ **Avec marteau** : Ouverture automatique et récupération de **2-3 objets**
- 🔄 **Marteau réutilisable** : Objet permanent, peut ouvrir plusieurs coffrets

## 🗺️ Localisation

### 🔒 5 Chambres avec Coffrets Verrouillés :
1. **Attic** - Contient : 20 Gold, 1 Gem, 1 Key
2. **Gallery** - Contient : 30 Gold, 2 Gems, 2 Dice
3. **Storeroom** - Contient : 15 Gold, 1 Dice, 1 Cake
4. **Utility Closet** - Contient : 25 Gold, 2 Keys, 1 Gem
5. **Boiler Room** - Contient : 18 Gold, 1 Dice, 1 Key (+ 1 marteau aussi)

### 🔨 3 Chambres avec Marteaux :
1. **The Foundation** (coût: 1 💎)
2. **Workshop** (gratuit)
3. **Boiler Room** (gratuit + coffret)

## 🎮 Comment jouer

1. **Trouvez un marteau** dans Workshop, The Foundation ou Boiler Room
2. **Ramassez-le** avec R (il devient permanent dans votre inventaire)
3. **Trouvez un coffret verrouillé** dans une des 5 chambres
4. **Essayez de l'ouvrir** avec R :
   - ✅ Si vous avez le marteau → ouvre et récupère 2-3 objets
   - ❌ Si pas de marteau → message + possibilité de faire ESC et revenir

## 📦 Contenu des coffrets

Chaque coffret contient **2-3 objets aléatoires** parmi :
- 💰 Gold (10-30 pièces)
- 🔑 Keys (1-2 clés)
- 💎 Gems (1 gemme)
- 🎲 Dice (1 dé)
- 🍰 Cake (gâteau)
- 🥪 Sandwich

## 🔧 Modifications techniques

### Fichiers modifiés :

1. **`items/interactive.py`** - Nouvelle classe `LockedChest`
   ```python
   class LockedChest(InteractiveObject):
       def can_open(self, player):
           # Vérifie si le joueur a un marteau
           if player.inventory.has_permanent_item("Marteau"):
               return True  # Ouvre le coffret
           else:
               return False  # Affiche message, peut revenir
   ```

2. **`rooms/catalog.py`** - 7 chambres modifiées (pas de nouvelles chambres)
   - Attic : +1 coffret
   - Gallery : +1 coffret  
   - Storeroom : +1 coffret
   - Utility Closet : +1 coffret
   - Boiler Room : +1 marteau +1 coffret
   - The Foundation : +1 marteau
   - Workshop : +1 marteau

3. **`game1/game.py`** - Gestion des objets interactifs
   - Détection automatique des objets interactifs
   - Vérification via `can_open()` comme Gold/Shovel
   - Si non ouvert, reste dans la pièce (ESC et revenir)
   - Si ouvert, récupère tous les objets contenus

## 💡 Messages du jeu

### Sans marteau :
```
🔒 Ce coffret est solidement verrouillé. 
   Vous avez besoin d'un marteau pour l'ouvrir.
   Revenez quand vous aurez trouvé un marteau!
```

### Avec marteau :
```
🔨 Vous utilisez le marteau pour briser le coffret verrouillé!
✅ Coffret Verrouillé ouvert!
💰 Gold ramassé! +20 pièces d'or (Total: 60)
💎 Gem ramassée! (Total: 3)
🔑 Key ramassée! (Total: 2)
```

## ✅ Différences avec Gold/Shovel

| Critère | Gold/Shovel | Coffret/Marteau |
|---------|-------------|-----------------|
| Outil requis | Pelle (Shovel) | Marteau (Hammer) |
| Objet à collecter | 1 tas de Gold | 1 Coffret |
| Contenu | 1 objet (Gold) | 2-3 objets variés |
| Comportement sans outil | Message + reste | Message + reste |
| Réutilisable | Oui | Oui |
| Type d'objet | Permanent | Permanent |

## 🎯 Points clés

✅ Exactement le même système que Gold/Shovel  
✅ 5 coffrets dans 5 chambres différentes  
✅ 3 marteaux disponibles  
✅ Coffrets contiennent 2-3 objets (pas 1)  
✅ Possibilité de faire ESC et revenir sans le marteau  
✅ Message clair quand on n'a pas le marteau  
✅ Marteau réutilisable (permanent)  
✅ Aucune nouvelle chambre créée  

Le système est **opérationnel** et testé ! 🎉
