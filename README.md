# Ship Simulator

Ship simulator repository is used the code and work of Matheus Bernat & Ludvig Granström made in 2021. It is written to run their MATLAB implementation of simulating motion of waves and motion of ships on those waves on Python. Python code is written for integration and further development.

Original MATLAB code link: https://github.com/LINK-SIC-2021-Bernat-Granstrom/ship-simulator

## Installation
Just clone the repository on your machine.

## Demos
### Simulate waves
The demo-file for wave simulation is __demoSimulateWaves.py__ 
When the Python script run, wavesStruct is created and __simulateWaves.py__ called, corresponding waves are created and saved to a .mat file \
When the repository cloned, in order to run ship simulation these wave files must be created first.

### Simulate ship on waves
The demo file for simulating a ship is __demoSimulateWaves.py__ Corresponding wave and ship files are loaded in script and __simulateShip.py__ is called. After the simulation, parameters needed for 3D visualization and graphs saved into a mat file inside __/simulation-results__ with respective demo number. This is done for quick visualization on weak machines.

## Visualization
### 3D Visualization
__visualizeSimulation.py__ file is used to animate wave and ship properties saved on simulations. Script uses python mayavi package and dependencies may need to be installed.
### Plotting Data
__plotShipStates.py__ file can be used to plot changes of parameters in time.


## License
[MIT](https://github.com/aliazak6/ship-simulator/blob/master/LICENSE)