def heap_sort(food_list):
    i = int(len(food_list) / 2)
    while i >= 0:
        food_list = heapify_down(food_list, i, len(food_list))
        i -= 1

    i = len(food_list) - 1

    while i > 0:
        temp = food_list[i]
        food_list[i] = food_list[0]
        food_list[0] = temp
        food_list = heapify_down(food_list, 0, i)
        i -= 1

    
    return food_list


def heapify_down(food_list, i, list_size):

    left = 2*i + 1
    right = 2*i + 2
    max_index = i

    if (left < list_size and food_list[left] > food_list[max_index]):
        max_index = left
    if (right < list_size and food_list[right] > food_list[max_index]):
        max_index = right
    
    temp = food_list[i]
    food_list[i] = food_list[max_index]
    food_list[max_index] = temp

    if (i != max_index):
        food_list = heapify_down(food_list, max_index, list_size)
    
    return food_list


if __name__ == "__main__":
    food_list = [32, 17, 81, 43, 62, 1, 28]
    food_list = heap_sort(food_list)
    print(food_list)
