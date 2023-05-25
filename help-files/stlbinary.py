import numpy as np

def stlbinary(M):
    F = []
    V = []
    N = []

    if len(M) < 84:
        raise ValueError('Incomplete header information in binary STL file.')

    # Bytes 81-84 are an unsigned 32-bit integer specifying the number of faces that follow.
    numFaces = np.frombuffer(M[80:84], dtype=np.uint32)[0]

    if numFaces == 0:
        print('No data in STL file.')
        return F, V, N

    T = M[84:]
    F = np.empty((numFaces, 3), dtype=np.double)
    V = np.empty((3 * numFaces, 3), dtype=np.double)
    N = np.empty((numFaces, 3), dtype=np.double)

    numRead = 0
    while numRead < numFaces:
        # Each facet is 50 bytes
        # - Three single precision values specifying the face normal vector
        # - Three single precision values specifying the first vertex (XYZ)
        # - Three single precision values specifying the second vertex (XYZ)
        # - Three single precision values specifying the third vertex (XYZ)
        # - Two unused bytes
        i1 = 50 * numRead
        i2 = i1 + 50
        facet = T[i1:i2]

        n = np.frombuffer(facet[0:12], dtype=np.float32)
        v1 = np.frombuffer(facet[12:24], dtype=np.float32)
        v2 = np.frombuffer(facet[24:36], dtype=np.float32)
        v3 = np.frombuffer(facet[36:48], dtype=np.float32)

        n = np.double(n)
        v = np.double([v1, v2, v3])

        fInd = numRead
        vInd1 = 3 * fInd
        vInd2 = vInd1 + 3

        V[vInd1:vInd2, :] = v
        F[fInd, :] = np.arange(vInd1, vInd2,dtype = np.double) + 1
        N[fInd, :] = n

        numRead += 1
    return F, V, N

