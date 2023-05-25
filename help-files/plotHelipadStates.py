import numpy as np
import matplotlib.pyplot as plt
from R import R

def plotHelipadStates(states, tVec, Ts, beta, helipadPos):
    # PLOTSHIPSTATES Plots the 12 states of the helipad through time vector tVec.

    fig = plt.figure(figsize=(12, 10))

    r = states[0:3, :] - helipadPos.reshape((-1, 1))

    globalHelipadPos = np.zeros_like(states[0:3, :])
    globalVel = np.zeros_like(states[0:3, :])

    for i in range(states.shape[1]):
        globalHelipadPos[:, i] = np.dot(R(states[6,i], states[7,i], states[8,i]), r[:, i])

        localVel = np.cross([states[9, i], states[10, i], states[11, i]], r[:, i]) + states[3:6, i]
        globalVel[:, i] = np.dot(R(states[6,i], states[7,i], states[8,i]), localVel)

    # Global position states x, y, z
    plt.subplot(4, 3, 1)
    plt.plot(tVec * Ts, globalHelipadPos[0, :])
    plt.title('Global Helipad position X [m]')
    plt.xlabel('Time [s]')
    plt.subplot(4, 3, 2)
    plt.plot(tVec * Ts, globalHelipadPos[1, :])
    plt.title('Global Helipad position Y [m]')
    plt.xlabel('Time [s]')
    plt.subplot(4, 3, 3)
    plt.plot(tVec * Ts, -globalHelipadPos[2, :])
    plt.title('Global Helipad position Z (UP)[m]')
    plt.xlabel('Time [s]')

    # Local velocity states u, v, w
    plt.subplot(4, 3, 4)
    plt.plot(tVec * Ts, globalVel[0, :] / Ts)
    plt.title('Global velocity U [m/s]')
    plt.xlabel('Time [s]')
    plt.subplot(4, 3, 5)
    plt.plot(tVec * Ts, globalVel[1, :] / Ts)
    plt.title('Global velocity V [m/s]')
    plt.xlabel('Time [s]')
    plt.subplot(4, 3, 6)
    plt.plot(tVec * Ts, -globalVel[2, :] / Ts)
    plt.title('Global velocity W (UP)[m/s]')
    plt.xlabel('Time [s]')

    # Local angles phi, th, psi
    plt.subplot(4, 3, 7)
    plt.plot(tVec * Ts, np.rad2deg(states[6, :]))
    plt.title('Roll \phi [deg]')
    plt.xlabel('Time [s]')
    plt.subplot(4, 3, 8)
    plt.plot(tVec * Ts, np.rad2deg(states[7, :]))
    plt.title('Pitch \theta [deg]')
    plt.xlabel('Time [s]')
    plt.subplot(4, 3, 9)
    plt.plot(tVec * Ts, np.rad2deg(states[8, :]))
    plt.title('Yaw \psi [deg]')
    plt.xlabel('Time [s]')

    # Local rotational velocities w_phi, w_th, w_psi
    plt.subplot(4, 3, 10)
    plt.plot(tVec * Ts, np.rad2deg(states[9, :]) / Ts)
    plt.title('Roll velocity w_\phi [deg/s]')
    plt.xlabel('Time [s]')
    plt.subplot(4, 3, 11)
    plt.plot(tVec * Ts, np.rad2deg(states[10, :]) / Ts)
    plt.title('Pitch velocity w_\theta [deg/s]')
    plt.xlabel('Time [s]')
    plt.subplot(4, 3, 12)
    plt.plot(tVec * Ts, np.rad2deg(states[11, :]) / Ts)
    plt.title('Yaw velocity w_\psi [deg/s]')
    plt.xlabel('Time [s]')

    plt.suptitle('Helipad states. Long crested waves from ' + str(np.rad2deg(beta)) + ' degrees')
    plt.tight_layout()
    plt.show()
