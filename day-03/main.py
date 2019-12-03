from __future__ import annotations

from dataclasses import dataclass
from collections import namedtuple


@dataclass(unsafe_hash=True)
class Point:
    """
    In this coordinate system, x goes right, y goes up
    """

    x: int
    y: int

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def origin_dist(self):
        return abs(self.x) + abs(self.y)


@dataclass
class Segment:
    start: Point
    end: Point

    def intersection(self, other: Segment):
        if self.is_perpendicular_to(other):
            horiz = self if self.is_horizontal() else other
            vert = self if self.is_vertical() else other

            left, right = horiz.horizontal_bounds()
            bottom, top = vert.vertical_bounds()

            horiz_y = horiz.start.y
            vert_x = vert.start.x

            if left <= vert_x <= right and bottom <= horiz_y <= top:
                return [Point(vert_x, horiz_y)]
            else:
                return []
        else:
            if self.is_horizontal():
                # other is horizontal, too
                if self.start.y == other.start.y:
                    s_left, s_right = self.horizontal_bounds()
                    o_left, o_right = other.horizontal_bounds()
                    start = max(s_left, o_left)
                    end = min(s_right, o_right)
                    return [Point(x, self.start.y) for x in range(start, end + 1)]
                else:
                    return []
            else:
                # both vertical
                if self.start.x == other.start.x:
                    s_bottom, s_top = self.vertical_bounds()
                    o_bottom, o_top = other.vertical_bounds()
                    start = max(s_bottom, o_bottom)
                    end = min(s_top, o_top)
                    return [Point(self.start.x, y) for y in range(start, end + 1)]
                else:
                    return []

    def is_horizontal(self):
        return self.start.y == self.end.y

    def is_vertical(self):
        return self.start.x == self.end.x

    def horizontal_bounds(self):
        left = min(self.start.x, self.end.x)
        right = max(self.start.x, self.end.x)
        return (left, right)

    def vertical_bounds(self):
        bottom = min(self.start.y, self.end.y)
        top = max(self.start.y, self.end.y)
        return (bottom, top)

    def is_perpendicular_to(self, other: Segment):
        """
        Using the scalar product of the two vectors to tell if
        they are perpendicular
        """

        return self * other == 0

    def __mul__(self, other: Segment):
        """
        The scalar product of the two segment vectors
        """

        return (self.end.x - self.start.x) * (other.end.x - other.start.x) + (
            self.end.y - self.start.y
        ) * (other.end.y - other.start.y)

    def __len__(self):
        return abs(self.start.x - self.end.x) + abs(self.start.y - self.end.y)


def build_path(steps):
    result = []

    x, y = 0, 0
    for step in steps:
        step_direction = step[0]
        step_len = int(step[1:])
        x1, y1 = x, y
        if step_direction == "R":
            x1 += step_len
        elif step_direction == "U":
            y1 += step_len
        elif step_direction == "L":
            x1 -= step_len
        elif step_direction == "D":
            y1 -= step_len

        result.append(Segment(Point(x, y), Point(x1, y1)))

        x, y = x1, y1

    return result


def find_intersections(path1, path2):
    result = set()

    for segment1 in path1:
        for segment2 in path2:
            for point in segment1.intersection(segment2):
                result.add(point)

    result.remove(Point(0, 0))

    return result


PointWithStep = namedtuple("PointWithStep", ["point", "step_sum"])


def find_intersections_with_step(path1, path2):
    origin = Point(0, 0)
    result = set()

    step1 = 0
    for segment1 in path1:
        step2 = 0
        for segment2 in path2:
            for point in segment1.intersection(segment2):
                if point == origin:
                    continue
                
                partial_segment_1 = Segment(segment1.start, point)
                partial_segment_2 = Segment(segment2.start, point)
                step_sum = (
                    step1 + step2 + len(partial_segment_1) + len(partial_segment_2)
                )
                
                result.add(PointWithStep(point, step_sum))

            step2 += len(segment2)

        step1 += len(segment1)

    return result


def part_one():
    with open("./input.txt") as f:
        lines = f.readlines()

    wire1 = build_path(lines[0].strip().split(","))
    wire2 = build_path(lines[1].strip().split(","))

    intersections = find_intersections(wire1, wire2)
    distances = list(map(Point.origin_dist, intersections))
    print(min(distances))


def part_two():
    with open("./input.txt") as f:
        lines = f.readlines()

    wire1 = build_path(lines[0].strip().split(","))
    wire2 = build_path(lines[1].strip().split(","))

    intersections = find_intersections_with_step(wire1, wire2)
    distances = list(map(lambda dist: dist.step_sum, intersections))
    print(min(distances))


if __name__ == "__main__":
    # part_one()
    part_two()
