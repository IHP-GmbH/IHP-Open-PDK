

class Location(object):

    LOWER_LEFT = 1
    CENTER_LEFT = 2
    UPPER_LEFT = 3
    LOWER_CENTER = 4
    CENTER_CENTER = 5
    UPPER_CENTER = 6
    LOWER_RIGHT = 7
    CENTER_RIGHT = 8
    UPPER_RIGHT = 9

    def mirrorX(self):
        raise Exception("Not implemented yet!")

    def mirrorY(self):
        raise Exception("Not implemented yet!")

    def rotate90(self):
        raise Exception("Not implemented yet!")

    def rotate180(self):
        raise Exception("Not implemented yet!")

    def rotate270(self):
        raise Exception("Not implemented yet!")

    def transform(self, transform):
        raise Exception("Not implemented yet!")



