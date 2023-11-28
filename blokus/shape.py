import math

def rotatex(coords, ref, deg):
    """
    Returns the new x value of a point (x, y) rotated about the point (refx, refy) by deg degrees clockwise.
    """
    x = coords[0]
    y = coords[1]
    refx = ref[0]
    refy = ref[1]
    return (math.cos(math.radians(deg))*(x - refx)) + (math.sin(math.radians(deg))*(y - refy)) + refx

def rotatey(coords, ref, deg):
    """
    Returns the new y value of a point (x, y) rotated about the point (refx, refy) by deg degrees clockwise.
    """
    x = coords[0]
    y = coords[1]
    refx = ref[0]
    refy = ref[1]
    return (- math.sin(math.radians(deg))*(x - refx)) + (math.cos(math.radians(deg))*(y - refy)) + refy

def rotatep(p, ref, d):
    """
    Returns the new point as an integer tuple of a point p (tuple) rotated about the point ref (tuple) by d degrees
    clockwise.
    """
    return (int(round(rotatex(p, ref, d))), int(round(rotatey(p, ref, d))))

class Shape(object):
    """
    A class that defines the functions associated with a shape.
    """

    def __init__(self):
        self.ID = "None"
        self.size = 1

      
    def create(self, num, pt):
        self.set_points(0, 0)
        pm = self.points
        self.points_map = pm
        self.refpt = pt
        x = pt[0] - self.points_map[num][0]
        y = pt[1] - self.points_map[num][1]
        self.set_points(x, y)

    def set_points(self, x, y):
        self.points = []
        self.corners = []

    def rotate(self, degrees):
        """
        Returns the points that would be covered by a shape that is rotated 0, 90, 180, of 270 degrees in a clockwise
        direction.
        """
        assert (self.points != "None")
        assert (degrees in [0, 90, 180, 270])

        def rotate_this(p):
            return (rotatep(p, self.refpt, degrees))

        self.points = list(map(rotate_this, self.points))
        self.corners = list(map(rotate_this, self.corners))

    def flip(self, orientation):
        """
        Returns the points that would be covered if the shape was flipped horizontally or vertically.
        """
        assert (orientation == "h" or orientation == "None")
        assert (self.points != "None")

        def flip_h(p):
            x1 = self.refpt[0]
            x2 = p[0]
            x1 = (x1 - (x2 - x1))
            return (x1, p[1])

        def no_flip(p):
            return p

        # flip the piece horizontally
        if orientation == "h":
            self.points = list(map(flip_h, self.points))
            self.corners = list(map(flip_h, self.corners))
        # flip the piece vertically
        elif orientation == "None":
            self.points = list(map(no_flip, self.points))
            self.corners = list(map(no_flip, self.corners))
        else:
            raise Exception("Invalid orientation.")

class I1(Shape):

    def __init__(self):
        self.ID = "I1"
        self.size = 1
        self.shift = 90
        self.flips = ['None']
        self.rots = [0]
    def set_points(self, x, y):
        self.points = [(x, y)]
        self.corners = [(x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]

class I2(Shape):

    def __init__(self):
        self.ID = "I2"
        self.size = 2
        self.shift = 86
        self.flips = ['None']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1), (x + 1, y + 2), (x - 1, y + 2)]

class I3(Shape):
    def __init__(self):
        self.ID = "I3"
        self.size = 3
        self.shift = 84
        self.flips = ['None']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1), (x + 1, y + 3), (x - 1, y + 3)]

class I4(Shape):
    def __init__(self):
        self.ID = "I4"
        self.size = 4
        self.shift = 82
        self.flips = ['None']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x, y + 3)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1), (x + 1, y + 4), (x - 1, y + 4)]

class I5(Shape):
    def __init__(self):
        self.ID = "I5"
        self.size = 5
        self.shift = 80
        self.flips = ['None']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x, y + 3), (x, y + 4)]
        self.corners = [(x - 1, y - 1), (x + 1, y - 1), (x + 1, y + 5), (x - 1, y + 5)]

class V3(Shape):
    def __init__(self):
        self.ID = "V3"
        self.size = 3
        self.shift = 76
        self.flips = ['None', 'h']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2), (x - 1, y + 2)]

class L4(Shape):
    def __init__(self):
        self.ID = "L4"
        self.size = 4
        self.shift = 40
        self.flips = ['None', 'h']
        self.rots = [0, 90, 180, 270]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 3), (x - 1, y + 3)]

class Z4(Shape):
    def __init__(self):
        self.ID = "Z4"
        self.size = 4
        self.shift = 68
        self.flips = ['None', 'h']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1), (x - 1, y)]
        self.corners = [(x - 2, y - 1), (x + 1, y - 1), (x + 2, y), (x + 2, y + 2), (x - 1, y + 2), (x - 2, y + 1)]

class O4(Shape):
    def __init__(self):
        self.ID = "O4"
        self.size = 4
        self.shift = 89
        self.flips = ['None']
        self.rots = [0]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1), (x + 1, y)]
        self.corners = [(x - 1, y - 1), (x + 2, y - 1), (x + 2, y + 2), (x - 1, y + 2)]

