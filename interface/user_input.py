import pygame
from interface.constants import *


class TextInput:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ''
        self.active = False
        self.color = pygame.Color('lightskyblue3')

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                self.color = pygame.Color('dodgerblue2') 
            else:
                self.color = pygame.Color('lightskyblue3')

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
            elif len(self.text) < 15 and event.unicode.isdigit():
                self.text += event.unicode

    def draw(self, WIN, font):
        pygame.draw.rect(WIN, self.color, self.rect, 1)
        text_surf = font.render(self.text, True, BLACK)
        WIN.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))

        if self.active and (pygame.time.get_ticks() // 500) % 2 == 0:
            tx = self.rect.x + 5 + font.size(self.text)[0]
            pygame.draw.line(WIN, BLACK, (tx, self.rect.y + 5), (tx, self.rect.y + self.rect.h - 5), 2)


class SortOption:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.selected = False

    def draw(self, WIN, font):
        bg_color = 'dodgerblue4' if self.selected else GREY
        text_color = WHITE if self.selected else BLACK

        pygame.draw.rect(WIN, bg_color, self.rect, border_radius=5)
        pygame.draw.rect(WIN, 'lightskyblue3', self.rect, 1, border_radius=5)

        surf = font.render(self.text, True, text_color)
        WIN.blit(surf, (self.rect.x + (self.rect.w - surf.get_width())//2, self.rect.y + (self.rect.h - surf.get_height())//2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class MultiSelectMenu:
    def __init__(self, x, y, w, h, options):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.selected = []
        self.is_open = False
        self.color = pygame.Color('lightskyblue3')

        # SCROLL
        self.scroll_y = 0
        self.max_visible_options = 5
        self.option_height = 35
        self.dropdown_rect = pygame.Rect(x, y+h, w, self.option_height * self.max_visible_options)
        self.is_dragging = False
        self.last_mouse_y = 0

    def draw(self, WIN, font):
        pygame.draw.rect(WIN, WHITE, self.rect)
        pygame.draw.rect(WIN, BLACK, self.rect, 1)

        display_text = ', '.join(self.selected)
        if not self.selected:
            display_text = 'Select Nutrients...'
        if font.size(display_text)[0] > self.rect.w - 30:
            display_text = display_text[:25] + '...'

        text_surf = font.render(display_text, True, (50, 50, 50))
        WIN.blit(text_surf, (self.rect.x + 5, self.rect.y + (self.rect.h - text_surf.get_height())//2))

        arrow_color = (100, 100, 100)
        p1 = (self.rect.right - 20, self. rect.centery - 5)
        p2 = (self.rect.right - 5, self. rect.centery - 5)
        p3 = (self.rect.right - 12, self. rect.centery + 5)
        pygame.draw.polygon(WIN, arrow_color, [p1, p2, p3])

        if self.is_open:
            pygame.draw.rect(WIN, WHITE, self.dropdown_rect)
            pygame.draw.rect(WIN, BLACK, self.dropdown_rect, 1)

            WIN.set_clip(self.dropdown_rect)

            for i, opt in enumerate(self.options):
                opt_y = self.dropdown_rect.y + (i * self.option_height) + self.scroll_y
                opt_draw_rect = pygame.Rect(self.rect.x, opt_y, self.rect.w, self.option_height)

                if opt_draw_rect.bottom > self.dropdown_rect.top and opt_draw_rect.top < self.dropdown_rect.bottom:
                    if opt in self.selected:
                        pygame.draw.rect(WIN, (180, 220, 255), opt_draw_rect)

                    pygame.draw.rect(WIN, (200, 200, 200), opt_draw_rect, 1)
                    opt_surf = font.render(opt, True, BLACK)
                    WIN.blit(opt_surf, (opt_draw_rect.x + 10, opt_draw_rect.y + 5))

            WIN.set_clip(None)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button != 1:
                return

            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
                return

            if self.is_open and self.dropdown_rect.collidepoint(event.pos):
                relative_y = event.pos[1] - self.dropdown_rect.y - self.scroll_y
                clicked_idx = int(relative_y // self.option_height)

                if 0 <= clicked_idx < len(self.options):
                    choice = self.options[clicked_idx]
                    if choice in self.selected:
                        self.selected.remove(choice)
                    else:
                        self.selected.append(choice)

                self.is_dragging = True
                self.last_mouse_y = event.pos[1]
            else:
                self.is_open = False

        # MOVING WITH MOUSE
        elif event.type == pygame.MOUSEWHEEL and self.is_open:
            self.scroll_y += event.y * 15
            max_scroll = -(len(self.options) * self.option_height - self.dropdown_rect.h)
            if self.scroll_y > 0: self.scroll_y = 0
            if self.scroll_y < max_scroll: self.scroll_y = max_scroll

        # MOVING WITH FINGER
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging and self.is_open:
                delta_y = event.pos[1] - self.last_mouse_y
                self.scroll_y += delta_y
                self.last_mouse_y = event.pos[1]

                max_scroll = -(len(self.options) * self.option_height - self.dropdown_rect.h)
                if self.scroll_y > 0: self.scroll_y = 0
                if len(self.options) * self.option_height > self.dropdown_rect.h:
                    if self.scroll_y < max_scroll: self.scroll_y = max_scroll
                else:
                    self.scroll_y = 0

        #
        elif event.type == pygame.MOUSEBUTTONUP:
                self.is_dragging = False
