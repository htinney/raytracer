#ifndef RAYTRACER_H
#define RAYTRACER_H

using namespace std;

#define RES_X 500
#define RES_Y 500
#define ASPECT RES_X / RES_Y
#define SAMPLES 1

#include "linearalgebra.h"
#include <string>

class Raytracer {
  private:
    Float3 bg_color;
    //SceneDescription scene_description;
    string outfile;
    Float3 pixels[RES_X][RES_Y];
  public:
    Raytracer(): Raytracer(Float3(), "example.ppm") {}
    Raytracer(Float3 BG_COLOR, string OUTFILE):
              bg_color(BG_COLOR), outfile(OUTFILE) {}
    //void gradient_fill(Float3 x_color1, Float3 x_color2, Float3 y_color1, Float3 y_color2) {}
    //void write() {}
    string get_outfile() {
      return outfile;
    }
};

#endif
