from R import R
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.animation import FuncAnimation
import numpy as np

def update_plot(t, ax,sea,xVec, yVec, waves,patches,deltaX,deltaY,deltaZ,vertices,faces):
    ax.clear()
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_zlabel('z [m]')
    ax.view_init(60, 21)
    ax.set_xlim(5, 300)
    ax.set_ylim(0, 100)
    ax.set_zlim(-10, 35)
    sea = ax.plot_surface(xVec, yVec, waves[:, :, t], cmap='Blues', alpha=0.7)
    deltaX += states[0, t] - states[0, t - 1]
    deltaY += states[1, t] - states[1, t - 1]
    deltaZ += states[2, t] - states[2, t - 1]

    rotation_matrix = R(states[6, t], -states[7, t], -states[8, t])
    transformed_vertices = np.dot(rotation_matrix.T, (vertices - cogVec[t, :]).T).T
    transformed_vertices += cogVec[t, :] + np.array([deltaX, -deltaY, -deltaZ])

    #patches.set_verts([transformed_vertices[face] for face in faces])
    #ax.add_collection3d(patches)

def visualizeSimulation(states, waves, xVec, yVec, tVec, faces, vertices, cogVec):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    vertices = np.array(vertices, dtype=np.float64)
    faces = np.array(faces, dtype=np.int32) -1
    # Create the collection of 3D patches
    patches = art3d.Poly3DCollection([vertices[face] for face in faces], facecolors=(0.8, 0.8, 1.0), edgecolors='none')

    #Add the collection to the axes
    ax.add_collection3d(patches)
    

    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_zlabel('z [m]')
    ax.view_init(60, 21)
    ax.set_xlim(5, 300)
    ax.set_ylim(0, 100)
    ax.set_zlim(-10, 35)
    xVec, yVec = np.meshgrid(xVec, yVec)
    
    sea = ax.plot_surface(xVec, yVec, waves[:, :, 0], cmap='Blues', alpha=0.7)
    
    deltaX = 0
    deltaY = 0
    deltaZ = 0

    animate = FuncAnimation(fig, update_plot, len(tVec[0]-1), fargs=(ax,sea,xVec, yVec, waves,patches,
                                                                     deltaX,deltaY,deltaZ,
                                                                     vertices,faces), interval=10)
    plt.show()

import scipy.io as sio
import os
visualFile =    f'{os.getcwd()}/visualizeStruct.mat'
visualData = sio.loadmat(visualFile)

states = visualData['states']
waves = visualData['waves']
xVec = visualData['xVec']
yVec = visualData['yVec']
tVec = visualData['tVec']
faces = visualData['faces']
vertices = visualData['vertices']
cogVec = visualData['cogVec']

visualizeSimulation(states, waves, xVec, yVec, tVec, faces, vertices, cogVec)
