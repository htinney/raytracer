import math
import json, jsonpickle
from linearalgebra import *

# An axis-aligned boudning box
class BBOX():
    def __init__(self, center, extent):
        self.center = center
        self.extent = size / 2
        self.x_plane = Plane(Vector3(y=0.0, z=0.0), center.X)
        self.y_plane = Plane(Vector3(x=0.0, z=0.0), center.Y)
        self.z_plane = Plane(Vector3(x=0.0, y=0.0), center.Z)

    def contains(self, p_center, p_extent=Vector3() * 0):
        if p_center.x + p_extent.x <= self.center.x + self.extent.x and \
           p_center.x - p_extent.x >= self.center.x - self.extent.x and \
           p_center.y + p_extent.y <= self.center.y + self.extent.y and \
           p_center.y - p_extent.y >= self.center.y + self.extent.y and \
           p_center.z + p_extent.z <= self.center.z + self.extent.z and \
           p_center.z - p_extent.z >= self.center.z + self.extent.z:
           return True

class Material():
    def __init__(self,
                 diffuse,
                 diffuse_intensity,
                 specular,
                 specular_intensity,
                 ambient,
                 ambient_intensity,
                 gloss):
        self.d = diffuse
        self.d_int = diffuse_intensity
        self.s = specular
        self.s_int = specular_intensity
        self.a = ambient
        self.a_int = ambient_intensity
        self.g = gloss

    def shade(self, V, N, R, L, light):
        # diffuse
        d = light.intensity * light.color * self.d * (N ** L)
        # specular
        s = light.intensity * light.color * self.s * math.pow((V * R), self.g)
        # ambient
        a = self.a
        #combined
        return d * self.d_int + s * self.s_int + a * self.a_int

class Sphere():
    def __init__(self, pos=Vector3() * 0, radius=1.0):
        self.pos = pos
        self.radius = radius
        self.center = pos
        self.extent = (Vector3() * self.radius) / 2

    def intersect(self, ray):
        pass

    def get_normal(self, point):
        pass

class Cube():
    def __init__(self, pos=Vector3() * 0, size=1.0):
        self.pos = pos
        self.size = size
        self.center = pos
        self.extent = (Vector3() * self.size) / 2

    def intersect(self, ray):
        pass

class Plane():
    def __init__(self, normal=Vector3() * 0, distance=1.0):
        self.normal = normal
        self.distance = distance

    def intersect(self, ray):
        pass

class CustomOBJ():
    def __init__(self, pos=Vector3() * 0, filepath="test.obj"):
        self.transform = transform
        self.filepath = filepath

class Octree():
    def __init__(self, center=Vector3() * 0, size=1.0, objects=[]):
        children = []
        for object in objects:
            object_bbox = object.center

    def intersect(self, ray):
        pass

class Camera():
    def __init__(self,
                 pos=Vector3() * 0,
                 forward=Vector3(x=0.0, y=0.0, z=-1.0),
                 up=Vector3(x=0.0, z=0.0),
                 fov=40.0):
        self.pos = pos
        self.forward = forward
        self.up = up
        self.right = (forward % up).normalized()
        self.fov = fov
        self.transform = Matrix3(cols=[self.right,
                                         self.up,
                                         self.forward])

class PointLight():
    def __init__(self, pos=Vector3() * 0, color=Vector3(), intensity=1.0):
        self.pos = pos
        self.color = color
        self.intensity = intensity

    def intersect(self, origin):
        return False

class SceneDescription():
    def __init__(self, lights=[], objects=[]):
        self.lights = lights
        self.objects = objects

    def import_from_file(self, file):
        with open(file, 'r') as f:
            updated = jsonpickle.decode(json.load(f))
            self.__dict__.update(updated.__dict__)

    def export_to_file(self, file):
        with open(file, 'w') as f:
            f.write(json.dumps(jsonpickle.encode(self)))

    def flatten_to_octree(self):
        return Octree()
