import math

from math_utils import Vec3, Ray
from PIL import Image
from scene import Scene
from camera import Camera


def render_scene(scene: Scene, img_width: int, img_height: int, camera: Camera, samples: int,
                 num_bounces: int = 3) -> Image:
    out_img = Image.new(mode="RGB", size=(img_width, img_height))
    accumulation_buffer = [Vec3(0, 0, 0)] * (img_height * img_width)
    camera.update_viewport(img_width, img_height)

    for s in range(samples):
        print(f"Sample {s + 1}/{samples}...", end="")
        for x in range(img_width):
            for y in range(img_height):
                ray = camera.gen_primary_ray(x, y, img_width, img_height)
                accumulation_buffer[x + y * img_width] = accumulation_buffer[x + y * img_width].add(
                    cast(scene, ray, num_bounces))
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

        if mat.emissive():
            return mat.attenuation()
        else:
            return mat.attenuation().multiply(cast(scene, mat.scatter(ray, normal, p), depth - 1))
    else:
        return sky_color(ray)


def vec_to_rgb(vec: Vec3) -> (int, int, int):
    return (
        int(math.sqrt(vec.x) * 255),
        int(math.sqrt(vec.y) * 255),
        int(math.sqrt(vec.z) * 255)
    )


def sky_color(ray: Ray) -> Vec3:
    t = 0.5 * (ray.dir.y + 1.0)
    return Vec3(
        (1.0 - t) + (t * 138 / 255),
        (1.0 - t) + (t * 188 / 255),
        1.0,
    )
