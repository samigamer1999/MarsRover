class Rover(object):
    BEARINGS = ["N", "E", "S", "W"]

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # Index of bearing

    def single_move(self, move):
        """Updates position/direction based one the current move"""
        if move == "R":
            self.direction = (self.direction + 1) % 4
        elif move == "L":
            self.direction = (self.direction - 1) % 4
        # Forward
        elif move == "F":
            # Facing NORTH
            if self.direction == 0:
                self.y += 1
            # Facing EAST
            elif self.direction == 1:
                self.x += 1
            # Facing SOUTH
            elif self.direction == 2:
                self.y -= 1
            # Facing WEST
            elif self.direction == 3:
                self.x -= 1
        # Backward
        elif move == "B":
            # Facing NORTH
            if self.direction == 0:
                self.y -= 1
            # Facing EAST
            elif self.direction == 1:
                self.x -= 1
            # Facing SOUTH
            elif self.direction == 2:
                self.y += 1
            # Facing WEST
            elif self.direction == 3:
                self.x += 1
        else:
            print(move + " is not a move. Skipped !")

    def execute_line(self, inpt):
        # Get moves and apply each move
        for move in inpt:
            self.single_move(move)

    def execute(self, inpt):
        output = []
        instructions = inpt.splitlines()

        if len(inpt) == 0:
            output.append("0 0 N")

        for instruction in instructions:
            self.execute_line(instruction)
            output.append(str(self.x) + " " + str(self.y) + " " + self.BEARINGS[self.direction])

        return output

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_direction(self):
        return self.direction

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_direction(self, direction):
        self.direction = direction
