import random

def getSignificantWaveHeight(seaState):
    # GETSIGNIFICANTWAVEHEIGHT Returns the significant wave height Hs given the
    # sea state from 0 to 8. Reference: Fossen's handbook pg. 204.
    if seaState == 0:
        Hs = 0
    elif seaState == 1:
        Hs = random.uniform(0, 0.3)  # Hs between 0 and 0.3 m
    elif seaState == 2:
        Hs = random.uniform(0.3, 0.6)  # Hs between 0.3 and 0.6 m
    elif seaState == 3:
        Hs = random.uniform(1, 2)  # Hs between 0.6 and 2 m
    elif seaState == 4:
        Hs = random.uniform(2, 3)  # Hs between 2 and 3 m
    elif seaState == 5:
        Hs = random.uniform(3, 4)  # Hs between 3 and 4 m
    elif seaState == 6:
        Hs = random.uniform(4, 6)  # Hs between 4 and 6 m
    elif seaState == 7:
        Hs = random.uniform(6, 9)  # Hs between 6 and 9 m
    elif seaState == 8:
        Hs = random.uniform(9, 14)  # Hs between 9 and 14 m
    return Hs
