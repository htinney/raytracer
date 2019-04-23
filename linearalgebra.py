import math

class Vector3():
    def __init__(self, x=1.0, y=1.0, z=1.0):
        self.x , self.y, self.z = x, y, z

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalized(self):
        return self / self.magnitude()

    def __str__(self):
        return "{0} {1} {2}".format(self.x, self.y, self.z)

    # USES % FOR CROSS PRODUCT
    def __mod__(self, other):
        return Vector3(x=(self.y * other.z - self.z * other.y),
                       y=-(self.x * other.z - self.z * other.x),
                       z=(self.x * other.y - self.y * other.x))

    # USES ** FOR DOT PRODUCT
    def __pow__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(x=self.x + other.x,
                           y=self.y + other.y,
                           z=self.z + other.z)
        else:
            return Vector3(x=self.x + other,
                           y=self.y + other,
                           z=self.z + other)

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(x=self.x - other.x,
                           y=self.y - other.y,
                           z=self.z - other.z)
        else:
            return Vector3(x=self.x - other,
                           y=self.y - other,
                           z=self.z - other)


    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(x=self.x * other.x,
                           y=self.y * other.y,
                           z=self.z * other.z)
        else:
            return Vector3(x=self.x * other,
                           y=self.y * other,
                           z=self.z * other)

    def __truediv__(self, scalar):
        return Vector3(x=self.x / scalar,
                       y=self.y / scalar,
                       z=self.z / scalar)

    def __div__(self, scalar):
        return Vector3(x=self.x / scalar,
                       y=self.y / scalar,
                       z=self.z / scalar)
    __rmod__ = __mod__
    __rpow__ = __pow__
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__
    __rdiv__ = __div__

class Matrix3():
    def __init__(self,
                 m=[1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0],
                 rows=(None, None, None),
                 cols=(None, None, None)):
        self.m = m
        for i, row in enumerate(rows):
            if row is not None:
                self.m[i] = row.x
                self.m[i + 1] = row.y
                self.m[i + 2] = row.z

        for i, col in enumerate(cols):
            if col is not None:
                self.m[(3 * i)] = col.x
                self.m[(3 * i) + 1] = col.y
                self.m[(3 * i) + 2] = col.z

    def row(self, i):
        return Vector3(self.m[i], self.m[i + 1], self.m[i + 2])

    def col(self, i):
        return Vector3(self.m[(3 * i)], self.m[(3 * i) + 1], self.m[(3 * i) + 2])

    def __mul__(self, other):
        if isinstance(other, Matrix3):
            m = [
                self.row(0) ** other.col(0),
                self.row(0) ** other.col(1),
                self.row(0) ** other.col(2),
                self.row(1) ** other.col(0),
                self.row(1) ** other.col(1),
                self.row(1) ** other.col(2),
                self.row(2) ** other.col(0),
                self.row(2) ** other.col(1),
                self.row(2) ** other.col(2)
            ]
            return Matrix3(m=m)

        elif isinstance(other, Vector3):
            x = self.row(0) ** other
            y = self.row(1) ** other
            z = self.row(2) ** other
            return Vector3(x=x, y=y, z=z)
        else:
            return None
