from typing import Self
import math

class Vec3():
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y 
        self.z = z

    def add(self, other: Self) -> Self:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def subtract(self, other: Self) -> Self:
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def multiply(self, other: Self) -> Self:
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
    
    def dot(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, b: Self) -> Self:
        return Vec3(
			self.y * b.z - self.z * b.y, 
	        self.z * b.x - self.x * b.z, 
	        self.x * b.y - self.y * b.x 
		)

    def magnitude(self) -> float:
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z);

    def scale(self, scalar: float) -> Self:
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def normalize(self) -> Self:
        return self.scale(1/self.normalize())
    
    def __str__(self) -> str:
        return f"Vec3({self.x}, {self.y}, {self.z})"
    
