import pygame,sys
from .constants import *
from pathlib import Path
from data import access_data
from sorting_algos import *


pygame.init()
pygame.font.init()

class FoodRanker:
    def __init__(self):
        # INITIALIZE DATA
        self.food_bank = access_data.FoodList()

        # SCREEN SETUP
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Customizable Food Ranker")

        # FONTS
        font_path = Path(__file__).resolve().parent / "baguet-script-regular.otf"
        if font_path.exists():
            self.base_font = pygame.font.Font(str(font_path), 32)
        else:
            self.base_font = pygame.font.SysFont("georgia", 32)

        self.user_font = pygame.font.SysFont('georgia', 20)
        self.result_font = pygame.font.SysFont('georgia', 20)

        # INPUT STATE
        self.user_text = ''
        self.input_rect = pygame.Rect(200, 130, 170, 30)
        self.color = pygame.Color('lightskyblue3')

        # SEARCH BUTTON
        self.search_btn_rect = pygame.Rect(150, HEIGHT- 90, 120, 40)
        self.btn_color = pygame.Color('dodgerblue4')

        # RESULTS STATE
        self.results = []
        self.scroll_y = 0
        self.scroll_speed = 25

    def perform_search(self):
        self.results = []
        query = self.user_text.lower()

        if query == '': return

        # LOOP THROUGH ALL ITEMS
        for i in range(self.food_bank.get_list_size()):
            category = self.food_bank.get_entry_category(i).lower()
            description = self.food_bank.get_entry_description(i).lower()
            if query in category or query in description:
                self.results.append(self.food_bank.get_entry_description(i))

        self.scroll_y = 0

    def draw_window(self):
        self.WIN.fill(WHITE)

        # TEXT
        title_surface = self.base_font.render('Welcome to Food Ranker', True, BLACK)
        category_surface = self.user_font.render('Type Category:', True, BLACK)
        sort_surface = self.user_font.render('Sort Method:', True, BLACK)
        self.WIN.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 20))
        self.WIN.blit(category_surface, (50, 130))
        self.WIN.blit(sort_surface, (50, 200))

        # RESULTS AREA
        results_area = pygame.Rect(450, 100, WIDTH - 500, HEIGHT - 150)
        pygame.draw.rect(self.WIN, self.btn_color, results_area, 1)

        self.WIN.set_clip(results_area)
        for i, item_text in enumerate(self.results):
            y_pos = results_area.y + (i*30) + self.scroll_y
            if 100 < y_pos < HEIGHT - 100:
                if len(item_text) > 80: item_text = item_text[:77] + '...'
                item_surf = self.result_font.render(item_text, True, BLACK)
                self.WIN.blit(item_surf, (results_area.x + 10, y_pos))
        self.WIN.set_clip(None)

        # INPUT BOX
        pygame.draw.rect(self.WIN, self.color, self.input_rect,1)
        input_surface = self.user_font.render(self.user_text, True, BLACK)
        self.WIN.blit(input_surface, self.input_rect)

        # SEARCH BUTTON
        pygame.draw.rect(self.WIN, self.btn_color, self.search_btn_rect, border_radius=5)
        btn_text = self.user_font.render('SEARCH', True, WHITE)
        self.WIN.blit(btn_text, (self.search_btn_rect.x + (self.search_btn_rect.width - btn_text.get_width())//2, self.search_btn_rect.y + 8))

        pygame.display.update()

    def main(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # TYPING
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.perform_search()
                    else:
                        if len(self.user_text) < 15:
                            self.user_text += event.unicode

                # BUTTON CLICKS
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.search_btn_rect.collidepoint(pygame.mouse.get_pos()):
                        self.perform_search()

                    # SCROLL
                    if event.button == 4: # scroll up
                        self.scroll_y = min(0, self.scroll_y + self.scroll_speed)
                    if event.button == 5: # scroll down
                        self.scroll_y -= self.scroll_speed
            self.draw_window()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = FoodRanker()
    app.main()