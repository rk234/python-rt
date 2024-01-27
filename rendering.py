from math_utils import Vec3, rand_float
from PIL import Image


class Ray:
    origin: Vec3
    dir: Vec3

    def __init__(self, origin: Vec3, dir: Vec3) -> None:
        self.origin = origin
        self.dir = dir.normalize()

    def at(self, t: float) -> Vec3:
        return self.origin.add(self.dir.scale(t))


from scene import Scene


class Camera:
    pos: Vec3
    dir: Vec3
    near_plane: float  # near plane distance
    viewport_size: Vec3  # size of the viewport

    def __init__(self, pos: Vec3, dir: Vec3, near_plane: float, viewport_size: Vec3) -> None:
        self.pos = pos
        self.dir = dir
        self.near_plane = near_plane
        self.viewport_size = viewport_size

    def update_viewport(self, screen_width: float, screen_height: float):
        self.viewport_size = Vec3(
            (screen_width / screen_height) * 1.5,
            1.5,
            0,
        )

    def gen_primary_ray(self, screen_x: float, screen_y: float, screen_width: float, screen_height: float):
        adjacent = Vec3(0, 1, 0).cross(self.dir).normalize()
        local_up = adjacent.cross(self.dir).normalize()
        bottom_left = adjacent.scale(-self.viewport_size.x / 2).add(local_up.scale(-self.viewport_size.y / 2))
        ray_dir = bottom_left.add(
            adjacent.scale(self.viewport_size.x) * ((screen_x + rand_float(-0.5, 0.5)) / screen_width)).add(
            local_up.scale((self.viewport_size.y) * ((screen_y + rand_float(-0.5, 0.5)) / screen_height))).add(
            self.dir.scale(self.near_plane)).normalize()

        return Ray(self.pos, ray_dir)


def render_scene(scene: Scene, img_width: int, img_height: int, camera: Camera, samples: int) -> Image:
    out_img = Image.new(mode="RGB", size=(img_width, img_height))
    accumulation_buffer = [Vec3(0, 0, 0)] * (img_height * img_width)

    for s in range(samples):
        print(f"Sample {s + 1}/{samples}...", end="")
        for x in range(img_width):
            for y in range(img_height):
                camera.update_viewport(img_width, img_height)
                ray = camera.gen_primary_ray(x, y, img_width, img_height)
                hit = scene.intersect(ray)

                if hit is not None:
                    accumulation_buffer[x + y * img_width] = accumulation_buffer[x + y * img_width].add(
                        (hit.normal + Vec3(1, 1, 1)).scale(0.5))
                else:
                    accumulation_buffer[x + y * img_width] = accumulation_buffer[x + y * img_width].add(sky_color(ray))
        print("Done!")

    for x in range(img_width):
        for y in range(img_height):
            out_img.putpixel((x, y), vec_to_rgb(accumulation_buffer[x + y * img_width].scale(1 / samples)))

    return out_img


def vec_to_rgb(vec: Vec3) -> (int, int, int):
    return (
        int(vec.x * 255),
        int(vec.y * 255),
        int(vec.z * 255)
    )


def sky_color(ray: Ray) -> Vec3:
    t = 0.5 * (ray.dir.y + 1.0)
    return Vec3(
        (1.0 - t) + (t * 138 / 255),
        (1.0 - t) + (t * 188 / 255),
        1.0,
    )
