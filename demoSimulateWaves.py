import numpy as np
import scipy.io as sio
import sys
import os
from simulateWaves import simulateWaves

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Append the relative path to the help-files folder
help_files_path = os.path.join(current_dir, 'help-files')
sys.path.append(help_files_path)
from getSignificantWaveHeight import getSignificantWaveHeight

# Demonstration of how to create wave files with different wave properties.
# Authors: Matheus Bernat & Ludvig Granström 2021
# Converted to Python from MATLAB by Ali Azak 2023
# Last updated: May 2023

# Helper function to save wave files
def saveWavesFile(wavesStruct):
    fileName = f"{os.path.abspath(current_dir)}/wave_files/waves__seaState_{wavesStruct['seaState']}__{wavesStruct['waveType']}__beta_{round(wavesStruct['beta'], 2)}__grid_{len(wavesStruct['xVec'])}x{len(wavesStruct['yVec'])}__time_0_{wavesStruct['Ts']}_{int(wavesStruct['tVec'][-1])}__U_{wavesStruct['U']}.mat"
    sio.savemat(fileName, {'wavesStruct': wavesStruct})
    print(f"Saved waves into file '{fileName}'")


## Wave #1: Sea state 6 wave coming from bow (front)
# ------- Use wave with properties below
# Sea state:        6
# Wave type (beta): long-crested (unidirectional)
# Wave angle:       180 degrees
# Grid:             200x100
# Time:             0:0.2:500
# Relative speed    0 m/s
wavesStruct = {}
wavesStruct['seaState'] = 6
wavesStruct['beta'] = np.pi
wavesStruct['xVec'] = np.linspace(0, 299, 300)
wavesStruct['yVec'] = np.linspace(0, 99, 100)
wavesStruct['Ts'] = 0.2
wavesStruct['tVec'] = np.arange(0, 200+wavesStruct['Ts'], wavesStruct['Ts'])
wavesStruct['U'] = 0

wavesStruct['waves'] = simulateWaves(wavesStruct['seaState'],
                                     wavesStruct['xVec'], wavesStruct['yVec'],
                                     wavesStruct['beta'], wavesStruct['tVec'],
                                     wavesStruct['U'])
wavesStruct['waveType'] = 'long'

wavesStruct['displayName'] = f"Waves with properties: " \
                             f"\n   -Sea state: {wavesStruct['seaState']}" \
                             f"\n   -Significant wave height: {getSignificantWaveHeight(wavesStruct['seaState'])} m" \
                             f"\n   -{wavesStruct['waveType']} crested" \
                             f"\n   -Main wave direction (beta): {wavesStruct['beta']} rad" \
                             f"\n   -xVec: {wavesStruct['xVec'][0]}:{1}:{wavesStruct['xVec'][-1]} m" \
                             f"\n   -yVec: {wavesStruct['yVec'][0]}:{1}:{wavesStruct['yVec'][-1]} m" \
                             f"\n   -tVec: {1}:{wavesStruct['Ts']}:{wavesStruct['tVec'][-1]} s" \
                             f"\n   -U: {wavesStruct['U']} m/s"

saveWavesFile(wavesStruct)

## Wave #2: Sea state 6 wave coming from port (left)
# ------- Use wave with properties below
# Sea state:        6
# Wave type (beta): long-crested (unidirectional)
# Wave angle:       pi/2 degrees
# Grid:             300x100
# Time:             0:0.2:100
# Relative speed    0 m/s
wavesStruct = {}
wavesStruct['seaState'] = 6
wavesStruct['beta'] = np.pi/2
wavesStruct['xVec'] = np.linspace(0, 299, 300)
wavesStruct['yVec'] = np.linspace(0, 99, 100)
wavesStruct['Ts'] = 0.2
wavesStruct['tVec'] = np.arange(0, 100+wavesStruct['Ts'], wavesStruct['Ts'])
wavesStruct['U'] = 0

wavesStruct['waves'] = simulateWaves(wavesStruct['seaState'],
                                     wavesStruct['xVec'], wavesStruct['yVec'],
                                     wavesStruct['beta'], wavesStruct['tVec'],
                                     wavesStruct['U'])
wavesStruct['waveType'] = 'long'

