WIDTH = 25
HEIGHT = 6


def split_into_layers(image: list) -> list:
    layer_size = WIDTH * HEIGHT

    layers = []
    for i in range(0, len(image), layer_size):
        layers.append(image[i : i + layer_size])

    return layers


def zero_count(layer: list) -> int:
    return digit_count(layer, 0)


def digit_count(layer: list, target: int) -> int:
    return len([digit for digit in layer if digit == target])


def part_one():
    with open("./input.txt") as f:
        input = list(map(int, f.readline().strip()))
    layers = split_into_layers(input)

    checksum_layer = min(layers, key=zero_count)

    answer = digit_count(checksum_layer, 1) * digit_count(checksum_layer, 2)

    print(answer)


if __name__ == "__main__":
    part_one()

