from math_utils import Ray, Vec3, rand_vec_in_unit_hemisphere
from typing import Optional


class Material:
    def emissive(self) -> bool:
        pass

    def scatter(self, in_ray: Ray, normal: Vec3, hit_position: Vec3) -> Optional[Ray]:
        pass

    def attenuation(self) -> Vec3:
        pass


class DiffuseMaterial(Material):
    albedo: Vec3 # color

    def __init__(self, albedo: Vec3):
        self.albedo = albedo

    def emissive(self) -> bool:
        return False

    def scatter(self, in_ray: Ray, normal: Vec3, hit_position: Vec3) -> Optional[Ray]:
        return Ray(hit_position + normal.scale(0.0001), normal + rand_vec_in_unit_hemisphere(normal))

    def attenuation(self) -> Vec3:
        return self.albedo