class L5(Shape):
    def __init__(self):
        self.ID = "L5"
        self.size = 5
        self.shift = 8
        self.flips = ['None', 'h']
        self.rots = [0, 90, 180, 270]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x + 2, y), (x + 3, y)]
        self.corners = [(x - 1, y - 1), (x + 4, y - 1), (x + 4, y + 1), (x + 1, y + 2), (x - 1, y + 2)]

class T5(Shape):
    def __init__(self):
        self.ID = "T5"
        self.size = 5
        self.shift = 56
        self.flips = ['None', 'h']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x - 1, y), (x + 1, y)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 3), (x - 1, y + 3), (x - 2, y + 1), (x - 2, y - 1)]

class V5(Shape):
    def __init__(self):
        self.ID = "V5"
        self.size = 5
        self.shift = 52
        self.flips = ['None', 'h']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x + 1, y), (x + 2, y)]
        self.corners = [(x - 1, y - 1), (x + 3, y - 1), (x + 3, y + 1), (x + 1, y + 3), (x - 1, y + 3)]

class N(Shape):
    def __init__(self):
        self.ID = "N"
        self.size = 5
        self.shift = 0 
        self.flips = ['None', 'h']
        self.rots = [0, 90, 180, 270]
    def set_points(self, x, y):
        self.points = [(x, y), (x + 1, y), (x + 2, y), (x, y - 1), (x - 1, y - 1)]
        self.corners = [(x + 1, y - 2), (x + 3, y - 1), (x + 3, y + 1), (x - 1, y + 1), (x - 2, y), (x - 2, y - 2)]

class Z5(Shape):
    def __init__(self):
        self.ID = "Z5"
        self.size = 5
        self.shift = 64
        self.flips = ['None', 'h']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x + 1, y), (x + 1, y + 1), (x - 1, y), (x - 1, y - 1)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 2), (x, y + 2), (x - 2, y + 1), (x - 2, y - 2), (x, y - 2)]

class T4(Shape):
    def __init__(self):
        self.ID = "T4"
        self.size = 4
        self.shift = 48
        self.flips = ['None', 'h']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x - 1, y)]
        self.corners = [(x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2), (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1)]

class P(Shape):
    def __init__(self):
        self.ID = "P"
        self.size = 5
        self.shift = 24
        self.flips = ['None', 'h']
        self.rots = [0, 90, 180, 270]
    def set_points(self, x, y):
        self.points = [(x, y), (x + 1, y), (x + 1, y - 1), (x, y - 1), (x, y - 2)]
        self.corners = [(x + 1, y - 3), (x + 2, y - 2), (x + 2, y + 1), (x - 1, y + 1), (x - 1, y - 3)]

class W(Shape):
    def __init__(self):
        self.ID = "W"
        self.size = 5
        self.shift = 72
        self.flips = ['None', 'h']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1), (x - 1, y), (x - 1, y - 1)]
        self.corners = [(x + 1, y - 1), (x + 2, y), (x + 2, y + 2), (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 2),
                        (x, y - 2)]

class U(Shape):
    def __init__(self):
        self.ID = "U"
        self.size = 5
        self.shift = 60
        self.flips = ['None', 'h']
        self.rots = [0, 90]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1), (x, y - 1), (x + 1, y - 1)]
        self.corners = [(x + 2, y - 2), (x + 2, y), (x + 2, y + 2), (x - 1, y + 2), (x - 1, y - 2)]

class F(Shape):
    def __init__(self):
        self.ID = "F"
        self.size = 5
        self.shift = 32
        self.flips = ['None', 'h']
        self.rots = [0, 90, 180, 270]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y + 1), (x, y - 1), (x - 1, y)]
        self.corners = [(x + 1, y - 2), (x + 2, y), (x + 2, y + 2), (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1),
                        (x - 1, y - 2)]

class X(Shape):
    def __init__(self):
        self.ID = "X"
        self.size = 5
        self.shift = 88
        self.flips = ['None']
        self.rots = [0]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
        self.corners = [(x + 1, y - 2), (x + 2, y - 1), (x + 2, y + 1), (x + 1, y + 2), (x - 1, y + 2), (x - 2, y + 1),
                        (x - 2, y - 1), (x - 1, y - 2)]

class Y(Shape):
    def __init__(self):
        self.ID = "Y"
        self.size = 5
        self.shift = 16
        self.flips = ['None', 'h']
        self.rots = [0, 90, 180, 270]
    def set_points(self, x, y):
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x + 2, y), (x - 1, y)]
        self.corners = [(x + 3, y - 1), (x + 3, y + 1), (x + 1, y + 2), (x - 1, y + 2), (x - 2, y + 1), (x - 2, y - 1)]

All_Shapes = [N(), L5(), Y(), P(), F(), L4(), T4(), V5(), T5(), U(), Z5(), Z4(), W(), V3(), I5(), I4(), I3(), I2(), X(), O4(), I1()]
