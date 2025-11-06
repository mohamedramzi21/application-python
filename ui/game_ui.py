"""
Interface graphique avec Pygame
"""
import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional
from game.game import Game, GameState
from core.game_objects import Direction

# Couleurs - Theme sombre
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# Couleurs vives pour meilleur contraste sur fond noir
BLUE = (100, 180, 255)
GREEN = (100, 255, 150)
RED = (255, 100, 100)
YELLOW = (255, 240, 100)
PURPLE = (200, 120, 255)
ORANGE = (255, 180, 50)

# Mapping des couleurs de pièces
ROOM_COLORS = {
    'blue': BLUE,
    'green': GREEN,
    'red': RED,
    'yellow': YELLOW,
    'purple': PURPLE,
    'orange': ORANGE
}


class GameUI:
    """Interface graphique principale du jeu"""

    def __init__(self, game: Game):
        pygame.init()

        self.game = game
        self.screen_width = 1400
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Blue Prince - Simplified")

        # Polices
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        # Dimensions de la grille
        self.grid_x = 50
        self.grid_y = 100
        self.cell_size = 80

        # Selection pour le choix de pièces
        self.selected_room_index = 0

        # FPS
        self.clock = pygame.time.Clock()
        self.fps = 60

    def run(self):
        """Boucle principale du jeu"""
        running = True

        while running:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Gestion des événements selon l'état du jeu
                if self.game.state == GameState.PLAYING:
                    self.handle_playing_events(event)
                elif self.game.state == GameState.ROOM_SELECTION:
                    self.handle_room_selection_events(event)
                elif self.game.is_game_over():
                    self.handle_game_over_events(event)

            # Affichage - Fond noir
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
        """Gestion des événements pendant le jeu"""
        if event.type == pygame.KEYDOWN:
            # Déplacement avec les FLÈCHES
            if event.key == pygame.K_UP:  # Nord
                self.game.try_move(Direction.NORTH)
            elif event.key == pygame.K_DOWN:  # Sud
                self.game.try_move(Direction.SOUTH)
            elif event.key == pygame.K_RIGHT:  # Est
                self.game.try_move(Direction.EAST)
            elif event.key == pygame.K_LEFT:  # Ouest
                self.game.try_move(Direction.WEST)

            # Interaction avec les objets (touches 1-9)
            elif pygame.K_1 <= event.key <= pygame.K_9:
                object_index = event.key - pygame.K_1
                self.game.interact_with_object(object_index)

            # Afficher l'inventaire (touche I)
            elif event.key == pygame.K_i:
                print(self.game.player.inventory)

    def handle_room_selection_events(self, event):
        """Gestion des événements lors de la sélection de pièce"""
        if event.type == pygame.KEYDOWN:
            # Sélection avec A (gauche) et D (droite)
            if event.key == pygame.K_a:  # A = Gauche
                self.selected_room_index = (self.selected_room_index - 1) % len(self.game.pending_room_selection)
            elif event.key == pygame.K_d:  # D = Droite
                self.selected_room_index = (self.selected_room_index + 1) % len(self.game.pending_room_selection)

            # Validation avec ESPACE
            elif event.key == pygame.K_SPACE:
                if self.game.select_room(self.selected_room_index):
                    self.selected_room_index = 0

            # Redraw avec R (si on a des dés)
            elif event.key == pygame.K_r:
                if self.game.reroll_rooms():
                    self.selected_room_index = 0

    def handle_game_over_events(self, event):
        """Gestion des événements en fin de partie"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Redémarrer le jeu
                self.game = Game()
                self.selected_room_index = 0

    def draw_playing_state(self):
        """Affiche l'état de jeu normal"""
        # Titre
        title = self.font_large.render("Blue Prince", True, WHITE)
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 20))

        # Grille du manoir
        self.draw_manor_grid()

        # Inventaire
        self.draw_inventory()

        # Informations de la pièce actuelle
        self.draw_current_room_info()

        # Instructions
        self.draw_instructions()

    def draw_room_selection_state(self):
        """Affiche l'écran de sélection de pièce"""
        # Titre
        title = self.font_large.render("Choisissez une piece", True, WHITE)
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))

        # Afficher les 3 pièces proposées
        if self.game.pending_room_selection:
            room_width = 300
            room_height = 400
            spacing = 50
            start_x = (self.screen_width - (room_width * 3 + spacing * 2)) // 2
            start_y = 200

            for i, room in enumerate(self.game.pending_room_selection):
                x = start_x + i * (room_width + spacing)

                # Rectangle de la pièce
                color = ROOM_COLORS.get(room.color.value, GRAY)
                if i == self.selected_room_index:
                    pygame.draw.rect(self.screen, WHITE, (x - 5, start_y - 5, room_width + 10, room_height + 10), 5)

                pygame.draw.rect(self.screen, color, (x, start_y, room_width, room_height))
                pygame.draw.rect(self.screen, WHITE, (x, start_y, room_width, room_height), 2)

                # Nom de la pièce
                name_surf = self.font_medium.render(room.name, True, BLACK)
                name_rect = name_surf.get_rect(center=(x + room_width // 2, start_y + 30))
                self.screen.blit(name_surf, name_rect)

                # Informations
                y_offset = start_y + 80

                # Coût en gemmes
                cost_text = f"Cout: {room.gem_cost} gemme(s)"
                cost_color = RED if not self.game.player.can_afford_room(room.gem_cost) else BLACK
                cost_surf = self.font_small.render(cost_text, True, cost_color)
                self.screen.blit(cost_surf, (x + 10, y_offset))
                y_offset += 30

                # Rareté
                rarity_text = f"Rarete: {'*' * room.rarity}{' ' * (3 - room.rarity)}"
                rarity_surf = self.font_small.render(rarity_text, True, BLACK)
                self.screen.blit(rarity_surf, (x + 10, y_offset))
                y_offset += 30

                # Portes
                doors_text = f"Portes: {len(room.doors_directions)}"
                doors_surf = self.font_small.render(doors_text, True, BLACK)
                self.screen.blit(doors_surf, (x + 10, y_offset))
                y_offset += 30

                # Objets
                objects_text = f"Objets: {len(room.objects)}"
                objects_surf = self.font_small.render(objects_text, True, BLACK)
                self.screen.blit(objects_surf, (x + 10, y_offset))
                y_offset += 40

                # Effet
                if room.effect:
                    effect_lines = self.wrap_text(room.effect.description, room_width - 20, self.font_small)
                    for line in effect_lines:
                        effect_surf = self.font_small.render(line, True, BLACK)
                        self.screen.blit(effect_surf, (x + 10, y_offset))
                        y_offset += 25

        # Instructions
        instructions = [
            "A / D : Selectionner",
            "ESPACE : Valider",
            f"R : Redraw (Des: {self.game.player.inventory.dice.quantity})"
        ]

        y = self.screen_height - 120
        for instruction in instructions:
            text = self.font_small.render(instruction, True, WHITE)
            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, y))
            y += 30

    def draw_game_over_state(self):
        """Affiche l'écran de fin de partie"""
        if self.game.state == GameState.GAME_WON:
            title = self.font_large.render("VICTOIRE!", True, GREEN)
            message = "Vous avez atteint l'Antichambre!"
        else:
            title = self.font_large.render("DEFAITE", True, RED)
            if not self.game.player.is_alive():
                message = "Vous n'avez plus de pas..."
            else:
                message = "Vous ne pouvez plus progresser..."

        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 300))

        message_surf = self.font_medium.render(message, True, WHITE)
        self.screen.blit(message_surf, (self.screen_width // 2 - message_surf.get_width() // 2, 400))

        restart = self.font_small.render("Appuyez sur ENTREE pour recommencer", True, WHITE)
        self.screen.blit(restart, (self.screen_width // 2 - restart.get_width() // 2, 500))

    def draw_manor_grid(self):
        """Dessine la grille du manoir"""
        for row in range(self.game.manor.height):
            for col in range(self.game.manor.width):
                x = self.grid_x + col * self.cell_size
                y = self.grid_y + row * self.cell_size

                room = self.game.manor.get_room(row, col)

                if room:
                    # Couleur de la pièce
                    color = ROOM_COLORS.get(room.color.value, GRAY)
                    pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

                    # Bordure
                    border_color = YELLOW if (row, col) == self.game.player.position else WHITE
                    border_width = 4 if (row, col) == self.game.player.position else 1
                    pygame.draw.rect(self.screen, border_color, (x, y, self.cell_size, self.cell_size), border_width)

                    # Nom de la pièce (abrégé)
                    name = room.name[:8]
                    name_surf = self.font_small.render(name, True, BLACK)
                    name_rect = name_surf.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                    self.screen.blit(name_surf, name_rect)
                else:
                    # Case vide
                    pygame.draw.rect(self.screen, BLACK, (x, y, self.cell_size, self.cell_size))
                    pygame.draw.rect(self.screen, GRAY, (x, y, self.cell_size, self.cell_size), 1)

    def draw_inventory(self):
        """Dessine l'inventaire du joueur"""
        x = self.grid_x + self.game.manor.width * self.cell_size + 100
        y = self.grid_y

        title = self.font_medium.render("Inventaire", True, WHITE)
        self.screen.blit(title, (x, y))
        y += 40

        inv = self.game.player.inventory

        items = [
            f"Pas: {inv.steps.quantity}",
            f"Or: {inv.gold.quantity}",
            f"Gemmes: {inv.gems.quantity}",
            f"Cles: {inv.keys.quantity}",
            f"Des: {inv.dice.quantity}"
        ]

        for item in items:
            text = self.font_small.render(item, True, WHITE)
            self.screen.blit(text, (x, y))
            y += 30

        y += 20
        perm_title = self.font_small.render("Objets permanents:", True, WHITE)
        self.screen.blit(perm_title, (x, y))
        y += 25

        if inv.permanent_items:
            for perm_item in inv.permanent_items:
                text = self.font_small.render(f"* {perm_item.name}", True, GREEN)
                self.screen.blit(text, (x + 10, y))
                y += 25
        else:
            text = self.font_small.render("(aucun)", True, GRAY)
            self.screen.blit(text, (x + 10, y))

    def draw_current_room_info(self):
        """Dessine les informations de la pièce actuelle"""
        x = self.grid_x
        y = self.grid_y + self.game.manor.height * self.cell_size + 50

        room = self.game.player.current_room

        title = self.font_medium.render(f"Piece: {room.name}", True, WHITE)
        self.screen.blit(title, (x, y))
        y += 40

        # Objets dans la pièce
        if room.objects:
            objects_title = self.font_small.render("Objets:", True, WHITE)
            self.screen.blit(objects_title, (x, y))
            y += 25

            for i, obj in enumerate(room.objects):
                text = self.font_small.render(f"{i + 1}. {obj.name}", True, YELLOW)
                self.screen.blit(text, (x + 20, y))
                y += 25
        else:
            text = self.font_small.render("Aucun objet", True, GRAY)
            self.screen.blit(text, (x, y))

    def draw_instructions(self):
        """Dessine les instructions"""
        x = self.grid_x + self.game.manor.width * self.cell_size + 100
        y = self.grid_y + 400

        title = self.font_small.render("Controles:", True, WHITE)
        self.screen.blit(title, (x, y))
        y += 30

        instructions = [
            "Z/Q/S/D : Se deplacer",
            "1-9 : Interagir avec objet",
            "I : Afficher inventaire"
        ]

        for instruction in instructions:
            text = self.font_small.render(instruction, True, LIGHT_GRAY)
            self.screen.blit(text, (x, y))
            y += 25

    def wrap_text(self, text: str, max_width: int, font) -> list:
        """Découpe un texte en plusieurs lignes"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines