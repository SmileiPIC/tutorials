###### Namelist for plasma wake excited by a relativistic electron bunch

import math 
import numpy as np
import scipy.constants

##### Physical constants
lambda0             = 0.8e-6                    # reference length, m
c                   = scipy.constants.c         # lightspeed, m/s
omega0              = 2*math.pi*c/lambda0       # laser angular frequency, rad/s
eps0                = scipy.constants.epsilon_0 # Vacuum permittivity, F/m
e                   = scipy.constants.e         # Elementary charge, C
me                  = scipy.constants.m_e       # Electron mass, kg
ncrit               = eps0*omega0**2*me/e**2    # reference density, m-3
c_over_omega0       = lambda0/2./math.pi        # converts from c/omega0 units to m
reference_frequency = omega0                    # reference frequency, s-1
E0                  = me*omega0*c/e             # reference electric field, V/m

##### Variables used for unit conversions
c_normalized        = 1.                        # speed of light in vacuum in normalized units
um                  = 1.e-6/c_over_omega0       # 1 micron in normalized units
fs                  = 1.e-15*omega0             # 1 femtosecond in normalized units
mm_mrad             = um                        # 1 millimeter-milliradians in normalized units
pC                  = 1.e-12/e                  # 1 picoCoulomb in normalized units

npatch_x = 64

##### Mesh parameters
dx = 0.05*um
dr = 0.12*um
dt = 0.8*dx/c_normalized
nx = 640
nr = 320
Lx = nx * dx
Lr = nr*dr

Main(
    geometry = "AMcylindrical",

    interpolation_order = 2,
   
    number_of_AM = 1,

    timestep = dt,
    simulation_time = dt*5000., #int(1*Lx/dt)*dt,

    cell_length  = [dx, dr],
    grid_length = [ Lx,  Lr],

    number_of_patches = [npatch_x, 32],
    
    EM_boundary_conditions = [
        ["silver-muller","silver-muller"],
        ["buneman","buneman"],
    ],

    solve_poisson = False,
    
    solve_relativistic_poisson = True,
    
    print_every = 100,

    random_seed = smilei_mpi_rank
)

MovingWindow(
    time_start = 0.,
    velocity_x = 1.
)

LoadBalancing(
    initial_balance = False,
        every = 20,
    cell_load = 1.,
    frozen_particle_load = 0.1
)

# Plasma parameters
n0 = 3.e24/ncrit  # density, converted from m-3
Radius_plasma = 20.*um
longitudinal_profile = polygonal(xpoints=[30.*um,35.*um,1e4*um,1e4*um],xvalues=[0.,n0,n0,0.])
def nplasma(x,r):
    profile_r = 0.
    if (r**2<Radius_plasma**2):
        profile_r = 1.
    return profile_r*longitudinal_profile(x,r)

Species(
    name = "electron",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell = 4,
    regular_number = [2,2,1],
    c_part_max = 1.0,
    mass = 1.0,
    charge = -1.0,
    charge_density = nplasma,
    mean_velocity = [0.0, 0.0, 0.0],
    temperature = [0.,0.,0.],
    pusher = "boris",
    time_frozen = 0.0,
    boundary_conditions = [
       ["remove", "remove"],
       ["remove", "remove"],
    ],
)


##### electron bunch parameters

# Bunch position and rms dimensions (gaussian density distribution)
Q_bunch                    = -50*pC                          # Total charge of the electron bunch
sigma_x                    = 2.*um                          # initial longitudinal rms size
sigma_r                    = 2.*um                            # initial transverse/radial rms size (cylindrical symmetry)
bunch_energy_spread        = 0.01                            # initial rms energy spread / average energy (not in percent)
bunch_normalized_emittance = 4.*mm_mrad                      # initial rms emittance, same emittance for both transverse planes
center_bunch               = 20.*um                # initial position of the electron bunch in the window   
gamma_bunch                = 200.                            # initial relativistic Lorentz factor of the bunch

