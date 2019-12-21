def pattern(digit_pos):
    base_pattern = [0, 1, 0, -1]
    i = 0
    while True:
        for _ in range(0, digit_pos):
            yield base_pattern[i]
        i = (i + 1) % len(base_pattern)


def take(n, gen):
    i = 0
    for item in gen:
        if i < n:
            yield item
        else:
            return
        
        i += 1

def skip(n, gen):
    i = 0
    for item in gen:
        if n <= i:
            yield item
        
        i += 1

def algo_phase(digits):
    result = []
    for i in range(0, len(digits)):
        digit_pos = i+1
        s = 0
        for digit, pat_digit in zip(digits, skip(1, pattern(digit_pos))):
            s += digit * pat_digit
        result.append(abs(s) % 10)

    return result

def simple_algo_phase(digits):
    result = []

    s = sum(digits)

    result.append(s % 10)
    for i in range(0, len(digits) - 1):
        digit = digits[i]
        s -= digit
        result.append(s % 10)

    return result

def text_to_digits(text):
    return [int(ch) for ch in text]

def digits_to_text(digits):
    return "".join(map(str, digits))


def part_one():
    with open("./input.txt") as f:
        input = f.readline().strip()
    digits = text_to_digits(input)
    for _ in range(0, 100):
        digits = algo_phase(digits)
    answer = digits_to_text(digits)[:8]
    print(answer)

def part_two():
    with open("./input.txt") as f:
        input = f.readline().strip()
    offset = int(input[0:7])
    digits = text_to_digits((input*10000)[offset:])
    for _ in range(0, 100):
        digits = simple_algo_phase(digits)
    answer = digits_to_text(digits)[:8]
    print(answer)


if __name__ == "__main__":
    part_one()
    print()
    part_two()

