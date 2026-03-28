def heap_sort(food_bank):
    i = int(len(food_bank) / 2)
    while i >= 0:
        food_bank = heapify_down(food_bank, i, len(food_bank))
        i -= 1

    i = len(food_bank) - 1

    while i > 0:
        temp = food_bank[i]
        food_bank[i] = food_bank[0]
        food_bank[0] = temp
        food_bank = heapify_down(food_bank, 0, i)
        i -= 1

    
    return food_bank


def heapify_down(food_bank, i, list_size):

    left = 2*i + 1
    right = 2*i + 2
    max_index = i

    if (left < list_size and food_bank[left][2] > food_bank[max_index][2]):
        max_index = left
    if (right < list_size and food_bank[right][2] > food_bank[max_index][2]):
        max_index = right
    
    temp = food_bank[i]
    food_bank[i] = food_bank[max_index]
    food_bank[max_index] = temp

    if (i != max_index):
        food_bank = heapify_down(food_bank, max_index, list_size)
    
    return food_bank


if __name__ == "__main__":
    food_bank = [32, 17, 81, 43, 62, 1, 28]
    food_bank = heap_sort(food_bank)
    print(food_bank)
