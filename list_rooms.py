#!/usr/bin/env python3
"""
Script pour afficher toutes les chambres du catalogue avec leurs portes
"""
from rooms.catalog import RoomCatalog

def main():
    catalog = RoomCatalog()
    rooms = catalog.get_all_rooms()
    
    print("=" * 70)
    print("📋 LISTE DES CHAMBRES DU CATALOGUE")
    print("=" * 70)
    print(f"\nTotal: {len(rooms)} chambres\n")
    
    for i, room in enumerate(rooms, 1):
        # Symboles de direction
        directions = []
        for d in room.doors_directions:
            if d.value == "north":
                directions.append("↑ Nord")
            elif d.value == "south":
                directions.append("↓ Sud")
            elif d.value == "east":
                directions.append("→ Est")
            elif d.value == "west":
                directions.append("← Ouest")
        
        doors_str = ", ".join(directions)
        cost = f"💎 {room.gem_cost}" if room.gem_cost > 0 else "Gratuit"
        
        print(f"{i:2}. {room.name:20} | {cost:12} | Portes: {doors_str}")
    
    print("\n" + "=" * 70)
    print("\n✅ Les 15 chambres attendues:")
    expected = [
        "Library", "Dining Room", "Mail Room", "Music Room", "Garage",
        "Courtyard", "Observatory", "Rumpus Room", "Security", "Veranda",
        "The Pool", "Commissary", "Chapel", "Antechamber", "Entrance Hall"
    ]
    
    room_names = [r.name for r in rooms]
    missing = []
    for name in expected:
        if name in room_names:
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} - MANQUANTE!")
            missing.append(name)
    
    # Note spéciale pour Entrance Hall
    if "Entrance Hall" in missing:
        print("\n  ℹ️  Note: Entrance Hall est créée automatiquement par get_entrance()")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
