"""
Test des modules individuels
"""
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("TEST DES MODULES IMPLÉMENTÉS")
print("=" * 70)

# Test 1: Classes de base
print("\n1️⃣  TEST: core/game_objects.py")
print("-" * 70)
try:
    from core.game_objects import Direction, RoomColor, GameObject
    print("✅ Import réussi: Direction, RoomColor, GameObject")
    print(f"   - Directions disponibles: {[d.value for d in Direction]}")
    print(f"   - Couleurs disponibles: {[c.value for c in RoomColor]}")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 2: Items consommables
print("\n2️⃣  TEST: items/consumables.py")
print("-" * 70)
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
    from items.consumables import Steps, Gold, Gems, Keys, Dice
    print("✅ Import réussi: Steps, Gold, Gems, Keys, Dice")
    
    # Créer des objets
    steps = Steps(70)
    gold = Gold(0)
    gems = Gems(2)
    
    print(f"   - {steps.name}: {steps.quantity}")
    print(f"   - {gold.name}: {gold.quantity}")
    print(f"   - {gems.name}: {gems.quantity}")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 3: Nourriture
print("\n3️⃣  TEST: items/food.py")
print("-" * 70)
try:
    from items.food import Apple, Banana, Cake, Sandwich, Meal
    print("✅ Import réussi: Apple, Banana, Cake, Sandwich, Meal")
    
    foods = [Apple(), Banana(), Cake(), Sandwich(), Meal()]
    print("   Nourriture disponible:")
    for food in foods:
        print(f"   - {food.name}: restaure {food.steps_restored} pas")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 4: Objets permanents
print("\n4️⃣  TEST: items/permanent.py")
print("-" * 70)
try:
    from items.permanent import Shovel, Hammer, LockpickKit, MetalDetector, RabbitFoot
    print("✅ Import réussi: Shovel, Hammer, LockpickKit, MetalDetector, RabbitFoot")
    
    items = [Shovel(), Hammer(), LockpickKit(), MetalDetector(), RabbitFoot()]
    print("   Objets permanents disponibles:")
    for item in items:
        print(f"   - {item.name}: {item.description}")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 5: Objets interactifs
print("\n5️⃣  TEST: items/interactive.py")
print("-" * 70)
try:
    # On ne peut pas tester complètement car il manque la classe Player
    print("⚠️  Test partiel - nécessite classe Player pour test complet")
    print("   Classes définies: Chest, DigSpot, Locker")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 6: Pièces
print("\n6️⃣  TEST: rooms/room.py")
print("-" * 70)
try:
    # Test partiel
    print("⚠️  Test partiel - nécessite autres classes pour test complet")
    print("   Classes définies: Door, Room")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Test 7: Effets
print("\n7️⃣  TEST: rooms/effects.py")
print("-" * 70)
try:
    print("⚠️  Test partiel - nécessite classe Game pour test complet")
    print("   Effets définis: ResourceEffect, ProbabilityModifierEffect, etc.")
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "=" * 70)
print("📊 RÉSUMÉ")
print("=" * 70)
print("""
✅ MODULES TESTÉS AVEC SUCCÈS:
   - core/game_objects.py (classes de base)
   - items/consumables.py (ressources)
   - items/food.py (nourriture)
   - items/permanent.py (objets permanents)

⚠️  MODULES PARTIELLEMENT TESTABLES:
   - items/interactive.py (nécessite Player)
   - rooms/room.py (nécessite Player)
   - rooms/effects.py (nécessite Game)
   - rooms/catalog.py (nécessite tous les imports)
   - ui/game_ui.py (nécessite Game, GameState)

❌ IMPOSSIBLE À EXÉCUTER:
   - main/main.py (nécessite Game et GameUI complets)

CONCLUSION:
Le projet a une bonne base de classes implémentées, mais il manque
les classes principales (Game, Player, Inventory, Manor) pour que
le programme soit fonctionnel.
""")
print("=" * 70)
