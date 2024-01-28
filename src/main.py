from materials import DiffuseMaterial, EmissiveMaterial, MetalMaterial
from math_utils import Vec3
from rendering import render_scene
from camera import Camera
from scene import Scene, Sphere


HEIGHT = 256
WIDTH = int(HEIGHT * (16 / 9))

scene = Scene()

white_diffuse = DiffuseMaterial(Vec3(0.8, 0.8, 0.8))
light = EmissiveMaterial(Vec3(255 / 70, 210 / 70, 74 / 70))
green_diffuse = DiffuseMaterial(Vec3(0.2, 0.8, 0.3))
metal = MetalMaterial(Vec3(1, 1, 1), 0.1)

scene.add_object(Sphere(Vec3(0, 2, 5), 2, green_diffuse))
scene.add_object(Sphere(Vec3(5, 2, 5), 2, light))
scene.add_object(Sphere(Vec3(-5, 2, 5), 2, metal))
scene.add_object(Sphere(Vec3(0, -1000, 5), 1000, white_diffuse))

cam = Camera(Vec3(0, 2, -3), Vec3(0, 0, 1), 1.0, Vec3(WIDTH, HEIGHT, 0))
out = render_scene(scene, WIDTH, HEIGHT, cam, 100)

out.save("out.png")
