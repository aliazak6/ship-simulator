import numpy as np

def R(phi, th, psi):
    # R Rotation matrix using the xyz rule.
    # Gustafsson, "Statistical Sensor Fusion" 3rd edition
    # Eq. (13.7), p. 348
    R = np.array([[np.cos(th)*np.cos(psi),       np.cos(th)*np.sin(psi),       -np.sin(th)],
                  [-np.cos(phi)*np.sin(psi)+np.sin(phi)*np.sin(th)*np.cos(psi), np.cos(phi)*np.cos(psi)+np.sin(phi)*np.sin(th)*np.sin(psi), np.sin(phi)*np.cos(th)],
                  [np.sin(phi)*np.sin(psi)+np.cos(phi)*np.sin(th)*np.cos(psi), -np.sin(phi)*np.cos(psi)+np.cos(phi)*np.sin(th)*np.sin(psi), np.cos(phi)*np.cos(th)]])
    
    return R
