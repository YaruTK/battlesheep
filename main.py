# class for player
# class for field
# method to print field out
# class for ships
import parameters

list_of_sheep = []


class Field:
    def __init__(self):
        self.width = parameters.width
        self.height = parameters.height
        self.form = parameters.form
        self.matrix = create_empty_map()

    def show(self):
        for row in range(self.height):
            for col in range(self.width):
                print(str(self.matrix[row][col]) + ' ', end="")
            print('\n')


class Sheep:
    def __init__(self, head, tail):
        x1, y1 = head[0]-1, head[1]-1
        x2, y2 = tail[0]-1, tail[1]-1
        if y1 == y2:
            self.horizontal = True
            self.length = abs(x2 - x1) + 1
        else:
            self.horizontal = False
            self.length = abs(y2 - y1) + 1

        self.temporal_shipmap = create_empty_map()
        if self.horizontal:
            for x in range(min(x1, x2), min(x1, x2) + self.length):
                self.temporal_shipmap[x][y1] = 2
        else:
            for y in range(min(y1, y2), min(y1, y2) + self.length):
                self.temporal_shipmap[x1][y] = 2
        list_of_sheep.append(self)

    def __del__(self):
        try:
            list_of_sheep.remove(self)
        except: # probably it should be written differently
            print("There was a problem deleting file")

    def place(self, field_class):
        for row in range(parameters.height):
            for col in range(parameters.width):
                field_class.matrix[row][col] = field_class.matrix[row][col] + self.temporal_shipmap[row][col]
        if max(map(max, field_class.matrix)) > 2:
            print("There are some overlaps in sheep")


def create_empty_map():
    temp_map = [[0 for col in range(parameters.width)] for row in range(parameters.height)]
    return temp_map


if __name__ == '__main__':
    field = Field()
    ship1 = Sheep((2, 2), (2, 3))
    ship2 = Sheep((6, 6), (6, 9))
    for ship in list_of_sheep:
        ship.place(field)
    field.show()
