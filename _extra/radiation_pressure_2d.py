import math
import scipy.constants

### Choice 1: Physical Inputs in normalized units ########################

# laser wavelength and period
l0           = 2.0*math.pi               # laser wavelength in normalized units
t0           = l0                        # optical cycle duration in normalized units

# ### Choice 2: Physical Inputs in normalized units, converted from SI units #######
# 
# # Physical constants
# lambda_r     = 0.8e-6                    # Reference length, m
# c            = scipy.constants.c         # Lightspeed, m/s
# omega_r      = 2*math.pi*c/lambda_r      # Laser angular frequency, rad/s
# # Variables used for unit conversions
# c_normalized = 1.                        # Speed of light in vacuum in normalized units
# um           = 1.e-6/(c/omega_r )        # 1 micron in normalized units
# fs           = 1.e-15*omega_r            # 1 femtosecond in normalized units
# # Laser wavelength and period
# l0           = lambda_r*um
# t0           = (c_normalized/lambda_r*um)*fs


####################  Simulated domain and time interval #######################
# Spatial and temporal resolution
resx         = 100.                     # nb of cells in on laser wavelength
rest         = 150.                     # time of timestep in one optical cycle 
# Mesh and integration timestep
dx           = l0/resx
dy           = l0/resx
dt           = t0/rest
# Grid size and total simulated time
Lx           = 6.*l0      
Ly           = 10.*l0
Tsim         = 10.*t0                   # duration of the simulation

Main(
    geometry = "2Dcartesian",
    
    interpolation_order = 2 ,
    
    cell_length = [dx,dy],  # normalized units
    grid_length  = [Lx,Ly], # normalized units
    
    number_of_patches = [ 8, 8 ],
    
    timestep = dt,          # normalized units
    simulation_time = Tsim, # normalized units
     
    EM_boundary_conditions = [
        ['silver-muller'],
        ['periodic'],
    ],
    
    random_seed = smilei_mpi_rank
)

# laser parameters
laser_a0    = 150.        # normalized laser peak field
laser_waist = 2.0*l0      # laser waist
# eps0        = scipy.constants.epsilon_0 # Vacuum permittivity, F/m
# e           = scipy.constants.e         # Elementary charge, C
# me          = scipy.constants.m_e       # Electron mass, kg
# E0          = me*omega_r*c/e            # Reference electric field, V/m

LaserGaussian2D(
   box_side        = "xmin",
   omega           = 1.,              # normalized units
   a0              = laser_a0,        # normalized units
   focus           = [10.*l0, Ly/2.], # normalized units
   waist           = laser_waist,     # normalized units
   ellipticity     = 1.,              # circular polarization
   time_envelope   = ttrapezoidal(slope1=t0),
)

# plasma parameters
# n_ref          = eps0*omega0**2*me/e**2 # Reference density, m-3
n0             = 100                    # initial plasma density, normalized units
vacuum_length  = l0                     # distance between Xmin and the plasma, normalized units
plateau_length = 0.44*l0                # length of plateau of plasma density profile, normalized units

Species(
    name = 'ion',
    position_initialization = 'regular',
    momentum_initialization = 'cold',
    particles_per_cell = 4,
    mass = 1836., # normalized units
    charge = 1.,  # normalized units
    number_density = trapezoidal(n0,xvacuum=vacuum_length,xplateau=plateau_length),
    boundary_conditions = [
        ["reflective", "reflective"],
        ["periodic", "periodic"],
    ],
)
Species(
    name = 'eon',
    position_initialization = 'regular',
    momentum_initialization = 'mj',
    particles_per_cell = 4,
    mass = 1.,    # normalized units
    charge = -1., # normalized units
    number_density = trapezoidal(n0,xvacuum=vacuum_length,xplateau=plateau_length),
    temperature = [0.001], # normalized units
    boundary_conditions = [
        ["reflective", "reflective"],
        ["periodic", "periodic"],
    ], 
)

globalEvery = 75

DiagScalar(every=globalEvery)

DiagProbe(
    every = globalEvery,
    origin = [0., Main.grid_length[1]/2.],
    corners = [
        [Main.grid_length[0], Main.grid_length[1]/2.],
    ],
    number = [int(Lx/dx)],
    fields = ['Ex','Ey','Ez','Bx','By','Bz','Rho_ion','Rho_eon']
)

DiagFields(
    every = globalEvery,
    fields = ['Ex','Ey','Ez','Bx','By','Bz','Rho_ion','Rho_eon']
)
