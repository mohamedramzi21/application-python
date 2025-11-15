"""
Script de test pour vérifier le chargement des images
"""
import os
import sys

def test_image_loading():
    """Teste le chargement des images et l'extraction des noms"""
    
    rooms_path = os.path.join("assets", "images", "rooms")
    
    if not os.path.exists(rooms_path):
        print(f"❌ Le dossier {rooms_path} n'existe pas!")
        return
    
    print("=" * 80)
    print("TEST DE CHARGEMENT DES IMAGES")
    print("=" * 80)
    
    # Lister tous les fichiers PNG
    png_files = [f for f in os.listdir(rooms_path) if f.endswith('.png')]
    
    print(f"\n📊 Nombre total d'images PNG: {len(png_files)}")
    print("-" * 80)
    
    # Dictionnaire pour stocker les résultats
    room_images = {}
    
    # Traiter chaque fichier
    for filename in sorted(png_files):
        # Extraire le nom de base de la pièce
        name = filename
        
        # Enlever les préfixes de couleur
        color_prefixes = ['BLUE', 'GREEN', 'RED', 'YELLOW', 'VIOLET', 'ORANGE', 'GREEMYELLOWVIOLET', 'YELLOWVIOLET']
        color_found = None
        for prefix in color_prefixes:
            if name.startswith(prefix):
                color_found = prefix
                name = name[len(prefix):]
                break
        
        # Enlever les suffixes standards
        name = name.replace('_Icon_blue.png', '').replace('_Icon_green.png', '').replace('_Icon_red.png', '').replace('_Icon_yellow.png', '').replace('_Icon.png', '').replace('_Iconblue.png', '')
        
        # Gérer le cas spécial %27 (apostrophe encodée)
        name = name.replace("%27", "'")
        
        # Remplacer underscores par espaces
        name = name.replace('_', ' ')
        
        # Nettoyer les espaces multiples
        name = ' '.join(name.split())
        
        # Stocker le résultat
        room_images[name] = filename
        
        # Afficher avec couleur si trouvée
        if color_found:
            print(f"✓ [{color_found:20s}] {filename:50s} → '{name}'")
        else:
            print(f"✓ [{'NO PREFIX':20s}] {filename:50s} → '{name}'")
    
    print("-" * 80)
    print(f"✅ Total: {len(room_images)} noms de chambres extraits")
    print("=" * 80)
    
    # Afficher la liste des noms extraits
    print("\n📋 LISTE DES NOMS EXTRAITS (pour rooms/catalog.py):")
    print("-" * 80)
    for i, name in enumerate(sorted(room_images.keys()), 1):
        print(f"{i:3d}. {name}")
    
    print("=" * 80)

if __name__ == "__main__":
    test_image_loading()
