def bubble_sorting(desordered_list):
    """
    This is the more ineficient sorting algorithm, travel all the array and compare one value by the other, if is higher than the first one, switch them, 
    in the other case, you may pass one value forward and compare the second with the next one, repeat until the list is sorted.
    """
    n = len(desordered_list)
    for i in range(n):
        for j in range(n-1):
            if desordered_list[j] > desordered_list[j+1]:
                desordered_list[j], desordered_list[j+1] = desordered_list[j+1], desordered_list[j]

    return desordered_list

print(bubble_sorting([64, 34, 25, 12, 22, 11, 90, 5]))

