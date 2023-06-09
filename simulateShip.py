import numpy as np
from scipy.signal import cont2discrete as c2d
import os
import sys
import scipy.io as sio


# Set paths
current_dir = os.path.dirname(os.path.abspath(__file__))
wavesPath = os.path.join(os.getcwd(), 'wave_files')
helpFilesPath = os.path.join(os.getcwd(), 'help-files')
boatPath = os.path.join(os.getcwd(), 'boat-files')

# Add paths
import sys
sys.path.append(wavesPath)
sys.path.append(helpFilesPath)
sys.path.append(boatPath)

# Append the relative path to the help-files folder
help_files_path = os.path.join(current_dir, 'help-files')
sys.path.append(help_files_path)
from areaOfFace import areaOfFace
from stlreadOwn import stlreadOwn
from R import R
# Suppress/hide the warning
np.seterr(invalid='ignore')

# Help functions
def calculatePointsAreasNormals(V):
    # Returns facepoints which are the center of the triangles, the
    # triangles' areas and the normals to the triangles.
    j = 0
    facePoints = []
    faceAreas = []
    normals = []
    for i in range(0, len(V)-2, 3):
        facePoints.append([np.mean(V[i:i+3, 0]), np.mean(V[i:i+3, 1]), np.mean(V[i:i+3, 2])])
        faceAreas.append(areaOfFace(V[i:i+3, 0], V[i:i+3, 1], V[i:i+3, 2]))
        p0 = V[i, :].T
        p1 = V[i+1, :].T
        p2 = V[i+2, :].T
        n = np.cross(p0-p1, p0-p2) / np.linalg.norm(np.cross(p0-p1, p0-p2))
        normals.append(-n)  # The normal of the face
    facePoints = np.array(facePoints)
    faceAreas = np.array(faceAreas)
    normals = np.array(normals)
    return facePoints, faceAreas, normals
def T(phi, th):
  # Gustafsson, "Statistical Sensor Fusion" 3rd edition
  # Eq. (13.9), p. 349
  T = [[1, np.sin(phi)*np.tan(th), np.cos(phi)*np.tan(th)],
        [0, np.cos(phi), -np.sin(phi)],
        [0, np.sin(phi)/np.cos(th), np.cos(phi)/np.cos(th)]]
  return T

def pRegulator(Kp, refValue, currentValue):
    # Simple P-control of speed.
    regulation = Kp * (refValue - currentValue)
    return regulation

def getVelMetPerTs(vel, Ts):
    # Gets a velocity in m/s and returns a velocity in m/Ts
    velMeterPerTs = vel * Ts
    return velMeterPerTs