wavesStruct['displayName'] = f"Waves with properties: " \
                             f"\n   -Sea state: {wavesStruct['seaState']}" \
                             f"\n   -Significant wave height: {getSignificantWaveHeight(wavesStruct['seaState'])} m" \
                             f"\n   -{wavesStruct['waveType']} crested" \
                             f"\n   -Main wave direction (beta): {wavesStruct['beta']} rad" \
                             f"\n   -xVec: {wavesStruct['xVec'][0]}:{1}:{wavesStruct['xVec'][-1]} m" \
                             f"\n   -yVec: {wavesStruct['yVec'][0]}:{1}:{wavesStruct['yVec'][-1]} m" \
                             f"\n   -tVec: {1}:{wavesStruct['Ts']}:{wavesStruct['tVec'][-1]} s" \
                             f"\n   -U: {wavesStruct['U']} m/s"

saveWavesFile(wavesStruct)

## Wave #3: Sea state 6 wave coming from port (left)
# ------- Use wave with properties below
# Sea state:        6
# Wave type (beta): long-crested (unidirectional)
# Wave angle:       3*pi/4 degrees
# Grid:             300x100
# Time:             0:0.2:500
# Relative speed    0 m/s

wavesStruct = {}
wavesStruct['seaState'] = 6
wavesStruct['beta'] = 3 * np.pi/4
wavesStruct['xVec'] = np.linspace(0, 299, 300)
wavesStruct['yVec'] = np.linspace(0, 99, 100)
wavesStruct['Ts'] = 0.2
wavesStruct['tVec'] = np.arange(0, 200+wavesStruct['Ts'], wavesStruct['Ts'])
wavesStruct['U'] = 0

wavesStruct['waves'] = simulateWaves(wavesStruct['seaState'],
                                     wavesStruct['xVec'], wavesStruct['yVec'],
                                     wavesStruct['beta'], wavesStruct['tVec'],
                                     wavesStruct['U'])
wavesStruct['waveType'] = 'long'

wavesStruct['displayName'] = f"Waves with properties: " \
                             f"\n   -Sea state: {wavesStruct['seaState']}" \
                             f"\n   -Significant wave height: {getSignificantWaveHeight(wavesStruct['seaState'])} m" \
                             f"\n   -{wavesStruct['waveType']} crested" \
                             f"\n   -Main wave direction (beta): {wavesStruct['beta']} rad" \
                             f"\n   -xVec: {wavesStruct['xVec'][0]}:{1}:{wavesStruct['xVec'][-1]} m" \
                             f"\n   -yVec: {wavesStruct['yVec'][0]}:{1}:{wavesStruct['yVec'][-1]} m" \
                             f"\n   -tVec: {1}:{wavesStruct['Ts']}:{wavesStruct['tVec'][-1]} s" \
                             f"\n   -U: {wavesStruct['U']} m/s"

saveWavesFile(wavesStruct)

## Wave #4: Sea state 3 wave coming from bow (front)
# ------- Use wave with properties below
# Sea state:        3
# Wave type (beta): long-crested (unidirectional)
# Wave angle:       180 degrees (from the stern)
# Grid:             300x100
# Time:             0:0.2:500
# Relative speed    0 m/s

wavesStruct = {}
wavesStruct['seaState'] = 3
wavesStruct['beta'] = np.pi
wavesStruct['xVec'] = np.linspace(0, 299, 300)
wavesStruct['yVec'] = np.linspace(0, 99, 100)
wavesStruct['Ts'] = 0.2
wavesStruct['tVec'] = np.arange(0, 300+wavesStruct['Ts'], wavesStruct['Ts'])
wavesStruct['U'] = 0

wavesStruct['waves'] = simulateWaves(wavesStruct['seaState'],
                                     wavesStruct['xVec'], wavesStruct['yVec'],
                                     wavesStruct['beta'], wavesStruct['tVec'],
                                     wavesStruct['U'])
wavesStruct['waveType'] = 'long'

