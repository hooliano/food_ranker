def merge_sort(food_list):
    if len(food_list) <= 1:
        return food_list
    
    mid = int(len(food_list) / 2)
    list2_size = len(food_list) - mid
    
    list1 = []
    list2 = []

    for i in range(mid):
        list1.append(food_list[i])
    
    for i in range(list2_size):
        list2.append(food_list[i+mid])

    list1 = merge_sort(list1)
    list2 = merge_sort(list2)

    i = 0 
    j = 0
    k = 0
    
    while (i < len(list1) and k < len(list2)):
        if list1[i] <= list2[k]:
            food_list[j] = list1[i]
            i += 1
        else:
            food_list[j] = list2[k]
            k += 1
        j += 1

    while i < len(list1):
        food_list[j] = list1[i]
        i += 1
        j += 1

    while k < len(list2):
        food_list[j] = list2[k]
        k += 1
        j += 1

    return food_list

if __name__ == "__main__":
    list1 = [72, 84, 32, 21, 19, 1002, 1023]
    list1 = merge_sort(list1)
    print(list1)
