from collections import defaultdict

# assuming this graph is a directed tree, with "COM" (Center Of Mass) as root
def build_grap(input):
    result = defaultdict(list)

    for orbit in input:
        orbited, orbitee = orbit.split(")")
        result[orbited].append(orbitee)

    return result


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


def part_one():
    with open("./input.txt") as f:
        lines = map(str.strip, f.readlines())
    graph = build_grap(lines)
    distances = bfs(graph, "COM")
    total_orbits = sum(distances.values())
    print(total_orbits)


if __name__ == "__main__":
    part_one()
