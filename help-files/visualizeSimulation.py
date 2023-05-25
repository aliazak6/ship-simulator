from R import R
from mayavi import mlab
import numpy as np

def visualizeSimulation(states, waves, xVec, yVec, tVec, faces, vertices, cogVec):
    # Create a figure
    mlab.figure()
    vertices = np.array(vertices, dtype=np.float64)
    faces = np.array(faces, dtype=np.int32) -1
    xVec, yVec = np.meshgrid(xVec, yVec)
    ## Create the ship mesh
    p = mlab.triangular_mesh(vertices[:, 0], vertices[:, 1], vertices[:, 2], faces,
                             color=(0.8, 0.8, 1.0), representation='surface')
    
    # Set the material properties
    p.actor.property.specular = 0.0
    p.actor.property.specular_power = 5

    # Create the sea surface
    sea = mlab.mesh(xVec, yVec, waves[:, :, 0])

    # Set the axes limits and labels
    mlab.axes(xlabel='x [m]', ylabel='y [m]', zlabel='z [m]',
              ranges=[5, 300, 0, 100, -10, 35])

    # Set the camera view
    mlab.view(60, 21)

    # Initialize deltas
    deltaX = 0
    deltaY = 0
    deltaZ = 0
    @mlab.animate(delay=10)
    def anim(deltaX,deltaY,deltaZ):
        for t in range(1, len(tVec[0])-1):
            # Update the sea surface
            sea.mlab_source.set(z=waves[:, :, t])
            # Update the ship position and orientation
            deltaX += states[0, t] - states[0, t - 1]
            deltaY += states[1, t] - states[1, t - 1]
            deltaZ += states[2, t] - states[2, t - 1]
            rotation_matrix = R(states[6, t], -states[7, t], -states[8, t])
            transformed_vertices = np.dot(rotation_matrix.T, (vertices - cogVec[t, :]).T).T
            transformed_vertices += cogVec[t, :] + np.array([deltaX, -deltaY, -deltaZ])
            p.mlab_source.set(x=transformed_vertices[:, 0], y=transformed_vertices[:, 1],
                            z=transformed_vertices[:, 2])
            #print(f'x: {transformed_vertices[:, 0]}')
            # Update the figure
            #mlab.draw()
            yield
    anim(deltaX,deltaY,deltaZ) 
    # Keep the visualization window open
    mlab.show()

import scipy.io as sio
import os
visualFile =    f'{os.getcwd()}/simulation-results/Simulation_6_Result_visualizeStruct.mat'
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
