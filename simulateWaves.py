import numpy as np

import sys
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Append the relative path to the help-files folder
help_files_path = os.path.join(current_dir, 'help-files')
sys.path.append(help_files_path)
from getSignificantWaveHeight import getSignificantWaveHeight
from wavespec import wavespec

def simulateWaves(seaState, xVec, yVec, beta, tVec, U, lambbda = 1, muVec = [], dmu = 0):
    '''    
    SIMULATEWAVES(seaState, xVec, yVec, beta, tVec, U , lambda, muVec, dmu) 
    Takes in sea state and plots a wave height. Uses the Bretschneider spectrum.
    Inputs:
      - seaState: integer in interval [1, 9].
      - xVec:     1xN vector. E.g. xVec = linspace(-50, 50, 100).
      - yVec:     1xN vector. E.g. yVec = linspace(-50, 50, 100).
      - beta:     direction of main wave in rad.
      - tVec:     time vector. E.g.: tVec = 0:0.1:50.
      - U:        speed of the ship [m/s]
      - muVec:    angle directions vector. E.g.: -pi/2:dmu:pi/2. If muVec=[],
                  then the waves generated will be unidirectional (long-
                  crested).
      - dmu:      direction interval taken in muVec. Used if muVec ~= [].
      - lambbda:   waveLength. If a sea with infinite depth is assumed, set
                  lambda to [].
    Ouput:
      - waves:    if ~is3d, then size(waves) = (1, length(tVec)), where waves
                  is equal to the wave height in some point in the sea. If  
                  is3d, then size(waves) = (length(xVec), length(yVec), 
                  length(tVec)), where waves will then represent the wave
                  height of all points (x, y) over a 2D grid defined by xVec
                  and yVec over an interval of time tVec.
    '''
    print('Creating waves...')
    g = 9.81
    lambbda = np.array(lambbda)
    # Get significant wave height
    Hs = getSignificantWaveHeight(seaState)

    # Create Bretschneider spectrum given Hs and plot spectrum
    dw = 0.1
    wVec = np.arange(dw/2, 3, dw)
    A = 8.1 * 1e-3 * g**2  # constant, Equation (8.54) in Fossen
    if Hs!=0:
        B = 3.11 / (Hs**2) # Equation (8.55) in Fossen
    else:
        B = 999999999999999 # Set B to a large number if Hs = 0 
    specType = 1  # Bretschneider (@ Fossen pg 203)
    S = wavespec(specType, [A, B], wVec, 0)
    S[0] = 0  # the first element is NaN for some reason

    waves = np.zeros((len(yVec), len(xVec), len(tVec)))

    # Get the set of frequencies, directions and phases that will be used to
    # generate waves for all points in the grid:
    waveFrequencies = np.zeros(len(wVec))
    for k in range(len(waveFrequencies)):
        waveFrequencies[k] = wVec[k] - dw/2 + dw * np.random.rand()

    if len(muVec) > 0:  # Short-crested wave
        waveDirections = np.zeros(len(muVec))
        for i in range(len(waveDirections)):
            waveDirections[i] = muVec[i] - dmu/2 + dmu * np.random.rand()
        sizeWaveDirections = len(waveDirections)
    else:
        sizeWaveDirections = 1

    wavePhases = np.zeros((len(waveFrequencies),sizeWaveDirections))
    for k in range(len(waveFrequencies)):
        for i in range(sizeWaveDirections):
            wavePhases[k, i] = 2 * np.pi * np.random.rand()
    # Get the wave heights for all coordinates (x, y) for all times in tVec:
    for yIdx in range(len(yVec)):
        y = yVec[yIdx]
        for xIdx in range(len(xVec)):
            x = xVec[xIdx]

            # For each coordinate (x, y), sum the contribution of all the waves
            # to get the final wave amplitude at that point = sumOfWaves.
            sumOfWaves = 0

            for k in range(len(waveFrequencies)):
                w_k = waveFrequencies[k]

                # Long-crested
                if len(muVec) == 0:
                    if lambbda is not None:
                        # Lambda is passed as an argument
                        coeff = 2 * np.pi / lambbda
                    else:
                        # Infinite depth sea assumed
                        coeff = w_k ** 2 / g
                    e_k = wavePhases[k]
                    amp = np.sqrt(2 * S[k] * dw)
                    wave = amp * np.cos(coeff * ((x + U * tVec) * np.cos(-beta) +
                                                 y * np.sin(-beta)) -
                                        w_k * tVec + e_k)
                    sumOfWaves += wave

                # Short-crested
                else:
                    for i in range(len(waveDirections)):
                        e_ik = wavePhases[0, k]
                        mu_i = waveDirections[i]
                        amp = np.sqrt(2 * S[k] * spread(mu_i) * dw * dmu);
                        wave = amp * np.cos(w_k**2/g * ((x+U*tVec) * np.cos(mu_i - beta) 
                                    + y * np.sin(mu_i - beta))  
                                                - w_k * tVec + e_ik)
                        sumOfWaves += wave
            waves[yIdx, xIdx, :] = sumOfWaves
    print("Done creating waves!")
    return waves

def spread(mu):
    if(mu >= -np.pi/2 and mu <= np.pi/2):
        return ((2/np.pi)*np.cos(mu)**2)
    else:
        return 0

    