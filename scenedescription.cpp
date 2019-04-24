class Ray {
  public:
    Float3 origin, direction;
    float distance;
    Ray(Float3 o, Float3 dest) {
      origin = o;
      vector = (dest - o);
      direction = (vector).normalized();
      distance = (vector).magnitude();
    }
    Ray(Float3 o, Float3 dir, Float3 dist):
      origin(o), direction(dir), distance(dist) {}
};

class Hit {
  public:
    Float3 pos, V, N, R;
    Hit(): Hit(Float3(), Float3(), Float3()) {}
    Hit(Float3 p, Float3 v, Float3 n): pos(p), V(v), N(n) {
      R = (2 * (V^N))*N - V;
    }
    float vector_to(Float3 point) {
      return (pos - point).normalized();
    }
};

class Plane {
  public:
    Float3 normal;
    float distance;
    Plane(Float3 norm, float dist): normal(norm), distance(dist) {}
    Hit intersect(Ray ray) {
      return Hit();
    }
};

class BBOX {
  public:
    Float3 center, extent;
    Plane x_plane, y_plane, z_plane;
    BBOX(Float3 ctr, Float3 ext) {
      center = ctr;
      extent = ext;
      x_plane = Plane(Float3(0.0, 0.0, center.x));
      y_plane = Plane(Float3(0.0, 0.0, center.y));
      z_plane = Plane(Float3(0.0, 0.0, center.z));
    }
    bool contains(Float3 p_center, Float3 p_extent) {
      if (p_center.x + p_extent.x <= center.x + extent.x &&
          p_center.x - p_extent.x >= center.x - extent.x &&
          p_center.y + p_extent.y <= center.y + extent.y &&
          p_center.y - p_extent.y >= center.y - extent.y &&
          p_center.z + p_extent.z <= center.z + extent.z &&
          p_center.z - p_extent.z >= center.z - extent.z &&) {
        return true;
      }
    }
    bool intersect(Ray ray) {
      return false;
    }
};

class Material {
  public:
    Float3 d, s, a;
    float di, si, ai, g;
    Material(Float3 D, Float3 S, Float3 A,
             float Di, float Si, float Ai, float G):
             d(D), s(S), a(A), di(Di), si(Si), g(G) {}
    // li = light intensity, lc = light color
    Float3 shade(Hit h, Light light) {
      Float3 diffuse = (light.color * light.intensity) * (d * (h.N ^ h.vector_to(light.pos)));
      Float3 specular = (light.color * light.intensity) * (s * pow(h.V * h.R), g));
      Float3 ambient = a;
      return (diffuse * di) + (specular * di) + (ambient * ai);
    }
};

class SceneObject {
  protected:
    BBOX bound;
  public:
    BBOX get_bound() {
      return bound;
    }
};

class Sphere : public SceneObject {
  protected:
    Float3 center;
    float radius;

  public:
    Sphere(Float3 c, float r) {
      center = c;
      radius = r;
      bound = Float3(radius);
    }
    void set_center(Float3 c) {
      center = c;
    }

    Float3 get_center() {
      return center;
    }

    void set_radius(float radius) {
      radius = r;
      bound = Float3(radius);
    }

    float get_radius() {
      return radius;
    }

    Hit intersect(Ray ray) {
      return Hit();
    }
};
