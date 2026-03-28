import pygame,sys
import math
import time
from data.access_data import *
from interface.user_input import *
from sorting_algos.heap_sort import *
from sorting_algos.merge_sort import *


pygame.init()
pygame.font.init()
pygame.key.set_repeat(300, 50)

class FoodRanker:
    def __init__(self):
        # INITIALIZE DATA
        self.user_text = None
        self.food_bank = FoodList()

        # SCREEN SETUP
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Customizable Food Ranker")

        # FONTS
        self.title_font = pygame.font.Font('interface/baguet-script-regular.otf', 32)
        self.base_font = pygame.font.SysFont('georgia', 20)
        self.category_font = pygame.font.SysFont('georgia', 12)

        # INPUT
        self.inputs = [
            TextInput(175, 200, 170, 30,)
        ]
        self.inputs[0].text = '10'
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('dodgerblue4')

        # SORT BUTTON
        self.sort_buttons = [
            SortOption(173, 260, 120, 40, 'Heap Sort'),
            SortOption(300, 260, 120, 40, 'Merge Sort'),
        ]
        self.sort_buttons[0].selected = True
        self.current_sort = 'Heap Sort'

        # NUTRITION MENU
        nutrients_available = ['Alpha Carotene', 'Beta Carotene', 'Beta Cryptoxanthin', 'Carbohydrate', 'Cholesterol', 'Choline', 'Fiber', 'Lutein and Zeaxanthin', 'Lycopene', 'Niacin', 'Protein', 'Retinol', 'Riboflavin', 'Selenium', 'Sugar Total', 'Thiamin', 'Water', 'Fat', 'Monosaturated Fat', 'Polysaturated Fat', 'Saturated Fat', 'Total Lipid', 'Major Minerals', 'Calcium', 'Copper', 'Iron', 'Magnesium', 'Phosphorus', 'Potassium', 'Sodium', 'Zinc', 'Vitamins', 'Vitamin A - RAE', 'Vitamin B12', 'Vitamin B6', 'Vitamin C', 'Vitamin E', 'Vitamin K']
        self.nutrient_menu = MultiSelectMenu(175, 130, 170, 30, nutrients_available)

        # SEARCH BUTTON
        self.search_btn_rect = pygame.Rect(150, HEIGHT- 90, 120, 40)
        self.btn_color = pygame.Color('dodgerblue4')

        # RESULTS STATE
        self.results = []
        self.scroll_y = 0
        self.scroll_speed = 25
        self.heap_sort_time = 0.0
        self.merge_sort_time = 0.0

    def perform_search(self):
        try:
            limit = int(self.inputs[0].text)
        except ValueError:
            print("Invalid list size input. Default set to 10.")
            limit = 10

        if len(self.nutrient_menu.get_selected()) == 0:
            self.results = ["Please select at least one category."]
            self.heap_sort_time = 0.0
            self.merge_sort_time = 0.0
            self.scroll_y = 0
            return
        
        category_list = self.nutrient_menu.get_selected()

        unsorted_results = self.food_bank.get_score_list_average_from_list(category_list)

        heapSortTime = 0
        mergeSortTime = 0

        temp_results = []
        if self.current_sort == 'Heap Sort':
            heapFirstTime = time.perf_counter()
            temp_results = heap_sort(unsorted_results)
            heapSecondTime = time.perf_counter()
            self.heap_sort_time = heapSecondTime - heapFirstTime

            mergeFirstTime = time.perf_counter()
            ignored_results = merge_sort(unsorted_results)
            mergeSecondTime = time.perf_counter()
            self.merge_sort_time = mergeSecondTime - mergeFirstTime

        if self.current_sort == 'Merge Sort':
            mergeFirstTime = time.perf_counter()
            temp_results = merge_sort(unsorted_results)
            mergeSecondTime = time.perf_counter()
            self.merge_sort_time = mergeSecondTime - mergeFirstTime

            heapFirstTime = time.perf_counter()
            ignored_results = heap_sort(unsorted_results)
            heapSecondTime = time.perf_counter()
            self.heap_sort_time = heapSecondTime - heapFirstTime
        
        # limit the results to size
        self.results.clear()
        final_matches = temp_results[-limit:][::-1]
        list_rank = 1
        for food_item in final_matches:
            case = 77
            result_msg = f"{list_rank}. {food_item[1]} - Score: {math.trunc(food_item[2] * 100) / 100}"
            if len(result_msg) > case:
                result_msg = result_msg[:case] + '\n' + result_msg[case:]
                case *= 2
            for result_msgo in result_msg.split('\n'):
                self.results.append(result_msgo)
            list_rank += 1
        self.scroll_y = 0

    def draw_window(self):
        self.WIN.fill(WHITE)

        # TEXT
        title_surface = self.title_font.render('Welcome to Food Ranker', True, BLACK)
        self.WIN.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 20))
        category_surface = self.base_font.render('Category', True, BLACK)
        sort_surface = self.base_font.render('List Size', True, BLACK)
        size_surface = self.base_font.render('Sort Method', True, BLACK)
        self.WIN.blit(category_surface, (50, 130))
        self.WIN.blit(sort_surface, (50, 200))
        self.WIN.blit(size_surface, (50, 270))

        # RESULTS AREA
        results_area = pygame.Rect(450, 100, WIDTH - 500, HEIGHT - 150)
        pygame.draw.rect(self.WIN, self.btn_color, results_area, 1)

        self.WIN.set_clip(results_area)
        for i, item_text in enumerate(self.results):
            y_pos = results_area.y + (i*30) + self.scroll_y           
            item_surf = self.base_font.render(item_text, True, BLACK)
            self.WIN.blit(item_surf, (results_area.x + 10, y_pos))
        self.WIN.set_clip(None)

        if (self.heap_sort_time > 0 and self.merge_sort_time > 0):
            heap_time_text = self.base_font.render(f"  Heap Sort Time: {math.trunc(self.heap_sort_time * 1000000) / 1000000} seconds", True, BLACK)
            merge_time_text = self.base_font.render(f"Merge Sort Time: {math.trunc(self.merge_sort_time * 1000000) / 1000000} seconds", True, BLACK)
            self.WIN.blit(heap_time_text, (50, 340))
            self.WIN.blit(merge_time_text, (50, 370))

        # INPUT BOX
        for box in self.inputs:
            box.draw(self.WIN, self.base_font)

        # SORT BUTTON
        for btn in self.sort_buttons:
            btn.draw(self.WIN, self.base_font)

        # NUTRITION MENU
        self.nutrient_menu.draw(self.WIN, self.category_font)

        # SEARCH BUTTON
        pygame.draw.rect(self.WIN, self.btn_color, self.search_btn_rect, border_radius=5)
        btn_text = self.base_font.render('SEARCH', True, WHITE)
        self.WIN.blit(btn_text, (self.search_btn_rect.x + (self.search_btn_rect.width - btn_text.get_width())//2, self.search_btn_rect.y + 8))

        pygame.display.update()

    def main(self):
        results_area = pygame.Rect(450, 100, WIDTH - 500, HEIGHT - 150)
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # INPUT
                for box in self.inputs:
                    box.handle_event(event)

                self.nutrient_menu.handle_event(event)

                # SORT
                for btn in self.sort_buttons:
                    if btn.handle_event(event):
                        for b in self.sort_buttons: b.selected = False
                        btn.selected = True
                        self.current_sort = btn.text

                # BUTTON CLICKS
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.search_btn_rect.collidepoint(pygame.mouse.get_pos()):
                        self.perform_search()

                    list_screen_size = 30 * len(self.results)
                    if list_screen_size > results_area.height:
                        max_scroll = (list_screen_size - results_area.height) * -1
                        if max_scroll > self.scroll_y:
                            self.scroll_y = max_scroll
                    else:
                        if event.button == 5:
                            self.scroll_y = 0

                    # SCROLL
                    if results_area.collidepoint(pygame.mouse.get_pos()):
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