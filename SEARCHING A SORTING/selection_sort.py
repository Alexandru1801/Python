def selection_sort(desordered_list):
    """
    This sorting algorithm improves the effienciency of the bubble algorithm, consist on trveling the array and for each iteration you select that value,
    travel the others until you fing a value smoller than the selected, after that, you may swap them and continue trveling and swawping the array until is ordered.
    """
    n = len(desordered_list)
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if desordered_list[j] < desordered_list[min_index]:
                min_index = j
            desordered_list[i], desordered_list[min_index] = desordered_list[min_index] , desordered_list[i]
    return desordered_list




print(selection_sort([7, 12, 9, 11, 3]))