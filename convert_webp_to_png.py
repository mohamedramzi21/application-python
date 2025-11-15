"""
Script pour convertir les images WebP en PNG
"""
import os
from PIL import Image

def convert_webp_to_png():
    """Convertit toutes les images .webp en .png dans assets/images/rooms"""
    rooms_path = os.path.join("assets", "images", "rooms")
    
    if not os.path.exists(rooms_path):
        print(f"❌ Le dossier {rooms_path} n'existe pas!")
        return
    
    webp_files = [f for f in os.listdir(rooms_path) if f.endswith('.webp')]
    
    if not webp_files:
        print("✅ Aucun fichier .webp trouvé - tous les fichiers sont déjà en PNG!")
        return
    
    print(f"📊 Nombre de fichiers .webp trouvés: {len(webp_files)}")
    print("-" * 80)
    
    converted = 0
    errors = 0
    
    for filename in webp_files:
        webp_path = os.path.join(rooms_path, filename)
        png_filename = filename.replace('.webp', '.png')
        png_path = os.path.join(rooms_path, png_filename)
        
        # Vérifier si le PNG existe déjà
        if os.path.exists(png_path):
            print(f"⏭️  {filename} → PNG existe déjà, suppression du WebP...")
            try:
                os.remove(webp_path)
                print(f"   ✓ WebP supprimé")
            except Exception as e:
                print(f"   ✗ Erreur suppression: {e}")
            continue
        
        try:
            # Ouvrir l'image WebP
            img = Image.open(webp_path)
            
            # Convertir en RGB si nécessaire (pour enlever la transparence)
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Sauvegarder en PNG
            img.save(png_path, 'PNG')
            print(f"✅ {filename} → {png_filename}")
            
            # Supprimer le fichier WebP
            os.remove(webp_path)
            converted += 1
            
        except Exception as e:
            print(f"❌ Erreur avec {filename}: {e}")
            errors += 1
    
    print("-" * 80)
    print(f"✅ Fichiers convertis: {converted}/{len(webp_files)}")
    if errors > 0:
        print(f"❌ Erreurs: {errors}")
    print("\n🎉 Conversion terminée!")

if __name__ == "__main__":
    convert_webp_to_png()
