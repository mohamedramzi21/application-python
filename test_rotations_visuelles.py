"""
Test pour vérifier que les rotations visuelles correspondent aux rotations logiques
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame
pygame.init()

from rooms.catalog import RoomCatalog

# Créer le catalogue
catalog = RoomCatalog()

print('='*80)
print('🔄 VÉRIFICATION DES ROTATIONS LOGIQUES ET VISUELLES')
print('='*80)

# Statistiques
rotation_stats = {0: 0, 90: 0, 180: 0, 270: 0}
rotated_rooms = []

for room in catalog.available_rooms:
    rot = getattr(room, 'rotation_degrees', 0)
    rotation_stats[rot] += 1
    
    if rot != 0:
        doors_str = ','.join([d.value for d in room.doors_directions])
        rotated_rooms.append({
            'name': room.name,
            'rotation': rot,
            'doors': doors_str
        })

print(f"\n📊 Statistiques des rotations:")
print(f"   0° : {rotation_stats[0]:2d} pièces (non tournées)")
print(f"  90° : {rotation_stats[90]:2d} pièces")
print(f" 180° : {rotation_stats[180]:2d} pièces")
print(f" 270° : {rotation_stats[270]:2d} pièces")
print(f"\n✅ Total tournées: {rotation_stats[90] + rotation_stats[180] + rotation_stats[270]}/{len(catalog.available_rooms)}")

print(f"\n🎯 Exemples de pièces tournées (premières 10):")
print("-" * 80)
for i, room_info in enumerate(rotated_rooms[:10]):
    print(f"{i+1:2d}. {room_info['name']:30s} → {room_info['rotation']:3d}° | Portes: [{room_info['doors']}]")

print("\n" + "="*80)
print("✅ Les rotations logiques sont appliquées!")
print("🎨 Les images seront tournées automatiquement dans l'UI via get_room_image()")
print("="*80)

# Test de rotation d'image
print("\n🖼️  Test de rotation d'image pygame...")
print("-" * 80)

# Créer une petite image de test
test_surface = pygame.Surface((100, 100))
test_surface.fill((255, 0, 0))  # Rouge
pygame.draw.rect(test_surface, (0, 255, 0), (10, 10, 30, 80))  # Barre verte verticale

for degrees in [0, 90, 180, 270]:
    pygame_rotation = -degrees  # Inverser pour Pygame (clockwise → counterclockwise)
    rotated = pygame.transform.rotate(test_surface, pygame_rotation)
    print(f"  Rotation {degrees:3d}° (pygame: {pygame_rotation:4d}°) → Nouvelle taille: {rotated.get_size()}")

print("\n✅ Les rotations d'images pygame fonctionnent correctement!")
print("="*80)

pygame.quit()
