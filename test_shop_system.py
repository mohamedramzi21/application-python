"""
Test du système de magasin
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rooms.room import Room
from rooms.catalog import RoomCatalog
from game1.player import Player
from game1.inventory import Inventory
from core.game_objects import RoomColor, Direction
from items.permanent import Shovel
from items.consumables import Keys

def test_shop_system():
    """Test le système de magasin"""
    print("=== TEST DU SYSTÈME DE MAGASIN ===\n")
    
    # Créer un joueur
    player = Player()
    player.inventory.gold.quantity = 50  # Donner 50 pièces d'or
    
    print(f"💰 Or initial: {player.inventory.gold.quantity}")
    print(f"🔑 Clés initiales: {player.inventory.keys.quantity}")
    
    # Créer une chambre magasin
    shop_room = Room(
        name="Test Shop",
        color=RoomColor.YELLOW,
        doors=[Direction.NORTH, Direction.SOUTH],
        shop_item={'item': lambda: Keys(3), 'name': '3 clés', 'price': 12}
    )
    
    print(f"\n🛒 Magasin: {shop_room.name}")
    print(f"   Article: {shop_room.shop_item['name']}")
    print(f"   Prix: {shop_room.shop_item['price']} pièces")
    
    # Simuler l'entrée du joueur
    print("\n📍 Le joueur entre dans le magasin...")
    shop_room.enter(player)
    
    # Tenter un achat
    print("\n💳 Tentative d'achat...")
    success = shop_room.buy_shop_item(player)
    
    if success:
        print("\n✅ ACHAT RÉUSSI!")
        print(f"💰 Or restant: {player.inventory.gold.quantity}")
        print(f"🔑 Clés après achat: {player.inventory.keys.quantity}")
    
    # Tenter un deuxième achat (devrait échouer)
    print("\n💳 Tentative d'un 2ème achat...")
    success2 = shop_room.buy_shop_item(player)
    
    if not success2:
        print("❌ Deuxième achat échoué comme prévu (objet déjà acheté)")
    
    # Test avec pas assez d'or
    print("\n\n=== TEST AVEC PAS ASSEZ D'OR ===\n")
    poor_player = Player()
    poor_player.inventory.gold.quantity = 5  # Seulement 5 pièces
    
    shop_room2 = Room(
        name="Expensive Shop",
        color=RoomColor.YELLOW,
        doors=[Direction.NORTH],
        shop_item={'item': Shovel, 'name': 'Pelle', 'price': 10}
    )
    
    print(f"💰 Or du joueur pauvre: {poor_player.inventory.gold.quantity}")
    print(f"🛒 Prix de l'objet: {shop_room2.shop_item['price']}")
    
    print("\n💳 Tentative d'achat...")
    success3 = shop_room2.buy_shop_item(poor_player)
    
    if not success3:
        print("❌ Achat échoué comme prévu (pas assez d'or)")
    
    print("\n=== TEST TERMINÉ ===")

if __name__ == "__main__":
    test_shop_system()
