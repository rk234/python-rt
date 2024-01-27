from math_utils import Vec3
from rendering import render_scene, Camera
from scene import Scene, Sphere


WIDTH = 256
HEIGHT = 256

scene = Scene()
scene.add_object(Sphere(Vec3(0,0,5), 2))

cam = Camera(Vec3(0,0,0), Vec3(0,0,1), 1.0, Vec3(WIDTH, HEIGHT, 0))
out = render_scene(scene, WIDTH, HEIGHT, cam, 10)

out.save("out.png")