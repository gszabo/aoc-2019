def generate_permutations(n):
    """
    Generates all the permutations of the numbers 0, 1, 2, ..., n-1
    """
    
    if n == 0:
        return []
    
    def _perms(numbers: list) -> list:
        if len(numbers) == 1:
            return [[numbers[0]]]
        
        result = []
        for i in range(0, len(numbers)):
            copy = numbers.copy()
            perm = [copy[i]]
            del copy[i]
            for continuation in _perms(copy):
                result.append(perm + continuation)
        
        return result

    return _perms(list(range(0, n)))
