#include<string>
#include "raytracer.h"
#include "linearalgebra.h"
using namespace std;

void Raytracer::gradient_fill(Float3 x_color1, Float3 x_color2, Float3 y_color1, Float3 y_color2) {
  for(int i = 0; i < RES_X; i++) {
    for(int j = 0; j < RES_Y; j++) {
      float percent_x = i / ((float) RES_X);
      float percent_y = j / ((float) RES_Y);
      Float3 x_color = x_color1 * (1 - percent_x) + x_color2 * (percent_x);
      Float3 y_color = y_color1 * (1 - percent_y) + y_color2 * (percent_y);
      pixels[i][j] = x_color * 0.5 + y_color * 0.5;
    }
  }
}

void Raytracer::write() {
  ofstream outputfile;
  outputfile.open(outfile);
  outputfile << "P3\n" << RES_X << " " << RES_Y << "\n255\n";
  for(int i = 0; i < RES_X; i++) {
    for(int j = 0; j < RES_Y; j++) {
      outputfile << pixels[i][j].x << " " << pixels[i][j].y << " " << pixels[i][j].z + " ";
    }
    outputfile << "\n";
  }
  outputfile.close();
}

int main() {
  Raytracer raytracer = Raytracer();
  raytracer.gradient_fill(Float(1.0, 0.0, 0.0),
                          Float(0.5, 1.0, 0.0),
                          Float(0.0, 1.0, 0.0),
                          Float(0.0, 0.5, 1.0));
  raytracer.write();
  cout << "\nWrote results to " << raytracer.get_outfile();
}
