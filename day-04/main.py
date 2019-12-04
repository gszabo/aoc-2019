def passes_criteria(numtext):
    return monoton_digits(numtext) and same_adjacent_digits_but_just_two(numtext)


def monoton_digits(numtext):
    for i in range(0, len(numtext) - 1):
        if numtext[i] > numtext[i + 1]:
            return False
    return True


# criterion for part 1
def same_adjacent_digits(numtext):
    for i in range(0, len(numtext) - 1):
        if numtext[i] == numtext[i + 1]:
            return True
    return False


# criterion for part 2
def same_adjacent_digits_but_just_two(numtext):
    i = 0
    while i < len(numtext) - 1:
        if numtext[i] != numtext[i + 1]:
            i += 1
        else:
            # searching for a group of same digits, indexes from i to j (inclusive)
            # i is the start position of the group
            # j is the end position of the group
            # size of the group is: j - i + 1
            
            j = i + 1
            while j < len(numtext) - 1 and numtext[i] == numtext[j + 1]:
                j += 1
            
            if (j - i + 1) == 2:
                return True
            
            # jump over the group to next start position
            i = j + 1
    
    return False


if __name__ == "__main__":
    start = 246515
    end = 739105
    answer = len([n for n in range(start, end + 1) if passes_criteria(str(n))])
    print(answer)

