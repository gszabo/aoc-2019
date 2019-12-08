def generate_permutations(n):
    """
    Generates all the permutations of the numbers 0, 1, 2, ..., n-1
    """
    
    return permutations_of(list(range(0, n)))

def permutations_of(items):
    """
    Generate all the permutations of the items
    """

    if len(items) == 0:
        return []
    
    if len(items) == 1:
        return [[items[0]]]
    
    result = []
    for i in range(0, len(items)):
        copy = items.copy()
        perm = [copy[i]]
        del copy[i]
        for continuation in permutations_of(copy):
            result.append(perm + continuation)
    
    return result