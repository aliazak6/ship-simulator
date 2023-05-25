import numpy as np
import os
from stlbinary import stlbinary
def stlreadOwn(file):
    # STLREAD imports geometry from an STL file into Python.
    # FV = STLREAD(FILENAME) imports triangular faces from the binary STL file indicated by FILENAME,
    # and returns the face and vertex arrays FV.
    # [F, V] = STLREAD(FILENAME) returns the face and vertex arrays F and V separately.
    # [F, V, N] = STLREAD(FILENAME) also returns the face normal vectors.
    # The faces and vertices are arranged in the format used by the mesh plot object.
    
    if not os.path.isfile(file):
        raise FileNotFoundError("File '{}' not found. If the file is not on the current working directory, "
                                "be sure to specify the full path to the file.".format(file))

    with open(file, 'rb') as fid:
        M = np.fromfile(fid, dtype=np.uint8)

    return stlbinary(M)