def simulateShip(wavesFile, shipStruct, isPlot, isVisual,demonum):
  '''
  SIMULATESHIP Ship on sea simulation. Given a waves file and a ship,
  simulates 12 states of the ship through time. The states are: 
    - [x,     y,    z]:    position of the ship’s center of gravity (cog)
                            described in the earth-fixed coordinate system;
    - [v_u,   v_v,  v_w]:  velocity of the ship’s cog described in the body
                            -fixed coordinate system;
    - [phi,   th,   psi]:  Euler angles describing rotation of the body-
                            fixed coordinate system in relation to the earth
                            -fixed coordinate system;
    - [w_phi, w_th, w_psi]: rotational velocity in the body-fixed
                            coordinate system.
  The forces considered are the hidrostatic (buoyancy) force by the water, 
  the ship's weight, the coriolis effect and the propellers force. Ignores:
  added mass, wind forces, dynamic water forces, etc. To calculate the 
  inertia, the ship was assumed to be a solid cuboid. 
  Inputs:
    - wavesFile:  file containing waves and its properties;
    - shipStruct: struct containing STL file and other ship properties;
    - isPlot:     boolean, if true: plots states through time;
    - isVisual:   boolean, if true: show visualization of simulation in 3D.
    - demonum:    number of the demo to be run. # Added by me to reproduce visualiztion without simulation
  Outputs:
    - states:    all 12 states simulated through the time vector defined in
                  the wave file;
    - faces:     ship's faces, only returned to be able to show
                  visualization outside function;
    - vertices:  ship's vertices, only returned to be able to show
                  visualization outside function;
    - cogVec:    center of gravity vector, only returned to be able to show
                  visualization outside function.
  Constants:
    - Ax: cross-sectional area of ship along ship's x-axis [m^2];
    - Ay: cross-sectional area of ship along ship's y-axis [m^2];
    - Az: cross-sectional area of ship along ship's z-axis [m^2];
    - Ix: ship's momentum of inertia along x axis;
    - Iy: ship's momentum of inertia along y axis;
    - Iz: ship's momentum of inertia along z axis;
    - Ki: integrational constant for the PI-regulator;
    - Kp: proportional constant for the PI-regulator;
    - B:  damping constant for ship's rotational velocity;
    - Cd: damping constant for ship's velocity;
    - M:  ship's mass [kg];
    - ro: water density [kg/m^3];
    - g:  gravitational acceleration [m/s^2];
    - l:  length of ship (along x-axis) [m];
    - w:  width of ship (along y-axis) [m];
    - h:  height of ship (along z-axis) [m].
  '''
  print("\nStarted shipOnSea simulation!\n")

  # ------------------------------- Define constants ------------------------
  # ----- Non-tunable constants

  # Ship dimensions inheritant to HMS Norfolk
  length = shipStruct['len']
  width = shipStruct['width']
  height = shipStruct['height']
  M = shipStruct['M']
  # Cross sectional area of the submerged hull
  Au = width * 0.9 * height * 0.33
  Av = height * 0.33 * length
  Aw = length * width * 0.9

  # Offset to ship's center of gravity, set by trial and error
  cogOffset = shipStruct['cogOffset']

  #Ship's moment of inertia
  I = M / 12 * np.diag([width**2 + height**2, length**2 + height**2, length**2 + width**2])
  Iu = I[0, 0]
  Iv = I[1, 1]
  Iw = I[2, 2]

  # Physical constants
  ro = 997
  g = 9.81

  # ----- Tunable constants
  Kp_force = 9.5
  Ki_force = 0.82
  Kp_torque = 3.5
  Ki_torque = 0.5

  C_du = 2.5
  C_dv = 2.5
  C_dw = 2.5

  B_phi = 1e10 / 20
  B_th  = 1e10 
  B_psi = 1e10

  # Load waves
  print('1) Loading waves...')
  wavesData = sio.loadmat(wavesFile)
  waves = wavesData['wavesStruct']['waves'][0, 0]
  beta = wavesData['wavesStruct']['beta'][0, 0]
  xVec = wavesData['wavesStruct']['xVec'][0, 0][0]
  yVec = wavesData['wavesStruct']['yVec'][0, 0][0]
  tVec = wavesData['wavesStruct']['tVec'][0, 0][0]
  Ts = wavesData['wavesStruct']['Ts'][0, 0][0]
  displayName = wavesData['wavesStruct']['displayName'][0, 0][0]
  print('Waves loaded:\n', displayName)

  # Load ship's STL file
  print('2) Loading ship and computing normal vectors to triangles...')
  faces, vertices, _ = stlreadOwn(shipStruct['file'])
  vertices += shipStruct['verticesPos']
  cog = np.array([(np.max(vertices[:, 0]) + np.min(vertices[:, 0])) / 2,
                  (np.max(vertices[:, 1]) + np.min(vertices[:, 1])) / 2,
                  (np.max(vertices[:, 2]) + np.min(vertices[:, 2])) / 2],dtype=np.float32)
  cog = cog + cogOffset
  facePoints, faceAreas, normals = calculatePointsAreasNormals(vertices)
  print('Boat loaded!')

  # Define time update model and simulate
  print('3) Simulating states through time...')
  # ----- Define update matrices A and B (C is arbitrary) and discretize.
  #x y z      v_u       v_v     v_w         phi th psi w_phi   w_th w_psi
  A = np.array([[0,0,0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0,0,0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0,0,0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0,0,0, -C_du*ro*Au/M, 0, 0, 0, 0, 0, 0, 0, 0],
                [0,0,0, 0, -C_dv*ro*Av/M, 0, 0, 0, 0, 0, 0, 0],
                [0,0,0, 0, 0, -C_dw*ro*Aw/M, 0, 0, 0, 0, 0, 0],
                [0,0,0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0,0,0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0,0,0, 0, 0, 0, 0, 0, 0, -B_phi/Iu, 0, 0],
                [0,0,0, 0, 0, 0, 0, 0, 0, 0, -B_th/Iv, 0],
                [0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, -B_psi/Iw]])
  # F_x/M   F_y/M   F_z/M   Tau_x/Ix   Tau_y/Iy   Tau_z/Iz
  B = np.array([[0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1]])

  C = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

  sys_ = c2d((A, B, C, []), Ts)
  Ad, Bd, _, _, _ = sys_
  # ----- Define reference states and initialize other variables
  refSpeedU = getVelMetPerTs(shipStruct['refSpeedU'], Ts)  # m/Ts
  refYaw = shipStruct['refYaw']
  extraUForce = 0
  extraYawTorque = 0
  cogVec = np.zeros((len(tVec), 3))

  # ----- Initialize all states and set 1st state
  states = np.zeros((12, len(tVec)))
  #  [x       y       z     ], [v_u v_v v_w phi th psi w_phi w_th w_psi]'
  states[:, 0] = np.concatenate(([cog[0], -cog[1], -cog[2]], shipStruct['x0']))

  # ----- Rotate facePoints & normals according to initial states
  phi = states[6, 0]
  th  = states[7, 0]
  psi = states[8, 0]
  rotation_matrix = R(phi, -th, -psi)  # Assuming R is a function for calculating the rotation matrix
  facePoints = np.dot(rotation_matrix.T, (facePoints - cog).T).T + cog
  normals = np.dot(rotation_matrix.T, normals.T).T
  # ----- State update for all time steps
  for tIdx in range(len(tVec)-1):
    cogVec[tIdx, :] = cog
    # ------- Compute sum of all forces F_net & sum of all torques Tau_net
    F_net = np.zeros((3, ))
    Tau_net = np.zeros((3, ))

    for nIdx in range(len(normals)):
      # Get index of waves that is closest to the evaluated normal
      xIdx = int(round(facePoints[nIdx, 0])) - 1
      yIdx = int(round(facePoints[nIdx, 1])) - 1
      facePointHeight = facePoints[nIdx, 2]

      # Extract wave height at the given indices
      waveHeight = waves[yIdx, xIdx, tIdx]

      # Add netto component if wave is above the considered normal
      if waveHeight > facePointHeight:
        # Force
        h = waveHeight - facePointHeight
        volume = h * faceAreas[nIdx]
        F_buoy = ro * g * volume * normals[nIdx, :]
        F_net += F_buoy

        # Torque
        lever = (facePoints[nIdx, :] - cog).reshape((3, 1))
        phi, th, psi = states[6:9, tIdx]
        R_phi_th_psi = R(phi, -th, -psi)
        lever_rotated = R_phi_th_psi @ lever
        F_buoy_rotated = R_phi_th_psi @ F_buoy
        Tau = np.cross(lever_rotated.flatten(), F_buoy_rotated.flatten())
        Tau_net += Tau

    # ------- Set up input
    phi = states[6, tIdx]
    th = states[7, tIdx]
    psi = states[8, tIdx]
    v_u = states[3, tIdx]
    
    extraUForce = Ki_force * extraUForce + pRegulator(Kp_force, refSpeedU, v_u)
    
    forcesInLocalCoord = R(phi,-th,-psi) @ np.array([F_net[0]/M, -F_net[1]/M, -F_net[2]/M + g],dtype = np.float32).flatten() + np.array([[extraUForce], [0], [0]],dtype = np.float32).flatten()
    
    extraYawTorque = Ki_torque * extraYawTorque + pRegulator(Kp_torque, refYaw, psi)
    torqueInLocalCoord = np.array([Tau_net[0]/Iu, -Tau_net[1]/Iv, -Tau_net[2]/Iw],dtype = np.float32) + np.array([0, 0, extraYawTorque],dtype = np.float32)
    
    inputs = np.concatenate((forcesInLocalCoord, torqueInLocalCoord), axis=0)
    
    # ------- Time-update
    v_u = states[3, tIdx]
    v_v = states[4, tIdx]
    v_w = states[5, tIdx]
    w_phi = states[9, tIdx]
    w_th = states[10, tIdx]
    w_psi = states[11, tIdx]
    
    velInGlobalCoord = np.linalg.inv(R(phi, th, psi)) @ np.array([[v_u], [v_v], [v_w]])
    rotVelDerivative = T(phi, th) @ np.array([[w_phi], [w_th], [w_psi]])

    coriolisV = np.cross(np.array([[w_phi, w_th, w_psi]]), np.array([[v_u, v_v, v_w]]))

    
    # Make time-update as below due to non-linearities in the A matrix
    op1 = np.array([[states[0,tIdx] + Ad[0, 3] * velInGlobalCoord[0, 0]],
                    [states[1,tIdx] + Ad[1, 4] * velInGlobalCoord[1, 0]],
                    [states[2,tIdx] + Ad[2, 5] * velInGlobalCoord[2, 0]],
                    [states[3, tIdx]* Ad[3, 3] - Ts * coriolisV[0, 0]],
                    [states[4, tIdx]* Ad[4, 4] - Ts * coriolisV[0, 1]],
                    [states[5, tIdx]* Ad[5, 5] - Ts * coriolisV[0, 2]],
                    [states[6,tIdx] + Ad[6, 9] *rotVelDerivative[0, 0]],
                    [states[7,tIdx] + Ad[7, 10]*rotVelDerivative[1, 0]],
                    [states[8,tIdx] + Ad[8, 11]*rotVelDerivative[2, 0]],
                    [Ad[9, 9] * states[9, tIdx]],
                    [Ad[10, 10] * states[10, tIdx]],
                    [Ad[11, 11] * states[11, tIdx]]],dtype = np.float32).flatten()
    op2 = (Bd @ inputs).flatten()
    states[:, tIdx+1] = op1 + op2

    # ------- Update ship hull
    deltaX = states[0, tIdx+1] - states[0, tIdx]
    deltaY = states[1, tIdx+1] - states[1, tIdx]
    deltaZ = states[2, tIdx+1] - states[2, tIdx]
    
    deltaPhi = states[6, tIdx+1] - states[6, tIdx]
    deltaTh  = states[7, tIdx+1] - states[7, tIdx]
    deltaPsi = states[8, tIdx+1] - states[8, tIdx]
    
    facePoints = (R(deltaPhi, -deltaTh, -deltaPsi).T @ (facePoints - cog).T).T + cog + np.array([[deltaX, -deltaY, -deltaZ]])
    normals = (R(deltaPhi, -deltaTh, -deltaPsi).T @ normals.T).T
    cog = cog + np.array([[deltaX, -deltaY, -deltaZ]])  
  print('Simulation done!')

  
  ##### SAVE VARIABLES FOR REPRODUCTION OF SIMULATION
  current_dir = os.path.dirname(os.path.abspath(__file__))
  # Save variables to a .mat file
  plotStruct = {
    'states': states,
    'tVec': tVec,
    'Ts': Ts,
    'beta': beta,
    'helipadPos': shipStruct['helipadPos']
  }
  sio.savemat(f'{current_dir}/simulation-results/Simulation_{demonum}_Result_plotStruct.mat', plotStruct)
  # Save variables to a .mat file
  visualizeStruct = {
      'states': states,
      'waves': waves,
      'xVec': xVec,
      'yVec': yVec,
      'tVec': tVec,
      'faces': faces,
      'vertices': vertices,
      'cogVec': cogVec
  }
  sio.savemat(f'{current_dir}/simulation-results/Simulation_{demonum}_Result_visualizeStruct.mat', visualizeStruct)

  return states, faces, vertices, cogVec
'''
  # ------------------------------- Plot states through time ----------------
  if isPlot:
      plotShipStates(states, tVec, Ts, beta)
  #     plotHelipadStates(states, tVec, Ts, beta, shipStruct.helipadPos)
      
  # ------------------------------- Visualize simulation in 3D --------------
  if isVisual:
      visualizeSimulation(states, waves, xVec, yVec, tVec, faces, vertices, cogVec)
  return states, faces, vertices, cogVec
'''
  
  
  




