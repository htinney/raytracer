#include "linearalgebra.h"
#include<stdio.h>
#include<cmath>

float Float3::magnitude() {
  return sqrt((*this)^(*this));
}
Float3 Float3::normalized() {
  return (*this) / magnitude();
}
Float3 Float3::operator +(Float3 other) {
  return Float3(x+other.x, y+other.y, z+other.z);
}
void Float3::operator +=(Float3 other) {
  x += other.x;
  y += other.y;
  z += other.z;
  return;
}
Float3 Float3::operator +(float scalar) {
  return Float3(x+scalar, y+scalar, z+scalar);
}
void Float3::operator +=(float scalar) {
  x += scalar;
  y += scalar;
  z += scalar;
  return;
}
Float3 Float3::operator -(Float3 other) {
  return Float3(x-other.x, y-other.y, z-other.z);
}
void Float3::operator -=(Float3 other) {
  x -= other.x;
  y -= other.y;
  z -= other.z;
  return;
}
Float3 Float3::operator -(float scalar) {
  return Float3(x+scalar, y+scalar, z+scalar);
}
void Float3::operator -=(float scalar) {
  x -= scalar;
  y -= scalar;
  z -= scalar;
  return;
}
Float3 Float3::operator *(Float3 other) {
  return Float3(x*other.x, y*other.y, z*other.z);
}
void Float3::operator *=(Float3 other) {
  x *= other.x;
  y *= other.y;
  z *= other.z;
  return;
}
Float3 Float3::operator *(float scalar) {
  return Float3(x*scalar, y*scalar, z*scalar);
}
void Float3::operator *=(float scalar) {
  x *= scalar;
  y *= scalar;
  z *= scalar;
  return;
}
Float3 Float3::operator %(Float3 other) {
  return Float3(y*other.z - z*other.y,
                x*other.z - z*other.x,
                x*other.y - y*other.x);
}
void Float3::operator %=(Float3 other) {
  x = y*other.z - z*other.y;
  y = x*other.z - z*other.x;
  z = x*other.y - y*other.x;
  return;
}
float Float3::operator ^(Float3 other) {
  return x * other.x + y * other.y + z * other.z;
}
float Float3::operator [](int index) {
  switch(index) {
    case 0:
      return x;
      break;
    case 1:
      return y;
      break;
    case 2:
      return z:
      break;
    default:
      return -1.0;
      break;
  }
}

Matrix3::Matrix3() {
      Float vectors[3] = {
        Float3(1.0, 0.0, 0.0), Float3(0.0, 1.0, 0.0), Float3(0.0, 0.0, 1.0)
      };
      _rows = vectors;
      _cols = vectors;
    }

Matrix3::Matrix3(Float3 vectors[3], bool rows) {
  if (rows) {
    _rows = vectors;
  } else {
    _cols = vectors;
  }
  for (int i = 0; i < 3; i++) {
    if (rows) {
      _cols[i] = Float3(vectors[0][i], vectors[1][i], vectors[2][i]);
    } else {
      _rows[i] = Float3(vectors[0][i], vectors[1][i], vectors[2][i]);
    }
  }
}

void Matrix3::get_col(int i) {
  return _cols[i];
}

void Matrix3::set_col(int i, Float3 vector) {
  _cols[i] = vector;
  for (int j = 0; j < 3; j++) {
    _rows[j][i] = vector[j];
  }
  return;
}

void Matrix3::get_row(int i) {
  return _rows[i];
}

void Matrix3::set_row(int i) {
  _rows[i] = vector;
  for (int j = 0; j < 3; j++) {
    _cols[j][i] = vector[j];
  }
  return;
}

void Matrix3::get_cell(int x, int y) {
  return _rows[x][y];
}

void Matrix3::set_cell(int x, int y, float value) {
  _rows[x][y] = value;
  _cols[y][x] = value;
}

Matrix3 Matrix3::operator *(Matrix3 other) {
  Matrix3 result = Matrix3();
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      result.set_cell[i][j] = get_row(i)^get_col(j);
    }
  }
}

Float3 Matrix3::operator *(Float3 vector) {
  return Float3(get_row(0)^vector,
                get_row(1)^vector,
                get_row(2)^vector);
}
