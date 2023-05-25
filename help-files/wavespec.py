import numpy as np
import matplotlib.pyplot as plt

def wavespec(SpecType, Par, W, PlotFlag):
    S = []
    if np.ndim(W) == 2:
        n, = np.shape(W)
    else:
        n,m = 1, np.shape(W)[0]
    if n > m:
        print('Error: W must be a column vector')
        return

    
    if SpecType == 1:  # Bretschneither
        A = Par[0]
        B = Par[1]
        for k in range(len(W)):
            Sa = A * W[k]**(-5) * np.exp(-B / (W[k]**4))
            S.append(Sa)
        TitleStr = 'Bretschneither Spectrum'
        L1Str = f'A={A} [m^2 s^{{-4}}], B={B} [s^{{-4}}]'
    
    elif SpecType == 2:  # Pierson-Moskowitz
        Vwind20 = Par[0]
        A = 8.1e-3 * 9.81**2
        B = 0.74 * (9.81 / Vwind20)**4
        for k in range(len(W)):
            Sa = A * W[k]**(-5) * np.exp(-B / (W[k]**4))
            S.append(Sa)
        TitleStr = 'Pierson-Moskowitz Spectrum'
        L1Str = f'Vwind @20m ASL = {Vwind20} [m/s]'

    elif SpecType == 3:  # ITTC-Modified Pierson-Moskowitz (Hs, T0)
        Hs = Par[0]
        T0 = Par[1]
        A = 487 * Hs**2 / T0**4
        B = 1949 / T0**4
        for k in range(len(W)):
            Sa = A * W[k]**(-5) * np.exp(-B / (W[k]**4))
            S.append(Sa)
        TitleStr = 'ITTC-Modified Pierson-Moskowitz Spectrum'
        L1Str = f'Hs = {Hs} [m], T0 = {T0} [s]'
    elif SpecType == 4:  # ITTC-Modified Pierson-Moskowitz (Hs, T1)
        Hs = Par[0]
        T1 = Par[1]
        A = 173 * Hs**2 / T1**4
        B = 691 / T1**4
        for k in range(len(W)):
            Sa = A * W[k]**(-5) * np.exp(-B / (W[k]**4))
            S.append(Sa)
        TitleStr = 'ITTC-Modified Pierson-Moskowitz Spectrum'
        L1Str = f'Hs = {Hs} [m], T1 = {T1} [s]'
    elif SpecType == 5:  # ITTC-Modified Pierson-Moskowitz (Hs, Tz)
        Hs = Par[0]
        Tz = Par[1]
        A = 123 * Hs**2 / Tz**4
        B = 495 / Tz**4
        for k in range(len(W)):
            Sa = A * W[k]**(-5) * np.exp(-B / (W[k]**4))
            S.append(Sa)
        TitleStr = 'ITTC-Modified Pierson-Moskowitz Spectrum'
        L1Str = f'Hs = {Hs} [m], Tz = {Tz} [s]'
    elif SpecType == 6:  # JONSWAP (Vwind10, Fetch)
        Vw10 = Par[0]
        fetch = Par[1]
        g = 9.81
        xtilde = g * fetch / (Vw10**2)
        f0 = 3.5 * (g / Vw10) * xtilde**-0.33
        w0 = 2 * np.pi * f0
        alpha = 0.076 * xtilde**-0.22
        for k in range(len(W)):
            if W[k] < w0:
                sigma = 0.07
            else:
                sigma = 0.09
            S1 = alpha * g**2 * (W[k]**-5) * np.exp(-(5 / 4) * (w0 / W[k])**4)
            S2 = 3.3**(np.exp(-(W[k] - w0)**2 / (2 * (sigma * w0)**2)))
            Sa = S1 * S2
            S.append(Sa)
        TitleStr = 'JONSWAP Spectrum'
        L1Str = f'Vwind @10m ASL = {Vw10} [m/s], Fetch = {fetch / 1000} [km]'
    elif SpecType == 7: #JONSWAP (gamma, Hs, w0)
        Hs = Par[0]
        w0 = Par[1]
        gamma = Par[2]
        g = 9.81
        alpha = 0.2 * (Hs**2) * (w0**4) / g**2
        if gamma < 1 or gamma > 7:
            if gamma != 0:
                # Display warning if gamma is outside validity range and not
                # set to zero
                print('Warning: gamma value in wave_spectrum function outside validity range, using DNV formula')
            k = 2 * (np.pi) / (w0*Hs**0.5)
            if k<= 3.6:
                gamma = 5
            elif k<= 5.0:
                gamma = np.exp(5.75 - 1.15*k)
            else:
                gamma = 1
        for k in range(len(W)):
            if W[k] < w0:
                sigma = 0.07
            else:
                sigma = 0.09
            S1 = alpha * g**2 * (W[k]**-5) * np.exp(-(5 / 4) * (w0 / W[k])**4)
            S2 = gamma**(np.exp(-(W[k] - w0)**2 / (2 * (sigma * w0)**2)))
            Conv_factor = 1-0.287*np.log(gamma)
            Sa = S1 * S2 * Conv_factor
            S.append(Sa) 
        TitleStr = 'JONSWAP Spectrum'
        L1Str = f'gamma = {gamma} , Hs = {Hs}, [m], w0 = {w0} [rad/s]'
    elif SpecType == 8: # Torsethaugen (Hs, w0)
        Hs = Par[0]
        w0 = Par[1]
        N = len(W)
        wmax = np.max(W)
        S = torset_spec(Hs, w0, W)  # See function below
        TitleStr = 'Torsethaugen Spectrum'
        L1Str = f'Hs = {Hs} [m], w0 = {w0} [rad/s]'
    else:
        print('Wrong spectrum type identifier, SpecType=1,2,..,8')
        return
    
    if PlotFlag:
        plt.plot(W, S, 'r', linewidth=1)
        plt.title(TitleStr)
        plt.legend([L1Str])
        plt.xlabel('ω [rad/s]')
        plt.ylabel('S(ω) [m^2 s]')
        plt.show()
    return S

