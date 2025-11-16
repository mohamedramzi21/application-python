"""
Test rapide : Vérifier qu'une chambre YELLOW a bien un shop_item
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rooms.catalog import RoomCatalog
from core.game_objects import RoomColor

catalog = RoomCatalog()

print("=== CHAMBRES YELLOW AVEC MAGASIN ===\n")

yellow_rooms = [r for r in catalog.available_rooms if r.color == RoomColor.YELLOW]

print(f"Nombre de chambres YELLOW: {len(yellow_rooms)}\n")

for room in yellow_rooms:
    has_shop = hasattr(room, 'shop_item') and room.shop_item is not None
    print(f"📍 {room.name}")
    print(f"   shop_item: {has_shop}")
    if has_shop:
        print(f"   - Article: {room.shop_item.get('name', 'N/A')}")
        print(f"   - Prix: {room.shop_item.get('price', 'N/A')} pièces")
    print()
