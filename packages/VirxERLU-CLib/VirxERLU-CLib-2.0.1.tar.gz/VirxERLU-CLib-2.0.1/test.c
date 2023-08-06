#include <math.h>
#include <stdio.h>
#include <time.h>
#include <Python.h>

// Constants

static const double simulation_dt = 1. / 60.;

static const double max_speed = 2300.;
static const double max_speed_no_boost = 1410.;

static const char one = 1;
static const char neg_one = -1;

// simple math stuff

static inline double cap(double value, double min_v, double max_v)
{
    return max(min(value, max_v), min_v);
}

static inline signed char sign(int value)
{
    return (value > 0) - (value < 0);
}

// Vector stuff

typedef struct vector
{
    double x;
    double y;
    double z;
} Vector;

typedef struct vec
{
    double x;
    double y;
} Vec;

static inline Vec flat_add(Vec vec1, Vec vec2)
{
    return (Vec){vec1.x + vec2.x, vec1.y + vec2.y};
}

static inline Vec flat_sub(Vec vec1, Vec vec2)
{
    return (Vec){vec1.x - vec2.x, vec1.y - vec2.y};
}

static inline Vec flat_multiply_d(Vec vec1, double factor)
{
    return (Vec){vec1.x * factor, vec1.y * factor};
}

static inline double dot(Vector vec1, Vector vec2)
{
    return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z;
}

static inline double flat_dot(Vec vec1, Vec vec2)
{
    return vec1.x * vec2.x + vec1.y * vec2.y;
}

static inline double magnitude(Vector vec)
{
    return sqrt(dot(vec, vec));
}

static inline double flat_magnitude(Vec vec)
{
    return sqrt(flat_dot(vec, vec));
}

static inline Vector cross(Vector vec1, Vector vec2)
{
    return (Vector){(vec1.y * vec2.z) - (vec1.z * vec2.y), (vec1.z * vec2.x) - (vec1.x * vec2.z), (vec1.x * vec2.y) - (vec1.y * vec2.x)};
}

static inline Vector flat_cross(Vec vec1, Vec vec2)
{
    return (Vector){vec1.y - vec2.y, vec2.x - vec1.x, (vec1.x * vec2.y) - (vec1.y * vec2.x)};
}

static inline Vec flat_cross_2d_z(Vec vec1, char z)
{
    return (Vec){vec1.y * z, -vec1.x * z};
}

static inline double flat_dist(Vec vec1, Vec vec2)
{
    return flat_magnitude(flat_sub(vec1, vec2));
}

static inline Vec flat_rotate(Vec vec, double angle)
{
    return (Vec){cos(angle) * vec.x - sin(angle) * vec.y, sin(angle) * vec.x + cos(angle) * vec.y};
}

Vec flat_normalize(Vec vec)
{
    double mag = flat_magnitude(vec);

    if (mag != 0)
        return (Vec){vec.x / mag, vec.y / mag};

    return (Vec){0, 0};
}

static inline double flat_angle(Vec vec1, Vec vec2)
{
    return acos(cap(flat_dot(flat_normalize(vec1), flat_normalize(vec2)), -1, 1));
}

static inline Vec flat_scale(Vec vec, double value)
{
    return flat_multiply_d(flat_normalize(vec), value);
}

// changed flat_cross_2d_z

// intersection point = origin + direction * t1
double ray_intersects_with_line(Vec origin, Vec direction, Vec p1, Vec p2)
{
    const Vec v1 = flat_sub(origin, p1);
    const Vec v2 = flat_sub(p2, p1);
    const Vec v3 = (Vec){-direction.y, direction.x};
    const double v_dot = flat_dot(v2, v3);

    const double t1 = magnitude(flat_cross(v2, v1)) / v_dot;

    if (t1 < 0)
        return -1;

    const double t2 = flat_dot(v1, v3) / v_dot;

    if (0 <= t1 && t2 <= 1)
        return t1;

    return -1;
}

double get_travel_distance(Vec ball_location, Vec offset_ball_location, Vec car_location, Vec shot_vector)
{
    const Vec car_to_ball = flat_sub(ball_location, car_location);
    const char side_of_shot = sign((int)flat_dot(flat_cross_2d_z(shot_vector, one), car_to_ball));
    const Vec ray_direction = flat_rotate(flat_multiply_d(shot_vector, -1), side_of_shot * -1.3);
    const Vec car_to_offset_perp = flat_cross_2d_z(flat_sub(offset_ball_location, car_location), side_of_shot);
    const Vec final_target = flat_scale(car_to_offset_perp, 2560);
    const double distance_from_turn = ray_intersects_with_line(ball_location, ray_direction, car_location, final_target);

    if (distance_from_turn == -1)
        return -1;

    const Vec car_turn_point = flat_add(ball_location, flat_multiply_d(ray_direction, distance_from_turn));
    return flat_dist(car_location, car_turn_point) + flat_dist(car_turn_point, final_target);
}

// stuff

static PyObject *method_test(PyObject *self, PyObject *args)
{
    double ball_radius;

    if (!PyArg_ParseTuple(args, "d", &ball_radius))
        return NULL;

    const Vec ball_location = (Vec){0, 0};
    const Vec shot_vector = (Vec){0, -1};
    const Vec offset_ball_location = flat_sub(ball_location, flat_multiply_d(shot_vector, ball_radius + (40 * 1.25)));

    const Vec car_location = (Vec){5120, -2560};

    clock_t start, end;
    double dist = 0;

    start = clock();
    
    for (long i = 0; i < 3600000; i++)
    {
        dist += get_travel_distance(ball_location, offset_ball_location, car_location, shot_vector);
    }

    end = clock();

    printf("%f\n", dist);
    double time_taken = (double)(end - start) / (double)(CLOCKS_PER_SEC);
    const double travel_distance = get_travel_distance(ball_location, offset_ball_location, car_location, shot_vector);

    return Py_BuildValue("dd", time_taken, travel_distance);
}

static PyMethodDef methods[] = {
    {"test", method_test, METH_VARARGS, "test"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "ctest",
    "C tests",
    -1,
    methods};

PyMODINIT_FUNC PyInit_ctest(void)
{
    return PyModule_Create(&module);
}
