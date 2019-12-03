line = "R8,U5,L5,D3"


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Segment:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start} -> {self.end}"

    def __repr__(self):
        return str(self)


def build_segments(path):
    result = []
    
    # x goes right, y goes up
    x, y = 0, 0
    for step in path:
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
    

s1 = build_segments(line.split(","))
print(s1)