def torset_spec(Hs,wo,omg):
#
# The Torsethaugen spectrum is an empirical two peaked spectrum for swell and 
# developing sea based on experimental data from the North Sea. For small peak
# frequencies, i.e.  0 < wmax <= 0.6 only one peak in the spectrum appears.
# Returns the spectral density function S of the Torsethaugen spectrum for 
# the frequencies:  0 < w < wmax (rad/s).
#
# Ouputs:
#   S     	- vector of power spectral densities (m^2s)
#
# Inputs:
#   Hs    	- significant wave height (m) - mean of the ones third highest waves
#   wo    	- peak frequency (rad/s)
#   omg  	- vector of frequencies at which to calculate S
#
# Ref: K.Torsethaugen (1996): "Model for a Doubly Peaked Wave Spectra"
#      Sintef report no.: STF22 A96204 prepared for Norsk Hydro.
#
# Author:     G. Kleiven, Norsk Hydro 
# Date:       2000-06-15
# Revisions:  2001-07-06,Svein I. Sagatun, Norsk Hydro - minor revisions
#             2001-10-14,Thor I. Fossen - IO compatible with the GNC toolbox
#	          2005-03-12 �yvind Smogeli - Revised to comply with MSS, added output consistency test
#             2007-10-08 �yvind Smogeli - Bug fix for scaling of spectrum magnitude

