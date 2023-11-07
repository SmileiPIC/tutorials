###### Laser Wakefield Acceleration tutorial in Azimuthal Modes cylindrical geometry
import math 
import numpy as np
import scipy.constants 

##### Physical constants
lambda0             = 0.8e-6                    # reference length, m - here it will be our plasma wavelength
c                   = scipy.constants.c         # lightspeed, m/s
omega0              = 2*math.pi*c/lambda0       # reference angular frequency, rad/s
eps0                = scipy.constants.epsilon_0 # Vacuum permittivity, F/m
e                   = scipy.constants.e         # Elementary charge, C
me                  = scipy.constants.m_e       # Electron mass, kg
ncrit               = eps0*omega0**2*me/e**2    # Plasma critical number density, m-3
c_over_omega0       = lambda0/2./math.pi        # converts from c/omega0 units to m
reference_frequency = omega0                    # reference frequency, s-1
E0                  = me*omega0*c/e             # reference electric field, V/m
electron_mass_MeV   = scipy.constants.physical_constants["electron mass energy equivalent in MeV"][0]


##### Variables used for unit conversions
c_normalized        = 1.                        # speed of light in vacuum in normalized units
um                  = 1.e-6/c_over_omega0       # 1 micron in normalized units
mm                  = 1.e-3/c_over_omega0       # 1 millimetre in normalized units
fs                  = 1.e-15*omega0             # 1 femtosecond in normalized units
mm_mrad             = um                        # 1 millimetre-milliradians in normalized units
pC                  = 1.e-12/e                  # 1 picoCoulomb in normalized units
MeV                 = 1./electron_mass_MeV      # 1 MeV in normalized units


##### Mesh and time evolution
dx                  = (lambda0/1e-6)*um/30      # longitudinal resolution
dr                  = 0.4*um                    # radial resolution

nx                  = 1536                      # number of grid points in the longitudinal direction
nr                  = 80                        # number of grid points in the radial direction

Lx                  = nx * dx                   # longitudinal size of the simulation window
Lr                  = nr * dr                   # radial size of the simulation window, which goes from r=0 to r=Lr

npatch_x            = 256

dt                  = 0.98*dx/c_normalized      # integration timeestep
Niterations         = 15000


##### Boundary conditions
EM_boundary_conditions  = [["PML","PML"],["PML","PML"],]
#EM_boundary_conditions = [ ["silver-muller","silver-muller"],["buneman","buneman"],]

##### B-TIS3 interpolation to cope with numerical Cherenkov radiation
use_BTIS3_interpolation = False

Main(
    geometry                       = "AMcylindrical",
    number_of_AM                   = 2,
    timestep                       = dt,
    simulation_time                = Niterations*dt, 
    cell_length                    = [dx, dr],
    grid_length                    = [Lx, Lr],
    number_of_patches              = [npatch_x, 8],
    EM_boundary_conditions         = EM_boundary_conditions,
    number_of_pml_cells            = [[20,20],[20,20]],     
    solve_poisson                  = False,
    print_every                    = 100,
    random_seed                    = smilei_mpi_rank,
    use_BTIS3_interpolation        = use_BTIS3_interpolation,
    reference_angular_frequency_SI = omega0,
)

#### Define the plasma

# The physics of interest in this case is near the axis, 
# so no need to radially fill all the window with plasma

density_plateau_cm_minus_3  = 3.e18
density_plateau_normalized  = density_plateau_cm_minus_3*1.e6/ncrit # convert to meters and then normalize
Radius_plasma               = 140.*um


upramp_length               = 100.*um
shock_downramp_length       = 30. *um
plateau_length              = 3.  *mm
downramp_length             = 100.*um

x_start_plasma              = Lx
x_density_transition_peak   = x_start_plasma           +upramp_length
x_plateau                   = x_density_transition_peak+shock_downramp_length
x_end_plateau               = x_plateau                +plateau_length
x_end_plasma                = x_end_plateau            +downramp_length

longitudinal_profile        = polygonal(xpoints=[x_start_plasma,x_density_transition_peak,x_plateau,x_end_plateau,x_end_plasma], 
                                        xvalues=[0.,2.*density_plateau_normalized,density_plateau_normalized,density_plateau_normalized,0.])
                                                                                
def nplasma(x,r):
    profile_r = 0.
    if (r<Radius_plasma):
        profile_r = 1.
    return profile_r*longitudinal_profile(x,r)

if (use_BTIS3_interpolation == False):
    pusher = "boris"
else:
    pusher = "borisBTIS3"
      
Species( 
    name                    = "electron",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell      = 16,
    regular_number          = [2,1,8], # i.e. 2 macro-particles along x, 1 macro-particle along r and 8 along the theta angle between 0 and 2*pi
    c_part_max              = 1.0,
    mass                    = 1.0,
    charge                  = -1.0,
    charge_density          = nplasma,
    mean_velocity           = [0.0, 0.0, 0.0],
    pusher                  = pusher,  
    time_frozen             = 0.0,
    boundary_conditions     = [["remove", "remove"],["reflective", "remove"],],
)


#### Define the laser

# this is the FWHM in intensity, i.e. sqrt(2) times larger than the FWHM in intensity  measured in experiments
laser_fwhm                  = 16.*fs  
laser_waist                 = 15.*um
t_laser_peak_enters_window  = 3*laser_fwhm

# Define a Gaussian beam linearly polarized on the y axis 
# (default polarization angle=0, default polarization=linear)
LaserGaussianAM(
    box_side                = "xmin",
    a0                      = 3.,
    focus                   = [0., 0.],
    waist                   = laser_waist,
    time_envelope           = tgaussian(center=t_laser_peak_enters_window, fwhm=laser_fwhm)
)

#### Define a CurrentFilter
# CurrentFilter(
#     model                   = "binomial",
#     passes                  = [2],
# )

#### Define the moving window

# this corresponds to the time needed by the laser to arrive where
# we want it after the moving window starts to move,
# i.e. in this case at a distance of 1.8*laser_fwhm from the right border 
time_start_moving_window    = (Lx-1.8*laser_fwhm)+t_laser_peak_enters_window

MovingWindow(
    time_start              = time_start_moving_window,
    velocity_x              = c_normalized
)

#### Define the grid diagnostics

DiagFields(
    every                   = int(50*um/dt),
    fields                  = ['El','Er','Rho']
)


fields_probes               = ['Ex','Ey','Rho','Bz']

if (use_BTIS3_interpolation == True):
    fields_probes.append("BzBTIS3")

# 1D Probe defined on a line parallel to the axis of propagation,
# at a distance sqrt(2)*dr from the axis.
# A Probe placed on the axis would be very noisy
DiagProbe(
    every                   = int(50*um/dt),
    origin                  = [0., 1*dr, 1*dr],
    corners                 = [[nx*dx, 0, 0],],
    number                  = [nx],
    fields                  = fields_probes
 )
 
# 2D Probe, defined on the plane parallel to the polarization axis of the laser, i.e. the xy plane
DiagProbe(
    every                   = int(50*um/dt),
    origin                  = [0., -nr*dr,0.],
    corners                 = [ [nx*dx,-nr*dr,0.], [0,nr*dr,0.] ],
    number                  = [nx, 2*nr],
    fields                  = fields_probes
)


## TrackParticle diagnostic
def my_filter(particles):
    return ((particles.px>10*MeV/c_normalized))

DiagTrackParticles(
 species = "electron",
 every = int(100*um/dt),
 filter = my_filter,
 attributes = ["x", "y", "z", "px", "py", "pz", "w"]
)
