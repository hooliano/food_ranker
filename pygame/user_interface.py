import pygame,sys
from constants import *
from access_data import *
from heap_sort import *
from merge_sort import *


pygame.init()
pygame.font.init()

class FoodRanker:
    def __init__(self):
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Customizable Food Ranker")
        self.base_font = pygame.font.Font('baguet-script-regular.otf', 32)
        self.user_font = pygame.font.SysFont('Arial', 24)
        self.user_text = ''


        self.input_rect = pygame.Rect(300, 80, 200, 40)
        self.color = pygame.Color('lightskyblue3')

    def draw_window(self):
        self.WIN.fill(WHITE)
        text_surface = self.base_font.render('YOUR CUSTOMIZABLE FOOD RANKER', True, BLACK)
        self.WIN.blit(text_surface, (140, 20))
        pygame.draw.rect(self.WIN, self.color, self.input_rect,2)
        input_surface = self.user_font.render(self.user_text, True, BLACK)
        self.WIN.blit(input_surface, self.input_rect)
        pygame.display.update()

    def main(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[0:-1]
                    else:
                        self.user_text += event.unicode

            self.draw_window()

        pygame.quit()

if __name__ == "__main__":
    app = FoodRanker()
    app.main()