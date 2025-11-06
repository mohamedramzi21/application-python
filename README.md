# Blue Prince - Jeu d'exploration de manoir 🏰

Adaptation Python du jeu de société Blue Prince, un jeu d'exploration de manoir avec gestion de ressources.

## 🎮 Comment jouer

### Installation

```bash
# Installer les dépendances
pip3 install pygame

# Lancer le jeu
python3 main/main.py
```

### Contrôles

#### Sélection de Pièce
- **A / D** : Naviguer entre les 3 pièces proposées
- **ESPACE** : Valider le choix de pièce
- **R** : Redraw (utilise un dé pour obtenir 3 nouvelles pièces)

#### En Jeu (Exploration)
- **↑ ↓ ← →** (Flèches) : Se déplacer dans les pièces adjacentes
- **1-9** : Interagir avec les objets dans la pièce
- **I** : Afficher l'inventaire (console)

### Objectif

Explorer le manoir en plaçant des pièces et en vous déplaçant jusqu'à atteindre l'Antechamber (sortie) avant de manquer de pas!

## 📊 Ressources

- **👣 Pas** : 70 au départ. Chaque déplacement coûte 1 pas
- **💎 Gemmes** : 2 au départ. Pour acheter des pièces spéciales
- **💰 Or** : 0 au départ. Monnaie du jeu
- **🔑 Clés** : 0 au départ. Pour ouvrir portes et coffres
- **🎲 Dés** : 0 au départ. Pour relancer le choix de pièces

## 🏠 Types de Pièces

- **🔵 BLEUES** (Communes) : Vault, Library, Den...
- **🟢 VERTES** (Jardins) : Garden, Greenhouse, Veranda...
- **🟣 VIOLETTES** (Chambres) : Bedroom, Chapel...
- **🟠 ORANGES** (Couloirs) : Hallway, Corridor...
- **🟡 JAUNES** (Magasins) : Shop, Market...
- **🔴 ROUGES** (Indésirables) : Trap Room, Dark Room...

## 🎯 Version Actuelle

**Version de Test 0.1** - Fonctionnalités de base implémentées :
- ✅ Sélection de pièces
- ✅ Déplacement entre les pièces
- ✅ Système d'inventaire
- ✅ Portes verrouillées
- ✅ 15 images de pièces
- ✅ 5 images d'objets
- ✅ Interface graphique Pygame

**À venir** :
- Effets spéciaux des pièces
- Plus d'objets interactifs
- Sons et musique
- Sauvegarde/Chargement

## 📁 Structure du Projet

```
application-python/
├── assets/          # Images et ressources
│   └── images/
│       ├── rooms/   # 15 images de pièces
│       └── items/   # 5 images d'objets
├── core/            # Classes de base
├── game/            # Logique du jeu
│   ├── game.py      # Moteur principal
│   ├── player.py    # Joueur
│   ├── inventory.py # Inventaire
│   └── manor.py     # Grille du manoir
├── items/           # Objets du jeu
├── rooms/           # Pièces et effets
├── ui/              # Interface Pygame
└── main/            # Point d'entrée
```

## 🛠️ Développement

Créé avec :
- Python 3.9+
- Pygame 2.6+

## 📝 Licence

Projet étudiant - Sorbonne Université - MASTER ISI
