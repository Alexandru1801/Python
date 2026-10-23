def binary_search(my_list, searched_number):
    """
    The binary search consist in select a random value or the midle value on a sorted array, with that value comproves if is
    equal, higher or lower that the value what are you searching, and depending of that repeat the procedure and
    search on a half or on the other depending, repeat this until you find your value.
    """
    left = 0
    right = len(my_list) - 1
    while left <= right:
        mid = (left + right) // 2
    
        if my_list[mid] == searched_number:
            return mid
    
        elif my_list[mid] > searched_number:
            right = mid -1
        else:
            left = mid +1
    return False

print(binary_search([1, 3, 5, 7, 9, 11, 13, 15, 17, 19], 17))