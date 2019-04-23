import os
import random
from scenedescription import *
from linearalgebra import *
import ray
ray.shutdown()
ray.init(num_gpus=1)

import time

def generate_example():
    sd = SceneDescription()
    main_light = PointLight()
    main_light.pos += Vector3(0.0, 1.0, 0.0)
    sd.lights.append(main_light)
    sd.objects.append(Sphere())
    sd.export_to_file("example.json")

def test():
    rt = Raytracer()
    for i in range(1,100):
        time1 = time.time()
        rt.gradient_fill(partitions=i)
        time2 = time.time()
        print('Gradient fill with {} took {:.3f} ms'.format(i, (time2-time1)*1000.0))
    rt.write()

class Raycast():
    def __init__(self, origin=Vector3(), direction=Vector3()):
        self.origin = origin
        self.direction = direction

@ray.remote
class GradientFiller():
    def __init__(self, res_x, res_y, x_color1, x_color2, y_color1, y_color2):
        self.res_x, self.res_y = res_x, res_y
        self.x_color1, self.x_color2 = x_color1, x_color2
        self.y_color1, self.y_color2 = y_color1, y_color2
        self.pixels = [[Vector3() for y in range(res_y)] for x in range(res_x)]

    def gradient_fill_cell_range(self, x1, x2, y1, y2):
        for x in range(x1, x2):
            for y in range(y1, y2):
                percent_x = float(x) / float(self.res_x)
                percent_y = float(y) / float(self.res_y)
                x_color = (1 - percent_x) * self.x_color1 + (percent_x) * self.x_color2
                y_color = (1 - percent_y) * self.y_color1 + (percent_y) * self.y_color2
                color = 0.5 * x_color + 0.5 * y_color
                self.pixels[x][y] = color
        #return color

    def get_pixels(self):
        return self.pixels

    def gradient_fill_row(self, x):
        row = []
        for y in range(self.res_y):
            row.append(self.gradient_fill_cell.remote(x, y))
        return ray.get(row)

    def gradient_fill(self):
        rows = []
        for x in range(self.res_x):
            rows.append(self.gradient_fill_row.remote(x))
        return ray.get(rows)

class Raytracer():
    def __init__(self,
                 res_x=500,#300,
                 res_y=500,#600,
                 camera=Camera(),
                 bg_color=Vector3(),
                 scenefile="example.scenedsc",
                 outfile="example.ppm"):

        if scenefile == "example.scenedsc":
            generate_example()
        self.res_x = res_x
        self.res_y = res_y
        self.aspect = float(res_x) / float(res_y)
        self.bg_color = bg_color
        self.scene_description = SceneDescription()
        self.scene_description.import_from_file(scenefile)
        self.outfile = outfile
        self.pixels = [[Vector3() for y in range(res_y)] for x in range(res_x)]


    def gradient_fill(self,
                     partitions = 5,
                     x_color1=Vector3(x=1.0, y=0.0, z=0.0),
                     x_color2=Vector3(x=0.5, y=1.0, z=0.0),
                     y_color1=Vector3(x=0.0, y=1.0, z=0.0),
                     y_color2=Vector3(x=0.0, y=0.5, z=1.0)):

        filler = GradientFiller.remote(self.res_x,
                                self.res_y,
                                x_color1,
                                x_color2,
                                y_color1,
                                y_color2)

        x_partition_size = int(self.res_x / partitions)
        y_partition_size = int(self.res_y / partitions)
        for i in range(partitions):
            x1 = x_partition_size * i
            x2 = x1 + x_partition_size
            x2 = x2 if x2 <= self.res_x else self.res_x
            for j in range(partitions):
                y1 = y_partition_size * j
                y2 = y1 + y_partition_size
                y2 = y2 if y2 <= self.res_y else self.res_y
                filler.gradient_fill_cell_range.remote(x1, x2, y1, y2)

        self.pixels = ray.get(filler.get_pixels.remote())


    def trace(self, samples=1):
        self.octree = self.scene_description.flatten_to_octree(self.camera)
        for i in samples:
            for x in range(self.res_x):
                for y in range(self.res_y):
                    print("({0}, {1}) {2} samples".format(x, y, i))
                    self.pixels[x][y] = (self.pixels[x][y] + self.sample(x, y)) / samples

#http://blog.johnnovak.net/2016/04/30/the-nim-raytracer-project-part-2-the-basics/
    def sample(self, x, y):
        raster_x = float(x) + random.uniform(0.01, 0.99)
        raster_y = float(y) + random.uniform(0.01, 0.99)
        ndc_x = (raster_x * self.aspect) / self.res_x
        ndc_y = raster_y / self.res_y
        f = math.tan(self.camera.fov / 2)
        screen_x = (2 * ndc_x - self.aspect) * f
        screen_y = -(2 * ndc_y - 1) * f
        direction = (Vector3(x=screen_x, y=screen_y, z=-1.0)).normalized()
        D = self.camera.transform * direction
        ray = Raycast(origin=camera.pos, direction=d)
        point, object = self.octree.intersect(ray)

        color = self.bg_color
        if object is not None:
            N = object.get_normal(point)
            R = D - (2 * (D ** N)) * N
            count = 0
            color = Vector3() * 0
            for light in self.scene_description.lights:
                L = Raycast(origin=point, direction=(light.pos - point).normalized)
                if L ** N < 0:
                    continue
                else:
                    light_count += 1
                shadow_point, shadow_object = self.octree.intersect(point)
                if shadow_object is None:
                    color += object.material.shade(D, N, R, L, light) / count
            if count == 0:
                color = self.bg_color
        return color

    def write(self):
        filename, ext = os.path.splitext(self.outfile)
        print("writing to ", filename, ext, "extension: ", ext)
        if ext == ".ppm":
            with open(self.outfile, 'w') as f:
                f.write("P3\n{0} {1}\n255\n".format(self.res_y, self.res_x))
                for row in self.pixels:
                    for pixel in row:
                        pixel_ppm = pixel * 255.99
                        f.write("{0} {1} {2}\n".format(int(pixel_ppm.x), int(pixel_ppm.y), int(pixel_ppm.z)))
        else:
            print("Functionality only for PPM files.")