wavesStruct['displayName'] = f"Waves with properties: " \
                             f"\n   -Sea state: {wavesStruct['seaState']}" \
                             f"\n   -Significant wave height: {getSignificantWaveHeight(wavesStruct['seaState'])} m" \
                             f"\n   -{wavesStruct['waveType']} crested" \
                             f"\n   -Main wave direction (beta): {wavesStruct['beta']} rad" \
                             f"\n   -xVec: {wavesStruct['xVec'][0]}:{1}:{wavesStruct['xVec'][-1]} m" \
                             f"\n   -yVec: {wavesStruct['yVec'][0]}:{1}:{wavesStruct['yVec'][-1]} m" \
                             f"\n   -tVec: {1}:{wavesStruct['Ts']}:{wavesStruct['tVec'][-1]} s" \
                             f"\n   -U: {wavesStruct['U']} m/s"

saveWavesFile(wavesStruct)

## Wave #5: Sea state 3 wave coming from bow (front), 15 knots
# ------- Use wave with properties below
# Sea state:        3
# Wave type (beta): long-crested (unidirectional)
# Wave angle:       180 degrees (from the stern)
# Grid:             300x100
# Time:             0:0.2:500
# Relative speed    7.72 m/s

wavesStruct = {}
wavesStruct['seaState'] = 3
wavesStruct['beta'] = np.pi
wavesStruct['xVec'] = np.linspace(0, 299, 300)
wavesStruct['yVec'] = np.linspace(0, 99, 100)
wavesStruct['Ts'] = 0.2
wavesStruct['tVec'] = np.arange(0, 500+wavesStruct['Ts'], wavesStruct['Ts'])
wavesStruct['U'] = 7.72

wavesStruct['waves'] = simulateWaves(wavesStruct['seaState'],
                                     wavesStruct['xVec'], wavesStruct['yVec'],
                                     wavesStruct['beta'], wavesStruct['tVec'],
                                     wavesStruct['U'])
wavesStruct['waveType'] = 'long'

wavesStruct['displayName'] = f"Waves with properties: " \
                             f"\n   -Sea state: {wavesStruct['seaState']}" \
                             f"\n   -Significant wave height: {getSignificantWaveHeight(wavesStruct['seaState'])} m" \
                             f"\n   -{wavesStruct['waveType']} crested" \
                             f"\n   -Main wave direction (beta): {wavesStruct['beta']} rad" \
                             f"\n   -xVec: {wavesStruct['xVec'][0]}:{1}:{wavesStruct['xVec'][-1]} m" \
                             f"\n   -yVec: {wavesStruct['yVec'][0]}:{1}:{wavesStruct['yVec'][-1]} m" \
                             f"\n   -tVec: {1}:{wavesStruct['Ts']}:{wavesStruct['tVec'][-1]} s" \
                             f"\n   -U: {wavesStruct['U']} m/s"

saveWavesFile(wavesStruct)

## Wave #6: Sea state 3 wave coming from bow (front), 15 knots
# ------- Use wave with properties below
# Sea state:        3
# Wave type (beta): short-crested (multi-directional)
# Wave angle:       180 degrees (from the stern)
# Grid:             300x100
# Time:             0:0.2:500
# Relative speed    7.72 m/s

wavesStruct = {}
wavesStruct['seaState'] = 3
wavesStruct['beta'] = np.pi
wavesStruct['xVec'] = np.linspace(0, 299, 300)
wavesStruct['yVec'] = np.linspace(0, 99, 100)
wavesStruct['Ts'] = 0.2
wavesStruct['tVec'] = np.arange(0, 500+wavesStruct['Ts'], wavesStruct['Ts'])
wavesStruct['U'] = 7.72
dmu = np.pi/20
muVec = np.arange(-np.pi/2, np.pi/2, dmu)

wavesStruct['waves'] = simulateWaves(wavesStruct['seaState'],
                                     wavesStruct['xVec'], wavesStruct['yVec'],
                                     wavesStruct['beta'], wavesStruct['tVec'],
                                     wavesStruct['U'])
wavesStruct['waveType'] = 'long'

wavesStruct['displayName'] = f"Waves with properties: " \
                             f"\n   -Sea state: {wavesStruct['seaState']}" \
                             f"\n   -Significant wave height: {getSignificantWaveHeight(wavesStruct['seaState'])} m" \
                             f"\n   -{wavesStruct['waveType']} crested" \
                             f"\n   -Main wave direction (beta): {wavesStruct['beta']} rad" \
                             f"\n   -xVec: {wavesStruct['xVec'][0]}:{1}:{wavesStruct['xVec'][-1]} m" \
                             f"\n   -yVec: {wavesStruct['yVec'][0]}:{1}:{wavesStruct['yVec'][-1]} m" \
                             f"\n   -tVec: {1}:{wavesStruct['Ts']}:{wavesStruct['tVec'][-1]} s" \
                             f"\n   -U: {wavesStruct['U']} m/s"

