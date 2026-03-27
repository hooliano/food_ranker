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
    
    def get_entry_nutrient_score(self, index: int, nutrient: str, subcategory: str = "") -> int:
        if subcategory:
            return self.food_list[index]['Data'][nutrient][subcategory]
        
        return self.food_list[index]['Data'][nutrient]
    
    def get_fat_dict(self, index: int, datapoint: str = ""):
        if not datapoint:
            return self.food_list[index]['Data']['Fat']
        else:
            return self.food_list[index]['Data']['Fat'][datapoint]
    
    def get_vitamins_dict(self, index: int, datapoint: str = ""):
        if not datapoint:
            return self.food_list[index]['Data']['Vitamins']
        else:
            return self.food_list[index]['Data']['Vitamins'][datapoint]
    
    # LIST GETTERS
    def get_score_list(self, index: int) -> list:
        score_list: list = []
        data_dict: dict = self.get_entry_data_dict(index)

        for value in data_dict.values():
            if type(value) == dict:
                for subs in value.values():
                    score_list.append(subs)
            else:
                score_list.append(value)
        
        return score_list
    
    def get_score_list_per_category(self, category: str, subcategory = "", size = 0) -> list:
        all_scores: list = []

        if size > 0:
            for i in range(size):
                if not subcategory:
                    all_scores.append([self.get_entry_category(i), self.get_entry_description(i), self.get_entry_nutrient_score(i, category)])
                else:
                    if category == 'Fat':
                        all_scores.append([self.get_entry_category(i), self.get_entry_description(i), self.get_fat_dict(i, subcategory)])
                    else:
                        all_scores.append([self.get_entry_category(i), self.get_entry_description(i), self.get_vitamins_dict(i, subcategory)])
            
            return all_scores
        
        for dictionary in self.food_list:
            if not subcategory:
                all_scores.append([dictionary['Category'], dictionary['Description'], dictionary['Data'][category]])
            else:
                all_scores.append([dictionary['Category'], dictionary['Description'], dictionary['Data'][category][subcategory]])
        return all_scores
    
    def _get_list_from_categorizer(self, category: str, size: int = 0):

        if size > 0:
            if "Vitamin" in category:
                return self.get_score_list_per_category("Vitamins", category, size)
            elif "Fat" in category:
                return self.get_score_list_per_category("Fat", category, size)
            else:
                return self.get_score_list_per_category(category, size=size)

        if "Vitamin" in category:
            return self.get_score_list_per_category("Vitamins", category)
        elif "Fat" in category:
            return self.get_score_list_per_category("Fat", category)
        else:
            return self.get_score_list_per_category(category)
    
    def get_score_list_average_from_list(self, categories: list, size: int = 0):
        list_size = len(categories)
        if (list_size == 0): return []

        final_list = self._get_list_from_categorizer(categories[0], size)

        for i in range(1, list_size):
            current_list = self._get_list_from_categorizer(categories[i], size)

            for val in range(len(final_list)):
                final_list[val][2] += current_list[val][2]
        
        for val in range(len(final_list)):
            final_list[val][2] /= list_size
        
        return final_list
