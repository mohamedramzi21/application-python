"""
Interface graphique améliorée avec images - Conforme aux captures d'écran
"""
import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, Dict
from game1.game import Game, GameState
from core.game_objects import Direction

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (40, 40, 40)
BLUE = (100, 180, 255)
GREEN = (100, 255, 150)
RED = (255, 100, 100)
YELLOW = (255, 240, 100)
PURPLE = (200, 120, 255)
ORANGE = (255, 180, 50)

# Mapping des couleurs
ROOM_COLORS = {
    'blue': BLUE,
    'green': GREEN,
    'red': RED,
    'yellow': YELLOW,
    'purple': PURPLE,
    'orange': ORANGE
}


class ImprovedGameUI:
    """Interface graphique améliorée avec images"""

    def __init__(self, game: Game):
        pygame.init()

        self.game = game
        self.screen_width = 1400
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Blue Prince")

        # Polices
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        # Zone de la grille (à gauche, fond noir)
        self.grid_x = 10
        self.grid_y = 100
        self.cell_size = 60
        self.grid_width = self.game.manor.width * self.cell_size
        self.grid_height = self.game.manor.height * self.cell_size

        # Zone d'information (à droite, fond blanc)
        self.info_x = self.grid_x + self.grid_width + 50
        self.info_y = 50
        self.info_width = self.screen_width - self.info_x - 20
        self.info_height = self.screen_height - 100

        # Sélection
        self.selected_room_index = 0
        self.selected_direction = None  # Pour choisir la direction avec AWSD

        # Cache d'images
        self.room_images: Dict[str, pygame.Surface] = {}
        self.item_images: Dict[str, pygame.Surface] = {}
        self.color_to_image: Dict[str, pygame.Surface] = {}  # Mapping couleur -> image
        self._load_images()

        # FPS
        self.clock = pygame.time.Clock()
        self.fps = 60

    def _load_images(self):
        """Charge toutes les images"""
        assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "images")
        
        # Charger images de pièces
        rooms_path = os.path.join(assets_path, "rooms")
        if os.path.exists(rooms_path):
            for filename in os.listdir(rooms_path):
                if filename.endswith('.png'):
                    # Extraire le nom de base de la pièce
                    # "Entrance_Hall_Icon_blue.png" -> "Entrance Hall"
                    name = filename.replace('_Icon_blue.png', '').replace('_Icon_green.png', '').replace('_Icon_red.png', '').replace('_Icon_yellow.png', '').replace('_Icon.png', '').replace('_Iconblue.png', '').replace('_', ' ')
                    filepath = os.path.join(rooms_path, filename)
                    try:
                        image = pygame.image.load(filepath)
                        # Sauvegarder avec le nom de la pièce (avec espaces)
                        self.room_images[name] = image
                        
                        # Créer mapping couleur -> image (prendre la première de chaque couleur)
                        if 'blue' in filename.lower() and 'blue' not in self.color_to_image:
                            self.color_to_image['blue'] = image
                        elif 'green' in filename.lower() and 'green' not in self.color_to_image:
                            self.color_to_image['green'] = image
                        elif 'red' in filename.lower() and 'red' not in self.color_to_image:
                            self.color_to_image['red'] = image
                        elif 'yellow' in filename.lower() and 'yellow' not in self.color_to_image:
                            self.color_to_image['yellow'] = image
                            self.color_to_image['orange'] = image  # Orange utilise yellow
                        
                        print(f"✓ Image chargée: {filename} -> '{name}'")
                    except Exception as e:
                        print(f"✗ Erreur chargement {filename}: {e}")

        # Charger images d'items
        items_path = os.path.join(assets_path, "items")
        if os.path.exists(items_path):
            for filename in os.listdir(items_path):
                if filename.endswith('.png'):
                    name = filename.replace('.png', '')
                    filepath = os.path.join(items_path, filename)
                    try:
                        image = pygame.image.load(filepath)
                        self.item_images[name] = image
                        print(f"✓ Item chargé: {name}")
                    except Exception as e:
                        print(f"✗ Erreur chargement {filename}: {e}")

    def run(self):
        """Boucle principale"""
        running = True

        while running:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.game.state == GameState.PLAYING:
                    self.handle_playing_events(event)
                elif self.game.state == GameState.ROOM_SELECTION:
                    self.handle_room_selection_events(event)
                elif self.game.is_game_over():
                    self.handle_game_over_events(event)

            # Affichage
            self.screen.fill(BLACK)

            if self.game.state == GameState.PLAYING:
                self.draw_playing_state()
            elif self.game.state == GameState.ROOM_SELECTION:
                self.draw_room_selection_state()
            elif self.game.is_game_over():
                self.draw_game_over_state()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def handle_playing_events(self, event):
        """En mode jeu: AWSD pour choisir direction, Flèches pour se déplacer"""
        if event.type == pygame.KEYDOWN:
            # Récupérer la chambre actuelle pour vérifier les portes
            current_room = self.game.manor.get_room(*self.game.player.position)
            if not current_room:
                return

            # W/A/S/D pour SÉLECTIONNER UNE DIRECTION (vérifier d'abord s'il y a une porte)
            if event.key == pygame.K_w:  # W = Nord
                if current_room.has_door(Direction.NORTH):
                    self.selected_direction = Direction.NORTH
                    print("🧭 Direction sélectionnée: NORD")
                else:
                    print(f"❌ Pas de porte au NORD dans {current_room.name}")
            elif event.key == pygame.K_s:  # S = Sud
                if current_room.has_door(Direction.SOUTH):
                    self.selected_direction = Direction.SOUTH
                    print("🧭 Direction sélectionnée: SUD")
                else:
                    print(f"❌ Pas de porte au SUD dans {current_room.name}")
            elif event.key == pygame.K_d:  # D = Est
                if current_room.has_door(Direction.EAST):
                    self.selected_direction = Direction.EAST
                    print("🧭 Direction sélectionnée: EST")
                else:
                    print(f"❌ Pas de porte à l'EST dans {current_room.name}")
            elif event.key == pygame.K_a:  # A = Ouest
                if current_room.has_door(Direction.WEST):
                    self.selected_direction = Direction.WEST
                    print("🧭 Direction sélectionnée: OUEST")
                else:
                    print(f"❌ Pas de porte à l'OUEST dans {current_room.name}")
            
            # ESPACE pour CONFIRMER la direction et proposer des pièces
            elif event.key == pygame.K_SPACE and self.selected_direction:
                # Vérifier s'il y a déjà une pièce dans cette direction
                next_pos = self.game.manor.get_adjacent_position(self.game.player.position, self.selected_direction)
                if next_pos and self.game.manor.get_room(*next_pos) is None:
                    # Pas de pièce → Proposer 3 nouvelles pièces pour cette direction
                    print(f"🚪 Direction {self.selected_direction.value} confirmée!")
                    self.game.selected_direction = self.selected_direction  # Stocker la direction dans Game
                    self.game.generate_room_selection()
                    self.selected_direction = None  # Réinitialiser pour l'UI
                elif next_pos is None:
                    print(f"❌ Hors des limites du manoir!")
                    self.selected_direction = None
                else:
                    print(f"⚠️ Il y a déjà une pièce dans cette direction!")
                    self.selected_direction = None

            # FLÈCHES pour SE DÉPLACER entre pièces adjacentes existantes (vérifier les portes)
            elif event.key == pygame.K_UP:  # ↑ = Se déplacer Nord
                if current_room.has_door(Direction.NORTH):
                    self.game.try_move(Direction.NORTH)
                    self.selected_direction = None  # Réinitialiser la direction après déplacement
                else:
                    print(f"❌ Pas de porte au NORD dans {current_room.name}")
            elif event.key == pygame.K_DOWN:  # ↓ = Se déplacer Sud
                if current_room.has_door(Direction.SOUTH):
                    self.game.try_move(Direction.SOUTH)
                    self.selected_direction = None  # Réinitialiser la direction après déplacement
                else:
                    print(f"❌ Pas de porte au SUD dans {current_room.name}")
            elif event.key == pygame.K_RIGHT:  # → = Se déplacer Est
                if current_room.has_door(Direction.EAST):
                    self.game.try_move(Direction.EAST)
                    self.selected_direction = None  # Réinitialiser la direction après déplacement
                else:
                    print(f"❌ Pas de porte à l'EST dans {current_room.name}")
            elif event.key == pygame.K_LEFT:  # ← = Se déplacer Ouest
                if current_room.has_door(Direction.WEST):
                    self.game.try_move(Direction.WEST)
                    self.selected_direction = None  # Réinitialiser la direction après déplacement
                else:
                    print(f"❌ Pas de porte à l'OUEST dans {current_room.name}")

            # I pour inventaire
            elif event.key == pygame.K_i:
                print(self.game.player.inventory)

    def handle_room_selection_events(self, event):
        """En mode sélection: Flèches + ESPACE"""
        if event.type == pygame.KEYDOWN:
            # Flèches pour naviguer entre les pièces
            if event.key == pygame.K_LEFT:
                self.selected_room_index = (self.selected_room_index - 1) % len(self.game.pending_room_selection)
            elif event.key == pygame.K_RIGHT:
                self.selected_room_index = (self.selected_room_index + 1) % len(self.game.pending_room_selection)

            # ESPACE pour valider
            elif event.key == pygame.K_SPACE:
                if self.game.select_room(self.selected_room_index):
                    self.selected_room_index = 0
                    self.selected_direction = None

            # R pour redraw avec dés
            elif event.key == pygame.K_r:
                if self.game.reroll_rooms():
                    self.selected_room_index = 0

    def handle_game_over_events(self, event):
        """Game over"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game = Game()
                self.selected_room_index = 0

    def draw_playing_state(self):
        """Mode exploration - comme capture d'écran 2"""
        # Zone gauche (noire) - Grille du manoir
        self.draw_manor_grid()
        
        # Afficher l'indicateur de direction sélectionnée (barre blanche)
        if self.selected_direction:
            self.draw_direction_indicator()

        # Zone droite (blanche) - Inventaire et info
        pygame.draw.rect(self.screen, WHITE, (self.info_x, self.info_y, self.info_width, self.info_height))
        
        # Inventaire
        self.draw_inventory_panel()
        
        # Info pièce actuelle
        self.draw_current_room_panel()

        # Instructions
        y = self.screen_height - 60
        inst = self.font_small.render("AWSD: Choose direction | SPACE: Confirm | Arrows: Move", True, WHITE)
        self.screen.blit(inst, (self.screen_width // 2 - inst.get_width() // 2, y))

    def draw_room_selection_state(self):
        """Mode sélection - comme capture d'écran 1 et 3"""
        # Zone gauche (noire) - Grille
        self.draw_manor_grid()

        # Zone droite (blanche)
        pygame.draw.rect(self.screen, WHITE, (self.info_x, self.info_y, self.info_width, self.info_height))
        
        # Inventaire en haut
        self.draw_inventory_panel()

        # Titre "Choose a room to draft"
        y_offset = 300
        title = self.font_large.render("Choose a room to draft", True, BLACK)
        self.screen.blit(title, (self.info_x + 50, y_offset))

        # "Redraw" à droite
        redraw_text = self.font_medium.render("Redraw", True, BLACK)
        self.screen.blit(redraw_text, (self.info_x + self.info_width - 150, y_offset))
        dice_text = self.font_small.render(f"with dice", True, GRAY)
        self.screen.blit(dice_text, (self.info_x + self.info_width - 150, y_offset + 40))

        # Afficher les 3 pièces avec images
        y_offset += 100
        room_size = 150
        spacing = 50
        start_x = self.info_x + 50

        for i, room in enumerate(self.game.pending_room_selection):
            x = start_x + i * (room_size + spacing)

            # Chercher l'image: 1) nom exact, 2) mapping par couleur, 3) n'importe quelle image
            img = None
            if room.name in self.room_images:
                # Nom exact trouvé
                img = self.room_images[room.name]
            elif hasattr(self, 'color_to_image') and room.color.value in self.color_to_image:
                # Utiliser le mapping couleur
                img = self.color_to_image[room.color.value]
            elif len(self.room_images) > 0:
                # Prendre la première image disponible
                img = list(self.room_images.values())[i % len(self.room_images)]
            
            if img:
                # Afficher l'image
                img_scaled = pygame.transform.scale(img, (room_size, room_size))
                self.screen.blit(img_scaled, (x, y_offset))
            else:
                # Fallback final: rectangle coloré
                color = ROOM_COLORS.get(room.color.value, GRAY)
                pygame.draw.rect(self.screen, color, (x, y_offset, room_size, room_size))

            # Bordure si sélectionné
            if i == self.selected_room_index:
                pygame.draw.rect(self.screen, YELLOW, (x - 3, y_offset - 3, room_size + 6, room_size + 6), 4)

            # Nom de la pièce
            name_surf = self.font_medium.render(room.name, True, BLACK)
            name_rect = name_surf.get_rect(center=(x + room_size // 2, y_offset + room_size + 30))
            self.screen.blit(name_surf, name_rect)

            # Coût en gemmes
            if room.gem_cost > 0:
                # Icône diamant
                if 'Gem' in self.item_images:
                    gem_img = pygame.transform.scale(self.item_images['Gem'], (24, 24))
                    self.screen.blit(gem_img, (x + room_size // 2 - 12, y_offset + room_size + 55))
                
                cost_color = RED if not self.game.player.can_afford_room(room.gem_cost) else BLACK
                cost_surf = self.font_small.render(str(room.gem_cost), True, cost_color)
                self.screen.blit(cost_surf, (x + room_size // 2 + 15, y_offset + room_size + 55))

        # Instructions
        y = self.screen_height - 60
        inst = self.font_small.render("← → : Select | SPACE: Confirm | R: Redraw", True, WHITE)
        self.screen.blit(inst, (self.screen_width // 2 - inst.get_width() // 2, y))

    def draw_manor_grid(self):
        """Dessine la grille du manoir avec images"""
        for row in range(self.game.manor.height):
            for col in range(self.game.manor.width):
                x = self.grid_x + col * self.cell_size
                y = self.grid_y + row * self.cell_size

                room = self.game.manor.get_room(row, col)

                if room:
                    # Chercher l'image: 1) nom exact, 2) mapping par couleur, 3) n'importe quelle image
                    img = None
                    if room.name in self.room_images:
                        # Nom exact trouvé
                        img = self.room_images[room.name]
                    elif hasattr(self, 'color_to_image') and room.color.value in self.color_to_image:
                        # Utiliser le mapping couleur
                        img = self.color_to_image[room.color.value]
                    elif len(self.room_images) > 0:
                        # Prendre une image au hasard
                        img = list(self.room_images.values())[0]
                    
                    if img:
                        # Afficher l'image
                        img_scaled = pygame.transform.scale(img, (self.cell_size, self.cell_size))
                        self.screen.blit(img_scaled, (x, y))
                    else:
                        # Fallback final: couleur
                        color = ROOM_COLORS.get(room.color.value, GRAY)
                        pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

                    # Bordure pour position du joueur
                    if (row, col) == self.game.player.position:
                        pygame.draw.rect(self.screen, YELLOW, (x, y, self.cell_size, self.cell_size), 3)
                    else:
                        pygame.draw.rect(self.screen, WHITE, (x, y, self.cell_size, self.cell_size), 1)
                else:
                    # Case vide
                    pygame.draw.rect(self.screen, DARK_GRAY, (x, y, self.cell_size, self.cell_size))
                    pygame.draw.rect(self.screen, GRAY, (x, y, self.cell_size, self.cell_size), 1)

    def draw_inventory_panel(self):
        """Dessine l'inventaire avec icônes"""
        x = self.info_x + 50
        y = self.info_y + 50

        # Titre
        title = self.font_large.render("Inventory:", True, BLACK)
        self.screen.blit(title, (x, y))

        # Ressources avec icônes
        y += 60
        items = [
            ('steps', self.game.player.inventory.steps.quantity, "👣"),
            ('Gold', self.game.player.inventory.gold.quantity, "💰"),
            ('Gem', self.game.player.inventory.gems.quantity, "💎"),
            ('Key', self.game.player.inventory.keys.quantity, "🔑"),
            ('dice', self.game.player.inventory.dice.quantity, "🎲"),
        ]

        for item_name, quantity, emoji in items:
            # Icône
            if item_name in self.item_images:
                icon = pygame.transform.scale(self.item_images[item_name], (32, 32))
                self.screen.blit(icon, (self.info_x + self.info_width - 80, y))
            else:
                # Fallback: emoji
                emoji_surf = self.font_medium.render(emoji, True, BLACK)
                self.screen.blit(emoji_surf, (self.info_x + self.info_width - 80, y))

            # Quantité
            qty_surf = self.font_large.render(str(quantity), True, BLACK)
            self.screen.blit(qty_surf, (self.info_x + self.info_width - 40, y))

            y += 50

        # Objets permanents
        if self.game.player.inventory.permanent_items:
            y += 20
            for item in self.game.player.inventory.permanent_items:
                item_surf = self.font_medium.render(item.name, True, BLACK)
                self.screen.blit(item_surf, (x, y))
                y += 35

    def draw_current_room_panel(self):
        """Affiche info de la pièce actuelle"""
        current_room = self.game.manor.get_room(*self.game.player.position)
        if not current_room:
            return

        x = self.info_x + 50
        y = self.info_y + 450

        # Nom de la pièce
        name_surf = self.font_large.render(current_room.name, True, BLACK)
        self.screen.blit(name_surf, (x, y))

        # Effet si présent
        if current_room.effect:
            y += 60
            effect_surf = self.font_small.render(current_room.effect.description[:50], True, BLUE)
            self.screen.blit(effect_surf, (x, y))

    def draw_direction_indicator(self):
        """Dessine une barre blanche PARALLÈLE au côté de la grille pour la direction sélectionnée"""
        if not self.selected_direction:
            return

        # Position du joueur sur la grille
        row, col = self.game.player.position
        player_x = self.grid_x + col * self.cell_size
        player_y = self.grid_y + row * self.cell_size

        # Dimensions de la barre (PARALLÈLE au côté)
        bar_thickness = 5
        bar_length = self.cell_size  # Même longueur que le côté de la cellule

        # Dessiner la barre PARALLÈLE au côté selon la direction
        if self.selected_direction == Direction.NORTH:
            # Barre HORIZONTALE au-dessus (parallèle au côté nord)
            rect = pygame.Rect(player_x, player_y - bar_thickness - 2, bar_length, bar_thickness)
        elif self.selected_direction == Direction.SOUTH:
            # Barre HORIZONTALE en-dessous (parallèle au côté sud)
            rect = pygame.Rect(player_x, player_y + self.cell_size + 2, bar_length, bar_thickness)
        elif self.selected_direction == Direction.WEST:
            # Barre VERTICALE à gauche (parallèle au côté ouest)
            rect = pygame.Rect(player_x - bar_thickness - 2, player_y, bar_thickness, bar_length)
        elif self.selected_direction == Direction.EAST:
            # Barre VERTICALE à droite (parallèle au côté est)
            rect = pygame.Rect(player_x + self.cell_size + 2, player_y, bar_thickness, bar_length)

        pygame.draw.rect(self.screen, WHITE, rect)
        pygame.draw.rect(self.screen, YELLOW, rect, 2)  # Bordure jaune pour le rendre plus visible

    def draw_game_over_state(self):
        """Écran de fin"""
        if self.game.state == GameState.GAME_WON:
            title = self.font_large.render("VICTORY!", True, GREEN)
            message = "You reached the Antechamber!"
        else:
            title = self.font_large.render("GAME OVER", True, RED)
            message = "Out of steps..." if not self.game.player.is_alive() else "Cannot progress..."

        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 300))
        msg_surf = self.font_medium.render(message, True, WHITE)
        self.screen.blit(msg_surf, (self.screen_width // 2 - msg_surf.get_width() // 2, 400))
        
        restart = self.font_small.render("Press ENTER to restart", True, WHITE)
        self.screen.blit(restart, (self.screen_width // 2 - restart.get_width() // 2, 500))
