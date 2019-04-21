import os
import random
import scenedescription, raytracer

class Raytracer():
    def __init__(self, res_x, res_y, camera, bg_color, scenefile="example.json", outfile="example.ppm"):
        self.res_x = res_x
        self.res_y = res_y
        self.aspect = float(res_x) / float(res_y)
        self.camera = camera
        self.bg_color = bg_color
        self.scene_description = SceneDescription()
        self.scene_description.import_from_file(scenefile)
        self.outfile = outfile
        self.pixels = [[Vector3() for i in range(res_x)] for j in range(res_y)]

    def trace(self, samples=1):
        self.octree = self.scene_description.flatten_to_octree(self.camera)
        for i in samples:
            for x in range(self.res_x):
                for y in range(self.res_y):
                    print "({0}, {1}) {2} samples".format(x, y, i)
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
        direction = (Vector3(x=screen_x, y=screen_y, -1.0)).normalized()
        D = self.camera.transform * direction
        ray = Ray(origin=camera.pos, direction=d)
        point, object = self.octree.intersect(ray)

        color = self.bg_color
        if object is not None:
            N = object.get_normal(point)
            R = D - (2 * (D ** N)) * N
            count = 0
            color = Vector3() * 0
            for light in self.scene_description.lights:
                L = Ray(origin=point, direction=(light.pos - point).normalized)
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
        filename, ext = os.path.splittext(self.outfile)
        with open(self.outfile, 'w') as f:
            if ext == "ppm":
                f.write("P3\n{0} {1}\n".format(self.res_x, self.res_y))
                for row in self.pixels():
                    for pixel in row:
                        pixel_ppm = pixel * 255.99
                        f.write("{0}\n".format(pixel_ppm))
            else:
                print "Functionality only for PPM files."
