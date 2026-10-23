def quicksort(desordered_list):
    """
    The quicksort algorith is the most effient, consist in takin the mid element (pivot value) in the array and with two list (lower num, and highest num) adds the
    numbers to the corresponding list, next, use  recursion repeat the process But for one, you pass the list with the small ones as a value, and for the other, 
    you pass the list with the large ones, and finaly, join the lists and the pivot value.
    """
    if len(desordered_list) <= 1:
        return desordered_list
    
    low = []
    high = []

    n = len(desordered_list)
    index = n // 2
    pivot_value = desordered_list[index]

    for elem in desordered_list:
        if elem < pivot_value:
            low.append(elem)
        elif elem >= pivot_value:
            high.append(elem)

    low = quicksort(low)
    high = quicksort(high)

    return low + [pivot_value] + high


print(quicksort([64, 34, 25, 12, 22, 11, 90, 5]))

