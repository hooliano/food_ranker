import pygame
from constants import *


class TextInput:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ''
        self.active = False
        self.color = pygame.Color('lightskyblue3')

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 15:
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
        bg_color = ('dodgerblue4') if self.selected else GREY
        text_color = WHITE if self.selected else BLACK

        pygame.draw.rect(WIN, bg_color, self.rect, border_radius=5)
        pygame.draw.rect(WIN, ('lightskyblue3'), self.rect, 1, border_radius=5)

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

    def draw(self, WIN, font):
        pygame.draw.rect(WIN, self.color, self.rect)
        pygame.draw.rect(WIN, BLACK, self.rect, 1)

        label = f'Nutrients ({len(self.options)} selected)'
        text_surf = font.render(label, True, BLACK)
        WIN.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))

        if self.is_open:
            for i, opt in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*self.rect.h, self.rect.w, self.rect.h)

                bg_color = (150, 200, 255) if opt in self.selected else WHITE
                pygame.draw.rect(WIN, bg_color, opt_rect)
                pygame.draw.rect(WIN, BLACK, opt_rect, 1)

                opt_surf = font.render(opt, True, BLACK)
                WIN.blit(opt_surf, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
                return

            if self.is_open:
                for i in range(len(self.options)):
                    opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*self.rect.h, self.rect.w, self.rect.h)
                    if opt_rect.collidepoint(event.pos):
                        choice = self.options[i]
                        if choice in self.selected:
                            self.selected.remove(choice)
                        else:
                            self.selected.append(choice)