npart                      = 50000                           # number of computational macro-particles to model the electron bunch 
normalized_species_charge  = -1                              # For electrons
Q_part                     = Q_bunch/npart                   # charge for every macroparticle in the electron bunch
weight                     = Q_part/((c/omega0)**3*ncrit*normalized_species_charge)

#### initialize the bunch using numpy arrays
#### the bunch will have npart particles, so an array of npart elements is used to define the x coordinate of each particle and so on ...
array_position = np.zeros((4,npart))                         # positions x,y,z, weight
array_momentum = np.zeros((3,npart))                         # momenta x,y,z

#### The electron bunch is supposed at waist. To make it convergent/divergent, transport matrices can be used
array_position[0,:] = np.random.normal(loc=center_bunch, scale=sigma_x, size=npart)                        # generate random number from gaussian distribution for x position
array_position[1,:] = np.random.normal(loc=0., scale=sigma_r, size=npart)                                  # generate random number from gaussian distribution for y position
array_position[2,:] = np.random.normal(loc=0., scale=sigma_r, size=npart)                                  # generate random number from gaussian distribution for z position
array_momentum[0,:] = np.random.normal(loc=gamma_bunch, scale=bunch_energy_spread*gamma_bunch, size=npart) # generate random number from gaussian distribution for px position
array_momentum[1,:] = np.random.normal(loc=0., scale=bunch_normalized_emittance/sigma_r, size=npart)       # generate random number from gaussian distribution for py position
array_momentum[2,:] = np.random.normal(loc=0., scale=bunch_normalized_emittance/sigma_r, size=npart)       # generate random number from gaussian distribution for pz position

array_position[3,:] = np.multiply(np.ones(npart),weight)

Species(
    name = "bunch_electrons",
    position_initialization = array_position,
    momentum_initialization = array_momentum, 
    relativistic_field_initialization = True,
    c_part_max = 1.0,
    mass = 1.0,
    charge = -1.0,
    pusher = "boris",
    time_frozen = 0.0,
    boundary_conditions = [
       ["remove", "remove"],
       ["remove", "remove"],
    ],
)


# 1D Probe diagnostic on the x axis
DiagProbe(
        every = 500,
        origin = [0., 1.*dr, 1.*dr],
        corners = [
            [Main.grid_length[0], 2.*dr, 2.*dr]
        ],
        number = [nx],
        fields = ['Ex','Ey','Rho','Jx','Env_A_abs','Env_Chi','Env_E_abs']
)

##### 2D Probe diagnostics on the xy plane
DiagProbe(
    every = 500,
    origin   = [0., -nr*dr,0.],
    corners  = [ [nx*dx,-nr*dr,0.], [0,nr*dr,0.] ],
    number   = [nx, int(2*nr)],
    fields = ['Ex','Ey','Rho','Jx','Env_A_abs','Env_Chi','Env_E_abs']
)

# Energy density of the bunch
DiagParticleBinning(
    deposited_quantity = "weight",
    every = 1000,
    time_average = 1,
    species = ["bunch_electrons"],
    axes = [
        ["ekin", 100, 250., 1000]
    ]
)


# longitudinal phase space of the bunch
DiagParticleBinning(
    deposited_quantity = "weight",
    every = 1000,
    time_average = 1,
    species = ["bunch_electrons"],
    axes = [
        ["moving_x", 0., Lx, 200],
        ["ekin", 0.1, 250., 1000]
    ]
)

# Transverse (y) phase space of the bunch
DiagParticleBinning(
    deposited_quantity = "weight",
    every = 1000,
    time_average = 1,
    species = ["bunch_electrons"],
    axes = [
        ["y", -20, 20, 200],
        ["py", -20, 20, 200]
    ]
)

# Transverse (z) phase space of the bunch
DiagParticleBinning(
    deposited_quantity = "weight",
    every = 1000,
    time_average = 1,
    species = ["bunch_electrons"],
    axes = [
        ["z", -20, 20, 200],
        ["pz", -20, 20, 200]
    ]
)







