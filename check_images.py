"""
Vérifie que toutes les chambres du catalogue ont une image correspondante
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rooms.catalog import RoomCatalog

def check_images_for_rooms():
    """Vérifie que chaque chambre a une image"""
    
    # Charger le catalogue
    catalog = RoomCatalog()
    
    # Lister les images disponibles
    rooms_path = os.path.join("assets", "images", "rooms")
    room_images = {}
    
    if os.path.exists(rooms_path):
        for filename in os.listdir(rooms_path):
            if filename.endswith('.png'):
                name = filename
                
                # Enlever les préfixes de couleur
                color_prefixes = ['GREEMYELLOWVIOLET', 'YELLOWVIOLET', 'BLUE', 'GREEN', 'RED', 'YELLOW', 'VIOLET', 'ORANGE']
                for prefix in color_prefixes:
                    if name.startswith(prefix):
                        name = name[len(prefix):]
                        break
                
                # Enlever les suffixes
                name = name.replace('_Icon_blue.png', '').replace('_Icon_green.png', '').replace('_Icon_red.png', '').replace('_Icon_yellow.png', '').replace('_Icon.png', '').replace('_Iconblue.png', '')
                name = name.replace("%27", "'")
                name = name.replace('_', ' ')
                name = ' '.join(name.split())
                
                room_images[name] = filename
    
    print("=" * 80)
    print("VÉRIFICATION DES IMAGES POUR CHAQUE CHAMBRE")
    print("=" * 80)
    
    # Vérifier chaque chambre
    missing = []
    found = []
    
    for room in catalog.available_rooms:
        if room.name in room_images:
            found.append(room.name)
            print(f"✅ {room.name:30s} → {room_images[room.name]}")
        else:
            missing.append(room.name)
            print(f"❌ {room.name:30s} → IMAGE MANQUANTE!")
    
    print("=" * 80)
    print(f"✅ Chambres avec image: {len(found)}/{catalog.get_room_count()}")
    
    if missing:
        print(f"❌ Chambres sans image: {len(missing)}")
        print("\nListe des chambres sans image:")
        for name in missing:
            print(f"   • {name}")
    else:
        print("🎉 Toutes les chambres ont une image!")
    
    print("=" * 80)

if __name__ == "__main__":
    check_images_for_rooms()
