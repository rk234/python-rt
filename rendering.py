from math_utils import Vec3, rand_float, Ray
from PIL import Image
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


def render_scene(scene: Scene, img_width: int, img_height: int, camera: Camera, samples: int, num_bounces: int = 4) -> Image:
    out_img = Image.new(mode="RGB", size=(img_width, img_height))
    accumulation_buffer = [Vec3(0, 0, 0)] * (img_height * img_width)

    for s in range(samples):
        print(f"Sample {s + 1}/{samples}...", end="")
        for x in range(img_width):
            for y in range(img_height):
                camera.update_viewport(img_width, img_height)
                ray = camera.gen_primary_ray(x, y, img_width, img_height)
                accumulation_buffer[x + y * img_width] = accumulation_buffer[x + y * img_width].add(cast(scene, ray, num_bounces))
        print("Done!")

    for x in range(img_width):
        for y in range(img_height):
            out_img.putpixel((x, y), vec_to_rgb(accumulation_buffer[x + y * img_width].scale(1 / samples)))

    return out_img


def cast(scene: Scene, ray: Ray, depth: int) -> Vec3:
    if depth < 0:
        return Vec3(0, 0, 0)

    hit = scene.intersect(ray)
    if hit is not None:
        p = hit.pos
        mat = hit.material
        normal = hit.normal

        return mat.attenuation().multiply(cast(scene, mat.scatter(ray, normal, p), depth-1))
    else:
        return sky_color(ray)

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
