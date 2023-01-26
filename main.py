# class for player
# class for field
# method to print field out
# class for ships
import config


dictionary_of_ships = {1: [], 2: [], 3: [], 4: []}
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letters_lowercase = "abcdefghijklmnopqrstuvwxyz"
separators = " .-=+/?!@#$%^&*()_\\"
roman = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX','X']
graphix = {-1: "o",
           0: ".",
           1: "*",
           2: "X"}


def count_ships(dict):
    number = 0
    for value in dict.values():
        number += len(value)
    return number


def create_empty_map():
    temp_map = [[0 for col in range(config.width)] for row in range(config.height)]
    return temp_map


intersections = create_empty_map()
shots_map = create_empty_map()


class Field:
    def __init__(self):
        self.width = config.width
        self.height = config.height
        self.form = config.form
        self.matrix = create_empty_map()

    def show(self):
        header = [i for i in range(1, self.width + 1)]
        print('   ' + ' '.join(str(element) for element in header))
        print('-'*(2*self.width + 2))
        for row in range(self.height):
            if config.form == "letters":
                print(letters[row]+'| '+' '.join(str(graphix[element]) for element in self.matrix[row]))
            elif config.form == "roman":
                print('X'*((row+1)//10)+roman[(row+1)%10]+'| '+' '.join(str(element) for element in self.matrix[row]))
            elif config.form == "digit":
                print(str(row+1) + '| ' + ' '.join(str(element) for element in self.matrix[row]))


class Shot:
    def __init__(self, a, b, f: Field):
        self.x, self.y = a, b
        if shots_map[self.x][self.y] == 0:
            shots_map[self.x][self.y] = 1
            f.matrix[self.x][self.y] -= 1
            f.show()
            for size in dictionary_of_ships:
                for ship in dictionary_of_ships[size]:
                    if (self.x, self.y) in ship.tiles:
                        ship.hp -= 1
                        ship.check_hp(f)
        else:
            print('Cannot shoot here')


class Sheep:
    def __init__(self, head, tail):
        self.topleft = (min(head[0]-1, tail[0]-1), min(head[1]-1, tail[1]-1))
        self.bottomright = (max(head[0]-1, tail[0]-1), max(head[1]-1, tail[1]-1))
        self.spawnbox = (
            (max(self.topleft[0]-1, 0), max(self.topleft[1]-1, 0)),
            (min(self.bottomright[0]+1, config.width-1), min(self.bottomright[1]+1, config.height-1)
             )
                              )
        if self.topleft[0] == self.bottomright[0]:  # if horizontal (or singular)
            self.length = abs(self.topleft[1] - self.bottomright[1]) + 1
            self.tiles = [(self.topleft[0], y) for y in range(self.topleft[1], self.topleft[1] + self.length)]
        else:  # otherwise
            self.length = abs(self.topleft[0] - self.bottomright[0]) + 1
            self.tiles = [(x, self.topleft[1]) for x in range(self.topleft[0], self.topleft[0] + self.length)]
        self.hp = 2 * self.length
        self.temporal_shipmap = create_empty_map()

        if check_existence_possibility(self) and check_intersection(self) and check_size(self):
            for x in range(self.spawnbox[0][0], self.spawnbox[1][0] + 1):
                for y in range(self.spawnbox[0][1], self.spawnbox[1][1] + 1):
                    intersections[x][y] = 1
            for item in self.tiles:
                x, y = item
                self.temporal_shipmap[x][y] = 2
            add_ship(self)
            self.alive = True

    def place(self, field_class):
        for row in range(config.height):
            for col in range(config.width):
                field_class.matrix[row][col] += self.temporal_shipmap[row][col]

    def check_hp(self, f: Field):
        if self.hp <= self.length:
            self.alive = False
            if config.autocover:
                self.cover_spawn_area_in_shots(f)

    def cover_spawn_area_in_shots(self, f: Field):
        for x in range(self.spawnbox[0][0], self.spawnbox[1][0] + 1):
            for y in range(self.spawnbox[0][1], self.spawnbox[1][1] + 1):
                temp_shot = Shot(x, y, f)  # just let machine shoot for you!



def check_existence_possibility(newship: Sheep):
    if len(dictionary_of_ships[newship.length]) < config.existence_of_the_ships[newship.length]:
        return True
    else:
        print("Error: max number of sheep of selected size reached")
        return False


def check_intersection(newship: Sheep):
    for item in newship.tiles:
        x, y = item
        if intersections[x][y] == 1:
            print("Error: cannot place sheep here")
            return False
        return True


def check_size(newship: Sheep):
    if (newship.topleft[0]-newship.bottomright[0]) * (newship.topleft[1]-newship.bottomright[1]) == 0:
        return True
    else:
        print("Error: cannot add the sheep of selected size")
        return False


def add_ship(ship):
    dictionary_of_ships[ship.length].append(ship)
    ship.place(field)


def translate(input):
    x0 = max(letters.find(input[0]), letters_lowercase.find(input[0]))+1
    y0 = int(input[1:])
    res = (x0, y0)
    return res


def cut_coordinates(str):
    for symbol in separators:
        index = str.find(symbol)
        if index != -1:
            beginning = str[:index]
            ending = str[index+1:]
            return beginning, ending
    return 0, 0


def announce_ships():
    message = "Singular sheep: " + str(len(dictionary_of_ships[1])) + '/' + str(config.existence_of_the_ships[1]) + \
        '\n' + "Double sheep: " + str(len(dictionary_of_ships[2])) + '/' + str(config.existence_of_the_ships[2]) +\
        '\n' + "Triple sheep: " + str(len(dictionary_of_ships[3])) + '/' + str(config.existence_of_the_ships[3]) +\
        '\n' + "Quadruple sheep: " + str(len(dictionary_of_ships[4])) + '/' + str(config.existence_of_the_ships[4])
    return message


if __name__ == '__main__':
    field = Field()

    field.show()
    while count_ships(dictionary_of_ships) < sum(config.existence_of_the_ships.values()):
        print(announce_ships())
        temp_ship = input("Choose coordinates of the battlesheep (format \'A6 C6\'): ")  # variety of separators avail.
        head_txt, tail_txt = cut_coordinates(temp_ship)
        headx, tailx = translate(head_txt), translate(tail_txt)  # translate is used in shooting too,
        # that is the reason why it is not part of cutting coordinates
        shipx = Sheep(headx, tailx)  # adding new ship to dictionary
        field.show()
    for x in range(10):  # conditions to be added later
        temp_shot = input("Choose where to shoot (format \'A6\'): ")
        tempx, tempy = translate(temp_shot)  # we get x and y coordinates of a shot
        shotx = Shot(tempx-1, tempy-1, field)  # creating new instance of a shot, checking if ship has sunk
        field.show()  # refreshing field
    field.show()  # might need to loop "game window", might need to add score, might need to add turns
