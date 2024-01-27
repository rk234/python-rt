from math_utils import Ray, Vec3, rand_vec_in_unit_hemisphere, rand_vec_in_unit_sphere
from typing import Optional

EPSILON = 0.0001

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
        return Ray(hit_position + normal.scale(EPSILON), normal + rand_vec_in_unit_hemisphere(normal))

    def attenuation(self) -> Vec3:
        return self.albedo

class EmissiveMaterial(Material):
    emit: Vec3

    def __init__(self, emit: Vec3):
        self.emit = emit

    def emissive(self) -> bool:
        return True

    def scatter(self, in_ray: Ray, normal: Vec3, hit_position: Vec3) -> Optional[Ray]:
        return None

    def attenuation(self) -> Vec3:
        return self.emit


class MetalMaterial(Material):
    albedo: Vec3
    roughness: float

    def __init__(self, albedo: Vec3, roughness: float):
        self.albedo = albedo
        self.roughness = roughness

    def emissive(self) -> bool:
        return False

    def scatter(self, in_ray: Ray, normal: Vec3, hit_position: Vec3) -> Optional[Ray]:
        return Ray(
            hit_position + normal.scale(EPSILON),
            in_ray.dir.reflect(normal) + rand_vec_in_unit_sphere().scale(self.roughness)
        )

    def attenuation(self) -> Vec3:
        return self.albedo

