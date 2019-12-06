from collections import defaultdict

# assuming this graph is a directed tree, with "COM" (Center Of Mass) as root
def build_graps(input):
    # downwards: directed from COM, generally for A)B it's A -> B
    # upwards: directed in the opposite direction, for A)B its A <- B
    downwards = defaultdict(list)
    upwards = {}

    for orbit in input:
        orbited, orbiter = orbit.split(")")
        downwards[orbited].append(orbiter)
        upwards[orbiter] = orbited

    return downwards, upwards


def bfs(graph, root):
    distances = {root: 0}

    to_visit = [root]

    while len(to_visit) > 0:
        node = to_visit.pop(0)
        neighbours = graph[node]
        for neighbour in neighbours:
            distances[neighbour] = distances[node] + 1
            to_visit.append(neighbour)

    return distances


def ancestors(graph, start):
    result = []

    current = start
    while current in graph:
        parent = graph[current]
        result.append(parent)
        current = parent

    return result


def drop_after_first_common_element(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    for i in range(0, len(list1)):
        if list1[i] in set2:
            del list1[i + 1 :]
            break

    for i in range(0, len(list2)):
        if list2[i] in set1:
            del list2[i + 1 :]
            break


def part_one():
    # With breadth-first-search calculate the distances (number of edges)
    # from each node to the root, and sum these together
    with open("./input.txt") as f:
        lines = map(str.strip, f.readlines())

    downwards_graph, _ = build_graps(lines)

    distances = bfs(downwards_graph, "COM")
    total_orbits = sum(distances.values())
    print(total_orbits)


def part_two():
    # Find the first common "ancestor" in the graph of YOU and SAN
    # and count the number of edges involved

    with open("./input.txt") as f:
        lines = map(str.strip, f.readlines())

    _, upwards_graph = build_graps(lines)

    you_ancestors = ancestors(upwards_graph, "YOU")
    santa_ancestors = ancestors(upwards_graph, "SAN")

    # only the closest common ancestor matters
    drop_after_first_common_element(you_ancestors, santa_ancestors)

    # len(...) - 1, because the number of steps are required
    # from the first element of the list to the last
    you_step = len(you_ancestors) - 1
    santa_step = len(santa_ancestors) - 1

    answer = you_step + santa_step

    print(answer)


if __name__ == "__main__":
    # part_one()
    part_two()
