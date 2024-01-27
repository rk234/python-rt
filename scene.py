from math_utils import Vec3
from rendering import Ray
from typing import Optional
import math


class HitData:
    pos: Vec3
    normal: Vec3

    def __init__(self, pos: Vec3, normal: Vec3):
        self.pos = pos
        self.normal = normal


class SceneObject:
    def intersect(self, ray: Ray) -> Optional[HitData]:
        pass


class Scene:
    objects: list[SceneObject]

    def __init__(self):
        self.objects = []

    def add_object(self, obj: SceneObject):
        self.objects.append(obj)

    def intersect(self, ray: Ray) -> Optional[HitData]:
        min_dist = 10e9
        closest_hit: Optional[HitData] = None

        for obj in self.objects:
            hit: Optional[HitData] = obj.intersect(ray)
            if hit is not None:
                dist = hit.pos.distance(ray.origin)
                if dist < min_dist:
                    min_dist = dist
                    closest_hit = hit

        return closest_hit


class Sphere(SceneObject):
    position: Vec3
    radius: float

    def __init__(self, position: Vec3, radius: float):
        self.position = position
        self.radius = radius

    def intersect(self, ray: Ray) -> HitData | None:
        oc = ray.origin - self.position

        a = ray.dir.dot(ray.dir)
        b = 2 * oc.dot(ray.dir)
        c = oc.dot(oc) - (self.radius * self.radius)

        disc = b * b - 4 * a * c

        if disc >= 0:
            t0 = (-b + math.sqrt(disc)) / (2 * a)
            t1 = (-b - math.sqrt(disc)) / (2 * a)
            t = min(t0, t1)

            if t >= 0:
                p = ray.at(t)
                return HitData(p, (p - self.position).normalize())
            else:
                return None
        else:
            return None
