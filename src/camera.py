from typing import Optional
from math_utils import Vec3, rand_float, Ray


class Camera:
    pos: Vec3
    dir: Vec3
    near_plane: float  # near plane distance
    viewport_size: Vec3  # size of the viewport
    cached_ray_directions: list[Optional[Vec3]]

    def __init__(self, pos: Vec3, dir: Vec3, near_plane: float, viewport_size: Vec3) -> None:
        self.pos = pos
        self.dir = dir
        self.near_plane = near_plane
        self.viewport_size = viewport_size

    def update_viewport(self, screen_width: float, screen_height: float):
        self.cached_ray_directions = [None] * int(screen_width * screen_height)
        self.viewport_size = Vec3(
            (screen_width / screen_height) * 1.5,
            1.5,
            0,
        )

    def gen_primary_ray(self, screen_x: float, screen_y: float, screen_width: float, screen_height: float):
        adjacent = Vec3(0, 1, 0).cross(self.dir).normalize()
        local_up = adjacent.cross(self.dir).normalize()
        bottom_left = adjacent.scale(-self.viewport_size.x / 2).add(local_up.scale(-self.viewport_size.y / 2))
        """
        ray_dir = bottom_left.add(
            adjacent.scale(self.viewport_size.x) * ((screen_x + rand_float(-0.5, 0.5)) / screen_width)).add(
            local_up.scale((self.viewport_size.y) * ((screen_y + rand_float(-0.5, 0.5)) / screen_height))).add(
            self.dir.scale(self.near_plane)).normalize()
        """
        i = int(screen_x + screen_width * screen_y)
        ray_dir = None
        if self.cached_ray_directions[i] is None:
            ray_dir = bottom_left.add(
                adjacent.scale(self.viewport_size.x * (screen_x / screen_width))).add(
                local_up.scale(self.viewport_size.y * (screen_y / screen_height))).add(
                self.dir.scale(self.near_plane)).normalize()
            self.cached_ray_directions[i] = ray_dir

        ray_dir = self.cached_ray_directions[i].add(adjacent.scale(rand_float(-0.5, 0.5) / screen_width)).add(
            local_up.scale(rand_float(-0.5, 0.5) / screen_height)).normalize()

        return Ray(self.pos, ray_dir)
