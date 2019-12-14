from collections import defaultdict


def read_equations(path):
    chemical_equations = {}

    with open(path) as f:
        lines = list(map(str.strip, f.readlines()))

    for line in lines:
        source_side, result_side = line.split(" => ")

        result_amount, result_element = result_side.split(" ")
        result_amount = int(result_amount)

        source_chemicals = {}

        for source_item in source_side.split(", "):
            amount, chemical = source_item.split(" ")
            amount = int(amount)
            source_chemicals[chemical] = amount

        chemical_equations[result_element] = {
            "result_amount": result_amount,
            "input": source_chemicals,
        }

    return chemical_equations


chemical_equations = read_equations("./input.txt")


def add_to_lab(lab, chemical, amount):
    """
    Updates the laboratory resource info by applying the
    equation corresponding to the given chemical creation.
    If there is not enough input chemicals for the eqution,
    those will go below zero, appearing as "debt".
    """

    produce_info = chemical_equations[chemical]
    amount_per_reaction = produce_info["result_amount"]

    reaction_count = amount // amount_per_reaction
    if (amount % amount_per_reaction) > 0:
        reaction_count += 1

    for input_chemical, input_amount in produce_info["input"].items():
        lab[input_chemical] -= input_amount * reaction_count

    lab[chemical] += amount_per_reaction * reaction_count


def create_missing_chemicals(lab):
    """
    Until there is resource "debt" in the lab, it creates the missing
    resources, by spending ORE.
    """
    while True:
        negative_keys = list(filter(lambda k: k != "ORE" and lab[k] < 0, lab.keys()))
        if len(negative_keys) == 0:
            break
        chemical_to_add = negative_keys[0]
        add_to_lab(lab, chemical_to_add, abs(lab[chemical_to_add]))


def part_one():
    # Here we create an empty lab, and add one FUEL to it.
    # After paying the debt in ORE, the ORE deficit is
    # going to tell the price of a FUEL.
    lab = defaultdict(int)

    add_to_lab(lab, "FUEL", 1)
    create_missing_chemicals(lab)

    answer = -lab["ORE"]

    print(answer)


def part_two():
    ORE_AMOUNT = 1000000000000
    ORE_PER_FUEL = 346961  # From part 1

    lab = defaultdict(int)
    lab["ORE"] = ORE_AMOUNT

    while lab["ORE"] > ORE_PER_FUEL:
        # We know we can create at least
        # lab["ORE"] // ORE_PER_FUEL amount of fuel.
        # We need to go in these big steps, otherwise
        # the calculation is too slow.
        add_to_lab(lab, "FUEL", lab["ORE"] // ORE_PER_FUEL)
        create_missing_chemicals(lab)

    while lab["ORE"] >= 0:
        # There might be enough leftover resource for more fuel.
        # If ORE counts goes below zero, we know we tried to
        # create one too many fuel
        add_to_lab(lab, "FUEL", 1)
        create_missing_chemicals(lab)

    answer = lab["FUEL"] - 1

    print(answer)


if __name__ == "__main__":
    part_one()
    print()
    part_two()
