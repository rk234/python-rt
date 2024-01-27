from typing import Self
import math
import random

class Vec3:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def add(self, other: Self) -> Self:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __add__(self, other: Self) -> Self:
        return self.add(other)

    def subtract(self, other: Self) -> Self:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __sub__(self, other: Self) -> Self:
        return self.subtract(other)

    def multiply(self, other: Self) -> Self:
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def dot(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __mul__(self, scalar: float) -> Self:
        return self.scale(scalar)

    def cross(self, b: Self) -> Self:
        return Vec3(
            self.y * b.z - self.z * b.y,
            self.z * b.x - self.x * b.z,
            self.x * b.y - self.y * b.x
        )

    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def scale(self, scalar: float) -> Self:
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def normalize(self) -> Self:
        return self.scale(1 / self.magnitude())

    def distance(self, other: Self) -> float:
        return self.subtract(other).magnitude()

    def __str__(self) -> str:
        return f"Vec3({self.x}, {self.y}, {self.z})"


def rand_float(lower_bound: float, upper_bound: float) -> float:
    return lower_bound + (random.random() * (upper_bound - lower_bound))


def rand_vec() -> Vec3:
    return Vec3(rand_float(-1, 1), rand_float(-1, 1), rand_float(-1, 1))


def rand_vec_in_unit_sphere() -> Vec3:
    vec = rand_vec()

    while vec.magnitude() > 1:
        vec = rand_vec()

    return vec.normalize()


def rand_vec_in_unit_hemisphere(normal: Vec3) -> Vec3:
    vec = rand_vec_in_unit_sphere()

    if vec.dot(normal) > 0:
        return vec
    else:
        return vec.scale(-1)


class Ray:
    origin: Vec3
    dir: Vec3

    def __init__(self, origin: Vec3, direction: Vec3) -> None:
        self.origin = origin
        self.dir = direction.normalize()

    def at(self, t: float) -> Vec3:
        return self.origin.add(self.dir.scale(t))
