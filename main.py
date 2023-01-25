# class for player
# class for field
# method to print field out
# class for ships
import config
import numpy as np


list_of_sheep = {1: [], 2: [], 3: [], 4: []}
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def create_empty_map():
    temp_map = [[0 for col in range(config.width)] for row in range(config.height)]
    return temp_map


intersections = create_empty_map()


class Field:
    def __init__(self):
        self.width = config.width
        self.height = config.height
        self.form = config.form
        self.matrix = create_empty_map()

    def show(self):
        header = [i for i in range(self.width + 1)]
        print(' ' + ' '.join(str(element) for element in header))
        print('-'*(2*self.width + 2))
        for row in range(self.height):
            print(letters[row]+'| '+' '.join(str(element) for element in self.matrix[row]))


class Sheep:
    def __init__(self, head, tail):
        self.topleft = (min(head[0]-1, tail[0]-1), min(head[1]-1, tail[1]-1))
        self.bottomright = (max(head[0]-1, tail[0]-1), max(head[1]-1, tail[1]-1))
        self.spawnbox = (
            (max(self.topleft[0]-1, 0), max(self.topleft[1]-1, 0)),
            (min(self.bottomright[0]+1, config.width), min(self.bottomright[1]+1, config.height)
             )
                              )
        if self.topleft[1] == self.bottomright[1]:
            self.horizontal = True
            self.length = abs(self.topleft[0] - self.bottomright[0]) + 1
        else:
            self.horizontal = False
            self.length = abs(self.topleft[1] - self.bottomright[1]) + 1
        self.temporal_shipmap = create_empty_map()
        if check_existence_possibility(self) and check_intersection(self):
            for x in range(self.spawnbox[0][0], self.spawnbox[1][0]):
                for y in range(self.spawnbox[1][0], self.spawnbox[1][1]):
                    intersections[x][y] = 1
            if self.horizontal:
                for x in range(self.topleft[0], self.topleft[0] + self.length):
                    self.temporal_shipmap[x][self.topleft[1]] = 2
            else:
                for y in range(self.topleft[1], self.topleft[1] + self.length):
                    self.temporal_shipmap[self.topleft[0]][y] = 2
            add_ship(self)

    def place(self, field_class):
        for row in range(config.height):
            for col in range(config.width):
                field_class.matrix[row][col] += self.temporal_shipmap[row][col]


def check_existence_possibility(newship:Sheep):
    if len(list_of_sheep[newship.length]) < config.existence_of_the_ships[newship.length]:
        return True
    else:
        return False


def check_intersection(newship: Sheep):
    for x in range(newship.spawnbox[0][0], newship.spawnbox[1][0]):
        for y in range(newship.spawnbox[1][0], newship.spawnbox[1][1]):
            if intersections[x][y] == 1:
                return False
            else:
                return True


def check_size(newship: Sheep):
    if (newship.topleft[0]-newship.bottomright[0]) * (newship.topleft[1]-newship.bottomright[1]) == 0:
        return True
    else:
        return False


def add_ship(ship):
    if check_size(ship):
        list_of_sheep[ship.length].append(ship)
        ship.place(field)
    else:
        print("Wrong shape of the sheep")


if __name__ == '__main__':
    field = Field()
    ship1 = Sheep((2, 2), (2, 3))
    ship2 = Sheep((6, 6), (6, 9))

    field.show()
