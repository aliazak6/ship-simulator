# Demonstration of how to simulate the movement of a ship on predefined 
# waves. Assume ship points north.
# Authors: Matheus Bernat & Ludvig Granström 2021
# Converted to Python from MATLAB by Ali Azak 2023
# Last updated: May 2023
#
# Demo 1-3: Sea state 6, long-crested waves, no ship speed,
# Demo 4:   Sea state 3, long-crested waves, no ship speed
# Demo 5:   Sea state 3, long-crested waves, ship speed of 15 knots
# Demo 6:   Sea state 3, short-crested waves, ship speed of 15 knots
# Demo 7:   No waves, stabilization test
# Demo 8:   Sea state 3, corridor test, ship speed of 15 knots


import os
import numpy as np
import sys
from simulateShip import simulateShip

# Set paths
current_dir = os.path.dirname(os.path.abspath(__file__))
wavesPath = os.path.join(current_dir, 'wave_files')
helpFilesPath = os.path.join(current_dir, 'help-files')
boatPath = os.path.join(current_dir, 'boat-files')

# Add paths
import sys
sys.path.append(wavesPath)
sys.path.append(helpFilesPath)
sys.path.append(boatPath)

## ------- Create ship with properties below
# Ship:                       HMS Norfolk (hull only)
# Mass:                       2.5e6
# Dimensions:                 137x15x16 
# Vertices initial position:  [30 35 5.55]
# Reference velocity along u: 0 [m/s] (should always be 0, the ship speed is set in the wave file)
# Reference yaw:              0 degrees
# CoG offset:                 [-4.77 0.022 -2]
# Position of heliPad         [40 35 6]
# Create ship structure
shipStruct = {
    'file': f'{boatPath}/filteredNorfolkNew.stl',
    'M': 2.5e6,
    'len': 137,
    'width': 15,
    'height': 16,
    'verticesPos': [35, 70, 5.55],
    'cogOffset': [-4.77, 0.022, -2],
    'refSpeedU': 0,
    'refYaw': 0,
    'helipadPos': [40, 35, 6],
    #     [v_u v_v v_w phi th psi w_phi w_th w_psi]'
    'x0': [0, 0, 0, 0, 0, 0, 0, 0, 0]
}

'''
## --------------- Demo #1: Sea state 6 pitch test (waves from the north)
# ------- Use wave with properties below
# Sea state:        6
# Wave type (beta): long-crested (unidirectional)
# Wave angle:       180 degrees (from the front)
# Grid:             300x100
# Time:             0:0.2:500
# Ship speed        0
isPlot = True
isVisual = True
waveFile = f'{os.path.abspath(current_dir)}/wave_files/waves__seaState_6__long__beta_3.14__grid_300x100__time_0_0.2_200__U_0.mat'
states, face, vert, cogVec = simulateShip(waveFile, shipStruct, isPlot, isVisual,1)


## --------------- Demo #2: Sea state 6 pitch & roll test (waves from northwest)
# ------- Use wave with properties below
# Sea state:        6
# Wave type (beta): long-crested (unidirectional)
# Wave angle:       pi degrees (from the left)
# Grid:             300x100
# Time:             0:0.2:500
# Ship speed        0

waveFile = f'{os.path.abspath(current_dir)}/wave_files/waves__seaState_6__long__beta_2.36__grid_300x100__time_0_0.2_200__U_0.mat'
states, face, vert, cogVec = simulateShip(waveFile, shipStruct, True, True,2)

## --------------- Demo #3: Sea state 3, waves from the north, no speed
# ------- Use wave with properties below
# Sea state:        3
# Wave type (beta): long-crested (unidirectional)
# Wave angle:       180 degrees (from the front)
# Grid:             300x100
# Time:             0:0.2:500
# Ship speed        0

waveFile = f'{os.path.abspath(current_dir)}/wave_files/waves__seaState_3__long__beta_3.14__grid_300x100__time_0_0.2_300__U_0.mat'
     
states, face, vert, cogVec = simulateShip(waveFile, shipStruct, True, True,3)

## --------------- Demo #4: Sea state 3, waves from the north, 15 knots
# ------- Use wave with properties below
# Sea state:        3
# Wave type (beta): long-crested (unidirectional)
# Wave angle:       180 degrees (from the front)
# Grid:             300x100
# Time:             0:0.2:500
# Ship speed        0

waveFile = f'{os.path.abspath(current_dir)}/wave_files/waves__seaState_3__long__beta_3.14__grid_300x100__time_0_0.2_500__U_7.72.mat'
states, face, vert, cogVec = simulateShip(waveFile, shipStruct, True, True,4)


## --------------- Demo #5: Stabilization test (crazy results)
# ------- Use wave with properties below
# Sea state:        3
# Wave type :       No waves
# Grid:             500x300
# Time:             0:0.2:50
# Ship speed        0

#               [v_u v_v v_w phi th psi w_phi w_th w_psi]'
import numpy as np
shipStruct['x0'] = [0, 0, 0, np.deg2rad(40), 0, 0, 0, 0, 0]# x Initial state values

waveFile = f'{os.path.abspath(current_dir)}/wave_files/waves__seaState_0__long__beta_3.14__grid_500x300__time_0_0.2_60__U_0.mat'
states, face, vert, cogVec = simulateShip(waveFile, shipStruct, True, True,5)
'''
##--------------- Demo #6: Corridor test
# ------- Use wave with properties below
# Sea state:        3
# Wave type :       No waves
# Grid:             300x100
# Time:             0:0.2:90
# Ship speed        0
shipStruct['refSpeedU']   = 7
waveFile = f'{os.path.abspath(current_dir)}/wave_files/waves__seaState_3__long__beta_3.14__grid_850x100__time_0_0.2_90__U_0.mat'
states, face, vert, cogVec = simulateShip(waveFile, shipStruct, True, True,6)



