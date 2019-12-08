WIDTH = 25
HEIGHT = 6
IMAGE_SIZE = WIDTH * HEIGHT

BLACK = 0
WHITE = 1
TRANSPARENT = 2


def split_into_layers(image: list) -> list:
    layers = []
    for i in range(0, len(image), IMAGE_SIZE):
        layers.append(image[i : i + IMAGE_SIZE])

    return layers


def zero_count(layer: list) -> int:
    return digit_count(layer, 0)


def digit_count(layer: list, target: int) -> int:
    return len([digit for digit in layer if digit == target])


def digit_to_print_char(digit: int) -> str:
    if digit in {BLACK, TRANSPARENT}:
        return " "
    else:
        # looked up from: https://en.wikipedia.org/wiki/Box-drawing_character
        # U+2593: DARK SHADE
        return "\u2593"


def print_image(image: list):
    for row_start in range(0, len(image), WIDTH):
        print("".join(map(digit_to_print_char, image[row_start : row_start + WIDTH])))


def part_one():
    with open("./input.txt") as f:
        input = list(map(int, f.readline().strip()))
    layers = split_into_layers(input)

    checksum_layer = min(layers, key=zero_count)

    answer = digit_count(checksum_layer, 1) * digit_count(checksum_layer, 2)

    print(answer)


def part_two():
    with open("./input.txt") as f:
        input = list(map(int, f.readline().strip()))
    layers = split_into_layers(input)

    # pre-fill list with transparent pixels in the appropriate size
    result_image = [TRANSPARENT] * IMAGE_SIZE

    for i in range(0, len(result_image)):
        for layer in layers:
            if layer[i] != TRANSPARENT:
                result_image[i] = layer[i]
                break

    print_image(result_image)


if __name__ == "__main__":
    part_one()
    print()
    part_two()

