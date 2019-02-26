
dx = 0.125
dy = 2.
dt = 0.124
nx = 128*20
ny = 320
Lx = nx * dx
Ly = ny * dy
npatch_x = 256
laser_fwhm = 40.
laser_waist = 200.

Main(
    geometry = "2Dcartesian",
    interpolation_order = 2,
    timestep = dt,
    simulation_time = int(Lx/dt)*dt*30, #Laser propagates over 10 grid length
    #simulation_time = int(Lx/dt)*dt*2., #Laser propagates over 10 grid length
    cell_length  = [dx, dy],
    grid_length = [ Lx, Ly ],
    number_of_patches = [npatch_x, 32],
    clrw = nx/npatch_x,
    EM_boundary_conditions = [
        ["silver-muller","silver-muller"],
        ["silver-muller","silver-muller"],
    ],
    solve_poisson = False,
    print_every = 100,
    random_seed = smilei_mpi_rank
)

MovingWindow(
    #time_start = 0.,
    time_start = Main.grid_length[0],
    velocity_x = 1.
    #velocity_x = 0.
)

#LoadBalancing(
#    initial_balance = False,
#    every = 20,
#    cell_load = 1.,
#)

Species( 
    name = "electron",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell = 9,
    c_part_max = 1.0,
    mass = 1.0,
    charge = -1.0,
    charge_density = trapezoidal(0.003, xvacuum=0., xplateau=1000000000, xslope1=1000.),
    mean_velocity = [0.0, 0.0, 0.0],
    pusher = "boris",    
    time_frozen = 0.0,
    boundary_conditions = [
        ["remove", "remove"],
        ["remove", "remove"],
    ],
)

LaserGaussian2D(
    box_side         = "xmin",
    a0              = 4.,
    focus           = [0., Main.grid_length[1]/2.],
    waist           = laser_waist,
    time_envelope   = tgaussian(center=3*laser_fwhm, fwhm=laser_fwhm)
)

## LASER -------------------------------------------------------------------------
#laser_FWHM_E             = laser_fwhm
#laser_focus_x          = Main.grid_length[0]
#laser_initial_position = Main.grid_length[0] - 2 * laser_FWHM_E
#waist                  = laser_waist
#a0                     = 6.
#
################################## Laser field, from external fields
#
#focus = [laser_focus_x, Main.grid_length[1]/2.]
#
#c_vacuum = 1.
#dx = Main.cell_length[0]
#dy = Main.cell_length[1]
#dt = Main.timestep
#
#omega       = 1.
#Zr          = omega * waist**2/2.  # Rayleigh length
#
## time gaussian function
#def time_gaussian(fwhm, center, order=2):
#    import math
#    import numpy as np
#    sigma = (0.5*fwhm)**order/math.log(2.0)
#
#    def f(t):
#        return np.exp( -(t-center)**order / sigma )
#
#    return f
#
#
#time_envelope_t              = time_gaussian(center=laser_initial_position                  , fwhm=laser_FWHM_E)
#time_envelope_t_plus_half_dt = time_gaussian(center=(laser_initial_position+c_vacuum*0.5*dt), fwhm=laser_FWHM_E)
#
## laser waist function
#def w(x):
#        import numpy as np
#        w  = np.sqrt(1./(1.+   ( (x-focus[0])/Zr  )**2 ) )
#        return w
#
#def coeff(x):
#        import numpy as np
#        coeff = omega * (x-focus[0]) * w(x)**2 / (2.*Zr**2)
#        return coeff
#
#def spatial_amplitude(x,y):
#        import numpy as np
#        invWaist2 = (w(x)/waist)**2
#        return w(x) * np.exp( -invWaist2*(  (y-focus[1])**2 )  )
#
## laser phase   
#def phase(x,y):
#        import numpy as np
#        return coeff(x) * ( (y-focus[1])**2 )
#
#def Gouy_phase(x):
#        import numpy as np
#        return np.arctan(   (x-focus[0]) / Zr     )
#
#def space_envelope(x,y):
#        import numpy as np
#        return a0 * spatial_amplitude(x,y) * np.exp(1j*phase(x,y)) * np.exp(-1j*Gouy_phase(x))
#
#def complex_exponential_comoving(x,t):
#        import numpy as np
#        csi = x-c_vacuum*t-laser_initial_position # comoving coordinate
#        return np.exp(1j*csi)
#
#### Electromagnetic field
## Electric field        
#def Ex(x,y):
#        import numpy as np
#        invWaist2 = (w(x)/waist)**2
#        complexEx = 2.* (y-focus[1]) * invWaist2 * space_envelope(x,y) * complex_exponential_comoving(x,0.)
#        return np.multiply(np.real(complexEx),time_envelope_t(x))
#
#def Ey(x,y):
#        import numpy as np
#        complexEy  = 1j * space_envelope(x,y) * complex_exponential_comoving(x,0)
#        return np.multiply(np.real(complexEy),time_envelope_t(x))
#
#
#def Ez(x,y):
#        import numpy as np
#        return np.zeros(shape=np.shape(x))
#
## Magnetic field
#def Bx(x,y):
#        import numpy as np
#        invWaist2 = (w(x)/waist)**2
#        complexBx = 2.* invWaist2 * space_envelope(x,y) * complex_exponential_comoving(x,dt/2.)
#        return np.multiply(np.real(complexBx),time_envelope_t_plus_half_dt(x))
#
#def By(x,y):
#        import numpy as np
#        return np.zeros(shape=np.shape(x))
#
#def Bz(x,y):
#        import numpy as np
#        complexBz = 1j * space_envelope(x,y) * complex_exponential_comoving(x,dt/2.)
#        return np.multiply(np.real(complexBz),time_envelope_t_plus_half_dt(x))
#
#
#
#field_profile = {'Ex': Ex, 'Ey': Ey, 'Ez': Ez, 'Bx': Bx, 'By': By, 'Bz': Bz}
#
#for field in ['Ex', 'Ey', 'Ez', 'Bx', 'By', 'Bz']:
#        ExternalField(
#                field = field,
#                profile = field_profile[field],
#        )
#
#
################################################################################

Checkpoints(
    dump_step = 0,
    dump_minutes = 0.0,
    exit_after_dump = False,
)

#list_fields = ['Ex','Ey','Rho','Jx']
#
#DiagFields(
#    every = 500,
#    fields = list_fields
#)

DiagProbe(
    every = 100,
    origin = [0., Main.grid_length[1]/2.],
    corners = [
        [Main.grid_length[0], Main.grid_length[1]/2.],
    ],
    number = [nx],
    fields = ['Ex','Ey','Rho','Jx']
)

DiagProbe(
    every = 100,
    origin = [0., 0.],
    vectors = [[Lx,0], [0,Ly]],
    number = [nx,ny],
    fields = ['Ex','Ey','Rho','Jx']
)

#DiagScalar(
#    every = 100,
#    vars=[
#        'Uelm','Ukin_electron',
#        'ExMax','ExMaxCell','EyMax','EyMaxCell','RhoMin','RhoMinCell',
#        'Ukin_bnd','Uelm_bnd','Ukin_out_mvw','Ukin_inj_mvw','Uelm_out_mvw','Uelm_inj_mvw'
#    ]
#)

DiagParticleBinning(
    deposited_quantity = "weight",
    every = 500,
    species = ["electron"],
    axes = [
        ["moving_x", 0, Lx, 300],
        ["ekin", 1, 400, 100]
    ]
)

DiagPerformances(
    every = 100,
    patch_information = False,
)
