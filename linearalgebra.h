#ifndef LINEARALGEBRA_H
#define LINEARALGEBRA_H

class Float3 {
  public:
    float x, y, z;
    Float3() : Float3(1.0) {}
    Float3(float scalar) : Float3(scalar, scalar, scalar) {}
    Float3(float X, float Y, float Z): x(X), y(Y), z(Z) {}
    float magnitude() {}
    Float3 normalized() {}
    Float3 operator +(Float3 other) {}
    void operator +=(Float3 o) {}
    Float3 operator +(float scalar) {}
    void operator +=(float scalar) {}
    Float3 operator -(Float3 other) {}
    void operator -=(Float3 other) {}
    Float3 operator -(float scalar) {}
    void operator -=(float scalar) {}
    Float3 operator *(Float3 other) {}
    void operator *=(Float3 other) {}
    Float3 operator *(float scalar) {}
    void operator *=(float scalar) {}
    Float3 operator %(Float3 other) {}
    void operator %=(Float3 other) {}
    float operator ^(Float3 other) {}
    float operator [](int index) {}
  };

class Matrix3 {
  private:
    Float3 _rows[3];
    Float3 _cols[3];
  public:
    Matrix3() {}
    Matrix3(Float3 vectors[3]): Matrix3(vectors, true) {}
    Matrix3(Float3 vectors[3], bool rows) {}
    void get_col(int i) {}
    void set_col(int i, Float3 vector) {}
    void get_row(int i) {}
    void set_row(int i) {}
    void get_cell(int x, int y) {}
    void set_cell(int x, int y, float value) {}
    Matrix3 operator *(Matrix3 other) {}
    Float3 operator *(Float3 vector) {}
};

#endif
