import numpy as np

def areaOfFace(x,y,z):
    # AREAOFFACE Calculates area of triangle given the coordinates of the 
    # points composing the triangle.

    x = np.array(x).T
    y = np.array(y).T
    z = np.array(z).T
    ons = np.array([1, 1, 1])
    A = 0.5 * np.sqrt(np.linalg.det([x, y, ons])**2 + np.linalg.det([y, z, ons])**2 + np.linalg.det([z, x, ons])**2)
    return A
