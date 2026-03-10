from . import food

class FoodList:
    food_list: list = []

    # Initialize the FoodList class object for operations
    def __init__(self):
        self.food_list = food.get_report()
    
    # INFORMATION GETTERS #
    def get_data_keys(self) -> list:
        entry: dict = self.food_list[0]
        return list(entry["Data"].keys())
    
    def get_list_size(self) -> int:
        return len(self.food_list)
    
    # INDEXED GETTER METHODS #
    def get_entry(self, index: int):
        return self.food_list[index]
    
    def get_entry_description(self, index: int):
        return self.food_list[index]["Description"]
    
    def get_entry_category(self, index: int):
        return self.food_list[index]["Category"]
    
    def get_entry_nutrient_data_bank_number(self, index: int):
        return self.food_list[index]["Nutrient Data Bank Number"]
    
    # DATA GETTERS #
    def get_entry_data_dict(self, index: int) -> dict:
        return self.food_list[index]['Data']
    
    def get_entry_nutrient_score(self, index: int, nutrient: str) -> int:
        return self.food_list[index]['Data'][nutrient]
    
