##################################################################
### SOLVING SIMPLE RATE EQUATIONS FOR THE IONIZATION OF CARBON ###
##################################################################

from numpy import array, arange, zeros, pi, exp, sqrt, sin, vectorize
from math import gamma as math_gamma
math_gamma = vectorize(math_gamma)

def solve_rate_eqs_( namelist ):

    # control parameter
    tiny = 1.e-18
    
    # conversion factor (between code units & atomic units)
    w_ref    = namelist.Main.reference_angular_frequency_SI
    Lmu      = 2.*pi * 3.e8/(w_ref*1.e-6)
    au_to_w0 = 4.134137172e+16 / w_ref
    Ec_to_au = 3.314742578e-15 * w_ref
    
    # laser
    aL  = max( namelist.Laser[0].space_envelope[0], namelist.Laser[0].space_envelope[1] )
    Eau = aL * Ec_to_au
    laser_time_envelope = namelist.Laser[0].time_envelope
    
    # PIC time-teps
    dt = namelist.Main.timestep
    nt = int(namelist.Main.simulation_time / dt)
    print('********** ')
    print('- [theory] dt = '+str(dt / w_ref * 1.0e15)+' fs')
    print(' ')
    
    # Carbon atom properties
    Zat = namelist.Species[0].atomic_number
    Z   = arange(0, Zat)
    Ip  = array([11.2602, 24.3845, 47.8877, 64.4935, 392.0905, 489.9931])/27.2114
    l   = array([1,1,0,0,0,0])
    
    nstar = (Z+1.) * sqrt(1./2./Ip)
    cst   = 2. * nstar
    alpha = cst - 1.
    beta  = 2.**(cst-1.)/cst/math_gamma(cst) * (8.*l+4.) * Ip * au_to_w0
    gamma = 2.*(2.*Ip)**1.5
    Wadk  = sqrt(6./pi) * beta * (gamma/Eau)**(cst-1.5) * exp(-1./3. * gamma/Eau)
    
    # Preparing arrays
    t    = zeros(nt)
    E    = zeros(nt)
    n    = zeros([Zat+1,nt]); n[0,0]=1.
    Wint = zeros(Zat)
    Env  = zeros(nt)
    
    # Solving the rate equations numerically
    for it in range(1,nt):
        t[it]   = it*dt
        E[it]   = aL*sin(t[it]) * laser_time_envelope(t[it])
        Env[it] = laser_time_envelope(t[it])
    
        # neutral atom
        delta  = gamma[0]/( abs(E[it])*Ec_to_au)
        if (delta>tiny):
            W        = beta[0] * delta**alpha[0] * exp(-delta/3.)
            Wint[0] += W
            n[0,it]  = (1.-W*dt/2.)/(1.+W*dt/2.) * n[0,it-1]
    
        # from charge 1 to charge Zat-1
        for Z in range(1,Zat):
            deltam    = gamma[Z-1]/( abs(E[it])*Ec_to_au) 
            deltap    = gamma[Z]  /( abs(E[it])*Ec_to_au) 
            if (deltam>tiny) and (deltap>tiny):
                Wm       = beta[Z-1] * (deltam)**alpha[Z-1] * exp(-deltam/3.)
                Wp       = beta[Z  ] * (deltap)**alpha[Z  ] * exp(-deltap/3.)
                Wint[Z] += Wp
                n[Z,it]  = (1.-Wp*dt/2.)/(1.+Wp*dt/2.)*n[Z,it-1] + Wm*dt/(1.+Wm*dt/2.)*n[Z-1,it-1]
    
        # last charge state
        delta = gamma[Zat-1]/( abs(E[it])*Ec_to_au)
        if (delta>tiny):
            W          = beta[Zat-1] * (delta)**alpha[Zat-1] * exp(-delta/3.)
            n[Zat,it]  = n[Zat,it-1]+W*dt/(1.+W*dt/2.)*n[Zat-1,it-1]
    
    # Compare ionisation rates
    Wint = Wint/nt
    for Z in range(Zat):
        print('- [theory] Z ='+str(Z)+'->'+str(Z+1)
              +'    Wadk='+str(Wadk[Z]* w_ref)
              +'    W   ='+str(Wint[Z] * w_ref)
        )
    
    nsum = sum( n[:,-1] )
    print(' ')
    print('- [theory] test cons. part. nb:'+str(nsum))
    print('********** ')
    
    return t, n, Env

