import numpy as np
import matplotlib.pyplot as plt

def plotShipStates(states, tVec, Ts, beta):
    # Global position states x, y, z
    plt.subplot(4, 3, 1)
    plt.plot(tVec * Ts, states[0, :])
    plt.title('Global CoG position X [m]')
    plt.xlabel('Time [s]')

    plt.subplot(4, 3, 2)
    plt.plot(tVec * Ts, states[1, :])
    plt.title('Global CoG position Y [m]')
    plt.xlabel('Time [s]')

    plt.subplot(4, 3, 3)
    plt.plot(tVec * Ts, -states[2, :])
    plt.title('Global CoG position Z (UP) [m]')
    plt.xlabel('Time [s]')

    # Local velocity states u, v, w
    plt.subplot(4, 3, 4)
    plt.plot(tVec * Ts, (states[3, :] / Ts).T)
    plt.title('Local velocity U [m/s]')
    plt.xlabel('Time [s]')

    plt.subplot(4, 3, 5)
    plt.plot(tVec * Ts, (states[4, :] / Ts).T)
    plt.title('Local velocity V [m/s]')
    plt.xlabel('Time [s]')

    plt.subplot(4, 3, 6)
    plt.plot(tVec * Ts, (-states[5, :] / Ts).T)
    plt.title('Local velocity W (UP) [m/s]')
    plt.xlabel('Time [s]')

    # Local angles phi, th, psi
    plt.subplot(4, 3, 7)
    plt.plot(tVec * Ts, np.rad2deg(states[6, :]))
    plt.title('Roll $\phi$ [deg]')
    plt.xlabel('Time [s]')

    plt.subplot(4, 3, 8)
    plt.plot(tVec * Ts, np.rad2deg(states[7, :]))
    plt.title('Pitch $\dot{\Theta}$ [deg]')
    plt.xlabel('Time [s]')

    plt.subplot(4, 3, 9)
    plt.plot(tVec * Ts, np.rad2deg(states[8, :]))
    plt.title('Yaw $\psi$ [deg]')
    plt.xlabel('Time [s]')

    # Local rotational velocities w_phi, w_th, w_psi
    plt.subplot(4, 3, 10)
    plt.plot(tVec * Ts, (np.rad2deg(states[9, :]) / Ts).T)
    plt.title('Roll velocity w_$\phi$ [deg/s]')
    plt.xlabel('Time [s]')

    plt.subplot(4, 3, 11)
    plt.plot(tVec * Ts, (np.rad2deg(states[10, :]) / Ts).T)
    plt.title('Pitch velocity w_$\dot{\Theta}$ [deg/s]')
    plt.xlabel('Time [s]')

    plt.subplot(4, 3, 12)
    plt.plot(tVec * Ts, (np.rad2deg(states[11, :]) / Ts).T)
    plt.title('Yaw velocity w_$\psi$ [deg/s]')
    plt.xlabel('Time [s]')

    plt.tight_layout()
    plt.suptitle('Long crested from ' + str(np.rad2deg(beta)) + ' degrees')
    plt.show()

import scipy.io as sio
import os
plotFile =    f'{os.getcwd()}/plotStruct.mat'
plotData = sio.loadmat(plotFile)
states = plotData['states']
tVec = plotData['tVec'].T
Ts = plotData['Ts']
beta = plotData['beta']
plotShipStates(states, tVec, Ts, beta)