#---------------------------------------------------------------------------
# source code: Norsk Hydro
#---------------------------------------------------------------------------
    Tp = 2 * np.pi / wo  # peak period (s)
    f2pii = 2 * np.pi
    fwtp = f2pii / Tp
    Nfrq = len(omg)

    # Hs must be positive
    if Hs > 0:
        # Parameters
        af = 6.6
        ae = 2.0
        au = 25
        a10 = 0.7
        a1 = 0.5
        kg = 35.0
        kg0 = 3.5
        kg1 = 1.0
        r = 0.857
        k0 = 0.5
        k00 = 3.2
        m0 = 4.0
        b1 = 2.0
        a20 = 0.6
        a2 = 0.3
        a3 = 6.0
        s0 = 0.08
        s1 = 3.0
        b2 = 0.7
        b3 = 3.0
        sigma_a2 = 2 * 0.07**2
        sigma_b2 = 2 * 0.09**2
        tf = af * Hs**(1.0/3)

        if Tp < tf:
            # Predominant wind sea peak
            tl = ae * (Hs**0.5)
            eps1 = (tf - Tp) / (tf - tl)
            rpw = (1 - a10) * np.exp(-((eps1 / a1)**2)) + a10
            hsw = rpw * Hs
            hss = np.sqrt(1.0 - rpw**2) * Hs
            tpw = Tp
            tps = tf + b1
            sp = ((f2pii / 9.81) * hsw / (Tp**2))
            gammaw = kg * (1 + kg0 * np.exp(-Hs / kg1)) * (sp**r)
            gammas = 1.0
            nw = k0 * np.sqrt(Hs) + k00
            mw = m0
            ns = nw
            ms = mw
            if ms < 1:
                ms = 1
            g_argw = (nw -1)/mw
            g_args = (ns -1)/ms
            if g_args < 0:
                g0s = 1.0/((1.0/ms)*np.euler_gamma(g_args)*((ns/ms)**(-g_args)))
            else:
                g0s = 1.0/((1.0/ms)*np.euler_gamma(g_args)/((ns/ms)**(-g_args)))
            if g_argw < 0:
                g0w = 1.0/((1.0/mw)*np.euler_gamma(g_argw)*((nw/mw)**(-g_argw)))
            else:
                g0w = 1.0/((1.0/mw)*np.euler_gamma(g_argw)/((nw/mw)**(-g_argw)))
            a1m = 4.1
            b1m = 2.0*(mw**0.28)-5.3
            c1m = -1.45*(mw**0.1)+0.96
            a2m = 2.2/(mw**3.3)+0.57
            b2m = -0.58*mw**0.37+0.53
            c2m = -1.04/(mw**1.9)+0.94
            if c1m < 0:
                f1w = a1m / (nw-b1m)**(-c1m)
            else:
                f1w = a1m * (nw-b1m)**c1m
            if b2m < 0:
                f2w = a2m / nw**(-b2m) + c2m
            else:
                f2w = a2m * nw**(b2m) + c2m
            b1m = 2.0*(ms**0.28)-5.3
            c1m = -1.45*(ms**0.1)+0.96
            a2m = 2.2/(ms**3.3)+0.57
            b2m = -0.58*ms**0.37+0.53
            c2m = -1.04/(ms**1.9)+0.94
            if c1m < 0:
                f1s = a1m / (ns-b1m)**(-c1m)
            else:
                f1s = a1m * (ns-b1m)**c1m
            if b2m < 0:
                f2s = a2m / ns**(-b2m) + c2m
            else:
                f2s = a2m * ns**(b2m) + c2m
            
            agammaw = (1+f1w*np.log(gammaw)^(f2w))/gammaw
            agammas = (1+f1s*np.log(gammas)^(f2s))/gammas
        else:
            #----------------------------------------------------------------------------------------------------------------
            # Predominant swell peak:
            #--------------------------------------------------------------------------
            tu = au
            epsu = (Tp-tf)/(tu-tf)
            rps = (1.-a20)*np.exp(-(epsu/a2)**2)+a20
            hss = rps*Hs
            hsw = np.sqrt(1.-rps**2)*Hs
            tps = Tp
            ns = k0*np.sqrt(Hs)+k00
            ms = m0
            nw = ns
            mw = m0*(1-b2*np.exp(-Hs/b3))
            s4 = s0*(1-np.exp(-Hs/s1))
            g_argw = (nw-1)/mw
            g_args = (ns-1)/ms
            if g_args < 0:
                g0s = 1./((1./ms)*np.euler_gamma(g_args)*((ns/ms)**(-g_args)))
            else:
                g0s = 1./((1./ms)*np.euler_gamma(g_args)/((ns/ms)**(g_args)))
            if g_argw < 0:
                g0w = 1./((1./mw)*np.euler_gamma(g_argw)*((nw/mw)**(-g_argw)))
            else:
                g0w = 1./((1./mw)*np.euler_gamma(g_argw)/((nw/mw)**(g_argw)))
            tpw = ((g0w*hsw**2)/(16*s4*(0.4**nw)))**(1./(nw-1.))
            sf = ((f2pii/9.81)*Hs/(tf**2))
            gammaw = 1.
            gamma_f = kg*(1+kg0*np.exp(-Hs/kg1))*sf**r
            gammas = gamma_f*(1.+a3*epsu)
            a1m = 4.1
            b1m = 2.0*(mw**0.28)-5.3
            c1m = -1.45*(mw**0.1)+0.96
            a2m = 2.2/(mw**3.3)+0.57
            b2m = -0.58*(mw**0.37)+0.53
            c2m = -1.04/(mw**1.9)+0.94
            if c1m < 0:
                f1w = a1m / (nw-b1m)**(-c1m)
            else:
                f1w = a1m * (nw-b1m)**c1m
            if b2m < 0:
                f2w = a2m / nw**(-b2m) + c2m
            else:
                f2w = a2m * nw**(b2m) + c2m
            b1m = 2.0*(ms**0.28)-5.3
            c1m = -1.45*(ms**0.1)+0.96
            a2m = 2.2/(ms**3.3)+0.57
            b2m = -0.58*(ms**0.37)+0.53
            c2m = -1.04/(ms**1.9)+0.94
            if c1m < 0:
                f1s = a1m / (ns-b1m)**(-c1m)
            else:
                f1s = a1m * (ns-b1m)**c1m
            if b2m < 0:
                f2s = a2m / ns**(-b2m) + c2m
            else:
                f2s = a2m * ns**(b2m) + c2m
            agammaw = (1+f1w*np.log(gammaw)**(f2w))/gammaw
            agammas = (1+f1s*np.log(gammas)**(f2s))/gammas
        
        fdenorm_s = (tps-(hss**2))/16
        fdenorm_w = (tpw-(hsw**2))/16

        #==================================================================
        # Estimates spectral density for each frequency in array omg:
        #===================================================================

        f = omg / f2pii
        #-------------------------------------------------------------------
        #Wind sea contribution:
        #-------------------------------------------------------------------
        fnw = f * tpw
        in_val = np.max(np.where(fnw < 1))
        ftest1 = np.zeros(Nfrq)
        ftest1[:in_val] = np.exp(-(((fnw[:in_val] - 1) ** 2) / sigma_a2))
        ftest1[in_val:Nfrq] = np.exp(-(((fnw[in_val:Nfrq] - 1) ** 2) / sigma_b2))
        gamma_wf = np.power(gammaw, ftest1)
        gamma_ws_1 = np.power(fnw, -nw)
        gamma_ws_2 = np.exp(-(nw / mw) * np.power(fnw, -mw))
        gamma_ws = gamma_ws_1 * gamma_ws_2
        sw = g0w * agammaw * gamma_ws * gamma_wf * fdenorm_w / (2 * np.pi)
        #-------------------------------------------------------------------
        #Swell contribution:
        #-------------------------------------------------------------------
        fns = f * tps
        is_val = np.max(np.where(fns < 1))
        ftest2 = np.zeros(Nfrq)
        ftest2[:is_val] = np.exp(-(((fns[:is_val] - 1) ** 2) / sigma_a2))
        ftest2[is_val:Nfrq] = np.exp(-(((fns[is_val:Nfrq] - 1) ** 2) / sigma_b2))
        gamma_sf = np.power(gammas, ftest2)
        gamma_ss_1 = np.power(fns, -ns)
        gamma_ss_2 = np.exp(-(ns / ms) * np.power(fns, -ms))
        gamma_ss = gamma_ss_1 * gamma_ss_2
        ss = g0s * agammas * gamma_ss * gamma_sf * fdenorm_s / (2 * np.pi)
        #-----------------------------------------------------------------------------
        #Estimates spectral-density Sf(m^2*s)
        #-----------------------------------------------------------------------------
        S = sw + ss  # frq. in Hz
    else:
        S = np.zeros(len(omg))
    # Check that the output is real, if not the input is beyond the validity range
    if np.sum(np.imag(S)) != 0:
        S = np.zeros(np.shape(omg))
        print('Torsethaugen spectrum input outside validity range in wave_spectrum, complex output set to zero')
    return S.T