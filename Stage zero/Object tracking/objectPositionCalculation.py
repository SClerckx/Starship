import scipy as sp
import numpy as np
import random

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

class Camera():
    def __init__(self, position, orientation, error) -> None:
        self.pos = position
        self.orient = orientation
        self.ang_res = 0.1
        self.process_box(error)

    def process_box(self, error):
        #Currently dummy
        vecToObservation = starshipPos - self.pos + error
        self.vecToObservation = vecToObservation/(np.linalg.norm(vecToObservation))

    def get_line(self, t):
        point = self.pos + t*self.vecToObservation
        print(point)
        return point

starshipPos = np.array([[0], [0], [-0.2]])
cam1 = Camera(np.array([[1], [0], [0.5]]), np.array([[-1],[0],[0]]), np.array([[0],[0],[0]]))
cam2 = Camera(np.array([[0],[-1],[0.5]]), np.array([[0],[-1],[0]]), np.array([[0],[0],[0]]))

A = np.hstack((cam1.vecToObservation, -cam2.vecToObservation))
B = cam2.pos - cam1.pos

print(A)
print(B)

x = np.linalg.lstsq(A,B)[0]

solution = (cam1.get_line(x[0][0]) + cam2.get_line(x[1][0]))/2

print(solution)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(cam1.pos[0][0], cam1.pos[1][0], cam1.pos[2][0], label = "cam1")
ax.scatter(cam2.pos[0][0], cam2.pos[1][0], cam2.pos[2][0], label = "cam2")
ax.scatter(starshipPos[0][0], starshipPos[1][0], starshipPos[2][0], label = "starship")

t1 = 2
ax.plot([cam1.pos[0][0], cam1.get_line(t1)[0][0]], [cam1.pos[1][0], cam1.get_line(t1)[1][0]], [cam1.pos[2][0], cam1.get_line(t1)[2][0]], label = "cam1Line")
ax.plot([cam2.pos[0][0], cam2.get_line(t1)[0][0]], [cam2.pos[1][0], cam2.get_line(t1)[1][0]], [cam2.pos[2][0], cam2.get_line(t1)[2][0]], label = "cam2Line")

ax.scatter(cam1.get_line(x[0][0])[0][0], cam1.get_line(x[0][0])[1][0], cam1.get_line(x[0][0])[2][0], label = "Cam1Sol")
ax.scatter(cam2.get_line(x[0][0])[0][0], cam2.get_line(x[0][0])[1][0], cam2.get_line(x[0][0])[2][0], label = "Cam2Sol")

plt.legend()
plt.show()









