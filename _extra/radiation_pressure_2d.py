from math import pi

### Choice 1: Physical Inputs in normalized units ########################

# laser wavelength and period
l0           = 2*pi    # laser wavelength in normalized units
t0           = 2*pi    # optical cycle duration in normalized units
# Grid size and total simulated time
Lx           = 6.*l0
Ly           = 10.*l0
Tsim         = 10.*t0   # duration of the simulation

# ### Choice 2: Physical Inputs in normalized units, converted from SI units #######
# 
# from scipy.constants import c, epsilon_0, e, m_e # constants in SI units
# wavelength_SI  = 0.8e-6 # laser wavelength, m
# # Normalization quantities
# L_r     = wavelength_SI       # reference length is the wavelength
# T_r     = L_r / c             # reference time
# omega_r = 2*pi*c/L_r          # reference angular frequency
# # Laser wavelength and period in normalized units
# l0 = wavelength_SI / L_r
# t0 = wavelength_SI/c / T_r
# # Grid size and total simulated time in normalized units
# Lx   = 6. *wavelength_SI / L_r
# Ly   = 10.*wavelength_SI / L_r
# Tsim = 10.*wavelength_SI/c / T_r   # duration of the simulation


####################  Simulated domain and time interval #######################
# Spatial and temporal resolution
resx         = 100.                     # nb of cells in one laser wavelength
rest         = 150.                     # nb of timesteps in one optical cycle 
# Mesh and integration timestep
dx           = l0/resx
dy           = l0/resx
dt           = t0/rest

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
# E_r         = me*omega_r*c/e            # Reference electric field, V/m

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
# N_r          = eps0*omega0**2*me/e**2 # Reference density, m-3
n0             = 100         # initial plasma density, normalized units
vacuum_length  = l0          # distance between Xmin and the plasma, normalized units
plateau_length = 0.44*l0     # length of plateau of plasma density profile, normalized units

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
