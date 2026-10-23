def insertion_sorting(desordered_list):
    """
    """
    n = len(desordered_list)
    for i in range(1, n):
        actual = desordered_list[i]
        j = i
        while desordered_list[j-1] > actual and j > 0:
            desordered_list[j] = desordered_list[j-1]
            j = j-1
            desordered_list[j] = actual
    return desordered_list

print(insertion_sorting([ 7, 12, 9, 11, 3]))