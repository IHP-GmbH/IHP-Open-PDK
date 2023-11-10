

class Orientation(object):
    # TODO: this better should match KLayout's transformation code for
    # easy porting
    R0 = 0
    R90 = 1
    R180 = 2
    R270 = 3
    MY = 4
    MYR90 = 5
    MX = 6
    MXR90 = 7

    def concat(self, other):
        raise Exception("Not implemented yet!")

    def getRelativeOrient(self, other):
        raise Exception("Not implemented yet!")


