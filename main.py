from math_utils import Vec3
from rendering import render_scene, Camera
from PIL import Image

WIDTH = 600
HEIGHT = 400

cam = Camera(Vec3(0,0,0), Vec3(0,0,1), 1.0, Vec3(WIDTH, HEIGHT, 0))
out = render_scene(WIDTH, HEIGHT, cam, 10)

out.save("out.png")