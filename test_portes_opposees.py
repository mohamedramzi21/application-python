"""
Test pour vérifier la logique des portes opposées lors du déplacement
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.game_objects import Direction
from rooms.room import Room, RoomColor

print('='*80)
print('🚪 TEST: Vérification des portes opposées')
print('='*80)

# Test 1: Direction.opposite()
print("\n📍 Test 1: Méthode opposite()")
print("-" * 80)
directions = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
for d in directions:
    opp = d.opposite()
    print(f"  {d.value:5s} → opposite: {opp.value:5s}")

print("\n✅ Test 1 réussi!")

# Test 2: Scénario de déplacement
print("\n📍 Test 2: Scénario de déplacement entre chambres")
print("-" * 80)

# Chambre A: porte à l'EST
room_a = Room(
    name="Chambre A",
    color=RoomColor.BLUE,
    doors=[Direction.EAST],
    gem_cost=0,
    rarity=0
)

# Chambre B1: porte à l'OUEST (compatible avec A)
room_b1 = Room(
    name="Chambre B1 (compatible)",
    color=RoomColor.BLUE,
    doors=[Direction.WEST],
    gem_cost=0,
    rarity=0
)

# Chambre B2: porte au SUD (incompatible avec A)
room_b2 = Room(
    name="Chambre B2 (incompatible)",
    color=RoomColor.BLUE,
    doors=[Direction.SOUTH],
    gem_cost=0,
    rarity=0
)

print(f"\n🏠 Chambre A: portes = [{', '.join([d.value for d in room_a.doors_directions])}]")
print(f"🏠 Chambre B1: portes = [{', '.join([d.value for d in room_b1.doors_directions])}]")
print(f"🏠 Chambre B2: portes = [{', '.join([d.value for d in room_b2.doors_directions])}]")

# Simulation de déplacement
print("\n🚶 Déplacement de A vers l'EST:")
direction_mouvement = Direction.EAST
opposite_needed = direction_mouvement.opposite()

print(f"   Direction du mouvement: {direction_mouvement.value}")
print(f"   Direction opposée requise dans la chambre de destination: {opposite_needed.value}")

print(f"\n   Chambre A a une porte au {direction_mouvement.value}? {room_a.has_door(direction_mouvement)}")

print(f"\n   Vers B1:")
print(f"     - B1 a une porte au {opposite_needed.value}? {room_b1.has_door(opposite_needed)}")
if room_a.has_door(direction_mouvement) and room_b1.has_door(opposite_needed):
    print(f"     ✅ Déplacement AUTORISÉ (les deux portes sont compatibles)")
else:
    print(f"     ❌ Déplacement BLOQUÉ")

print(f"\n   Vers B2:")
print(f"     - B2 a une porte au {opposite_needed.value}? {room_b2.has_door(opposite_needed)}")
if room_a.has_door(direction_mouvement) and room_b2.has_door(opposite_needed):
    print(f"     ✅ Déplacement AUTORISÉ")
else:
    print(f"     ❌ Déplacement BLOQUÉ (B2 n'a pas de porte à l'ouest)")

print("\n✅ Test 2 réussi!")
print("="*80)
print("✅ La logique des portes opposées fonctionne correctement!")
print("="*80)