saveWavesFile(wavesStruct)

## Wave #7: Sea state 3 wave coming from bow (front)
# ------- Use wave with properties below
# Sea state:        3
# Wave type (beta): long-crested
# Wave angle:       180 degrees (from the stern)
# Grid:             850x100
# Time:             0:0.2:90
# Relative speed    0 m/s

wavesStruct = {}
wavesStruct['seaState'] = 3
wavesStruct['beta'] = np.pi
wavesStruct['xVec'] = np.linspace(0, 849, 850)
wavesStruct['yVec'] = np.linspace(0, 99, 100)
wavesStruct['Ts'] = 0.2
wavesStruct['tVec'] = np.arange(0, 90+wavesStruct['Ts'], wavesStruct['Ts'])
wavesStruct['U'] = 0

wavesStruct['waves'] = simulateWaves(wavesStruct['seaState'],
                                     wavesStruct['xVec'], wavesStruct['yVec'],
                                     wavesStruct['beta'], wavesStruct['tVec'],
                                     wavesStruct['U'])
wavesStruct['waveType'] = 'long'

wavesStruct['displayName'] = f"Waves with properties: " \
                             f"\n   -Sea state: {wavesStruct['seaState']}" \
                             f"\n   -Significant wave height: {getSignificantWaveHeight(wavesStruct['seaState'])} m" \
                             f"\n   -{wavesStruct['waveType']} crested" \
                             f"\n   -Main wave direction (beta): {wavesStruct['beta']} rad" \
                             f"\n   -xVec: {wavesStruct['xVec'][0]}:{1}:{wavesStruct['xVec'][-1]} m" \
                             f"\n   -yVec: {wavesStruct['yVec'][0]}:{1}:{wavesStruct['yVec'][-1]} m" \
                             f"\n   -tVec: {1}:{wavesStruct['Ts']}:{wavesStruct['tVec'][-1]} s" \
                             f"\n   -U: {wavesStruct['U']} m/s"

saveWavesFile(wavesStruct)

## Wave #8: Sea state 0
# ------- Use wave with properties below
# Sea state:        0
# Wave type (beta): long-crested
# Wave angle:       180 degrees (from the stern)
# Grid:             300x100
# Time:             0:0.2:60
# Relative speed    0 m/s

wavesStruct = {}
wavesStruct['seaState'] = 0
wavesStruct['beta'] = np.pi
wavesStruct['xVec'] = np.linspace(0, 499, 500)
wavesStruct['yVec'] = np.linspace(0, 299, 300)
wavesStruct['Ts'] = 0.2
wavesStruct['tVec'] = np.arange(0, 60+wavesStruct['Ts'], wavesStruct['Ts'])
wavesStruct['U'] = 0

wavesStruct['waves'] = simulateWaves(wavesStruct['seaState'],
                                     wavesStruct['xVec'], wavesStruct['yVec'],
                                     wavesStruct['beta'], wavesStruct['tVec'],
                                     wavesStruct['U'])
wavesStruct['waveType'] = 'long'

wavesStruct['displayName'] = f"Waves with properties: " \
                             f"\n   -Sea state: {wavesStruct['seaState']}" \
                             f"\n   -Significant wave height: {getSignificantWaveHeight(wavesStruct['seaState'])} m" \
                             f"\n   -{wavesStruct['waveType']} crested" \
                             f"\n   -Main wave direction (beta): {wavesStruct['beta']} rad" \
                             f"\n   -xVec: {wavesStruct['xVec'][0]}:{1}:{wavesStruct['xVec'][-1]} m" \
                             f"\n   -yVec: {wavesStruct['yVec'][0]}:{1}:{wavesStruct['yVec'][-1]} m" \
                             f"\n   -tVec: {1}:{wavesStruct['Ts']}:{wavesStruct['tVec'][-1]} s" \
                             f"\n   -U: {wavesStruct['U']} m/s"

saveWavesFile(wavesStruct)











