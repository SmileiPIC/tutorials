############################# Input namelist for Laser Wakefield Acceleration 
############################# with ionization injection

import math 
import numpy as np
import scipy.constants


##### Physical constants
lambda0             = 0.8e-6                    # laser wavelength, m
c                   = scipy.constants.c         # lightspeed, m/s
omega0              = 2*math.pi*c/lambda0       # laser angular frequency, rad/s
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
fs                  = 1.e-15*omega0             # 1 femtosecond in normalized units
mm_mrad             = um                        # 1 millimeter-milliradians in normalized units
pC                  = 1.e-12/e                  # 1 picoCoulomb in normalized units
me_over_me          = 1.0                       # normalized electron mass
mp_over_me          = scipy.constants.proton_mass / scipy.constants.electron_mass  # normalized proton mass
mn_over_me          = scipy.constants.neutron_mass / scipy.constants.electron_mass # normalized neutron mass
MeV                 = 1./electron_mass_MeV      # 1 MeV in normalized units

#########################  Simulation parameters

##### mesh resolution
dx                  = 0.14*um                   # longitudinal mesh resolution
dr                  = 0.75*um                   # transverse mesh resolution
dt                  = 0.9*dx/c_normalized       # integration timestep

##### simulation window size
nx                  = 384                       # number of mesh points in the longitudinal direction
nr                  = 96                        # number of mesh points in the transverse direction
Lx                  = nx * dx                   # longitudinal size of the simulation window
Lr                  = nr * dr                   # transverse size of the simulation window

##### Total simulation time
T_sim               = 13001.*dt #3000.*dt

##### patches parameters (parallelization)
npatch_x            = 32
npatch_r            = 8


######################### Main simulation definition block

# Use True to activate a force interpolation scheme 
# that reduces the effects of the Numerical Cherenkov Radiation
use_BTIS3_interpolation            = False #True 

Main(
    geometry                       = "AMcylindrical",

    interpolation_order            = 2,

    timestep                       = dt,
    simulation_time                = T_sim,

    cell_length                    = [dx, dr],
    grid_length                    = [Lx, Lr],

    number_of_AM                   = 1,

    number_of_patches              = [npatch_x,npatch_r],

    EM_boundary_conditions         = [["silver-muller"],["PML"],],
    number_of_pml_cells            = [[0,0],[20,20]],
  
    solve_poisson                  = False,
    solve_relativistic_poisson     = False,
    
    print_every                    = 100,
    use_BTIS3_interpolation        = use_BTIS3_interpolation,

    random_seed                    = 0,
    reference_angular_frequency_SI = omega0,
)

######################### Define the laser pulse

#### laser parameters
a0                                 = 1.8
laser_fwhm                         = 25*math.sqrt(2)*fs                              # laser FWHM duration in field, i.e. FWHM duration in intensity*sqrt(2)
laser_waist                        = 16.*um                                            # laser waist, conversion from um
center_laser                       = Lx-1.7*laser_fwhm                                 # laser position at the start of the simulation
x_focus_laser                      = 500*um

#### Define a Gaussian Beam with Gaussian temporal envelope
LaserEnvelopeGaussianAM(
  a0                               = a0, 
  omega                            = (2.*math.pi/lambda0*c)/reference_frequency,       # laser frequency, normalized
  focus                            = [(Lx+x_focus_laser),0.],                          # laser focus, [x,r] position
  waist                            = laser_waist,                                      # laser waist
  time_envelope                    = tgaussian(center=center_laser, fwhm=laser_fwhm),  # time profile of the laser pulse
  envelope_solver                  = 'explicit_reduced_dispersion',
  Envelope_boundary_conditions     = [ ["reflective"],["PML"] ],
  Env_pml_sigma_parameters         = [[0.9 ,2     ],[80.0,2]     ,[80.0,2     ]],
  Env_pml_kappa_parameters         = [[1.00,1.00,2],[1.00,1.00,2],[1.00,1.00,2]],
  Env_pml_alpha_parameters         = [[0.90,0.90,1],[0.65,0.65,1],[0.65,0.65,1]]
)


######################### Define a moving window

# window starts  moving at the start of the simulation

MovingWindow(
    time_start                     = 0.,     
    velocity_x                     = c_normalized,
)

######################### Define the plasma

##### plasma parameters
# atomic density
plasma_plateau_density_1_ov_cm3    = 1.3e18
n_at                               = plasma_plateau_density_1_ov_cm3*1e6/ncrit  # plasma plateau density in units of critical density defined above
R_plasma                           = 65.*um                                     # Radius of plasma

# Define the density function
# this plasma density profile tries to create the density distribution
# inside a gas cell with two chambers. 
# In the first one, H2-N2 gas mixture is injected. In this chamber ionization injection occurs
# In the second one, pure H2 is injected
p_xmin                             = Lx*c_over_omega0         # Position of the beginning of the plasma (meters)
p_xmax                             = Lx*c_over_omega0+7.0e-3  # Position of the end of the plasma (meters)
xc1                                = Lx*c_over_omega0+0.4e-3  # position of the max of density in the first chamber (m)
xc2                                = Lx*c_over_omega0+0.8e-3  # position of the max of density in the second chamber (m)
mu1                                = 0.2e-3                   # 'Fermi energy' in the first chamber (m)
mu2                                = 1.0e-3                   # 'Fermi energy' in the second chamber (m)
T1                                 = 0.03e-3                  # 'Temperature' at the cell entrance (m)
T2                                 = 0.04e-3                  # 'Temperature' at the interface between the two chambers, assuming constant pressure  (m)
T3                                 = 0.03e-3                  # 'Temperature' at the cell entrance (m)
level_start_N                      = 5                        # initial ionisation state of N atoms
Q_init_N                           = float(level_start_N)     # initial charge of N atoms
dopant_N_concentration             = 0.10
Prop_N_in_1                        = dopant_N_concentration   # proportion of N atoms in H2-N2 mixture
Prop_H_in_1                        = 1.-Prop_N_in_1           # proportion of H atoms in H2-N2 mixture


def dens_func_at1(x, r):
    x_meters = (x)*c_over_omega0
    var1 = (1.+np.exp(-mu1/T1)) / (1.+np.exp(-(mu1+x_meters-xc1)/T1))
    var2 = (1.+np.exp(-mu1/T2)) / (1.+np.exp(-(mu1-x_meters+xc1)/T2))
    nat1 = np.where(x_meters < xc1, var1, var2)
    nat1 = np.where(x_meters <= p_xmin, 0.0, nat1)
    nat1 = np.where(x_meters >= p_xmax, 0.0, nat1)

    return nat1

def dens_func_at2(x, r):
    x_meters = (x)*c_over_omega0
    var1     = (np.exp(-(mu1-x_meters+xc1)/T2)- np.exp(-mu1/T2)) / (1.+np.exp(-(mu1-x_meters+xc1)/T2))
    var1     = np.where(var1 > 0.0, var1, 0.0)
    var2     = (1.+np.exp(-mu2/T3)) / (1.+np.exp(-(mu2-x_meters+xc2)/T3))
    nat2     = np.where(x_meters < xc2, var1, var2)
    nat2     = np.where(x_meters <= p_xmin, 0.0, nat2)
    nat2     = np.where(x_meters >= p_xmax, 0.0, nat2)
    return nat2

def dens_func_e(x, r):
    n1       = dens_func_at1(x, r)
    n2       = dens_func_at2(x, r)
    return (Prop_H_in_1 + Prop_N_in_1*Q_init_N)*n1 + n2

# number density profile of the dopant (nitrogen)
def my_density_profile_dopant(x,r):
    radial_profile     = 1.
    if (r>R_plasma) or (x<p_xmin/c_over_omega0):
        radial_profile = 0.
    return radial_profile*dens_func_at1(x,r)*Prop_N_in_1*n_at

# number density profile of the electrons (hydrogen + first 5 levels of nitrogen)
def density_profile_electrons(x,r):
    radial_profile     = 1.
    if (r>R_plasma) or (x<p_xmin/c_over_omega0):
        radial_profile = 0.
    return radial_profile*dens_func_e(x,r)*n_at

###### define the plasma electrons

pusher = "ponderomotive_boris"
if (use_BTIS3_interpolation == True):
        pusher = "ponderomotive_borisBTIS3"

Species(
  name                      = "bckgelectron",
  position_initialization   = "regular",
  momentum_initialization   = "cold",
  particles_per_cell        = 4,
  regular_number            = [4,1,1],
  c_part_max                = 1.0,
  mass                      = 1.0,
  charge                    = -1.0,
  number_density            = density_profile_electrons,
  mean_velocity             = [0.0, 0.0, 0.0],
  temperature               = [0.,0.,0.],
  pusher                    = pusher,
  time_frozen               = 0.0,
  boundary_conditions       = [["remove", "remove"],["remove", "remove"],],
)

# Nitrogen N5+ ions (i.e. already ionized up to the first two ionization levels over seven)
Species(
    name                    = "nitrogen5plus",
    position_initialization = "bckgelectron", # superposing this species macro-particles to "bckgelectron" macro-particles
    momentum_initialization = "cold",
    particles_per_cell      = 4,  
    atomic_number           = 7, # Nitrogen
    ionization_model        = "tunnel_envelope_averaged",
    ionization_electrons    = "electronfromion",
    maximum_charge_state    = 7,
    c_part_max              = 1.0,
    mass                    = 7.*mp_over_me + 7.*mn_over_me + 2.*me_over_me,
    charge                  = 5.0,
    number_density          = my_density_profile_dopant,
    mean_velocity           = [0., 0., 0.],
    time_frozen             = 2*T_sim,
    pusher                  = pusher,
    boundary_conditions     = [ ["remove", "remove"], ["reflective", "remove"],],
)

#### define the electron bunch
Species( 
  name                      = "electronfromion",
  position_initialization   = "regular",
  momentum_initialization   = "cold",
  particles_per_cell        = 0,
  c_part_max                = 1.0,
  mass                      = 1.0,
  charge                    = -1.0,
  number_density            = 0.,  
  pusher                    = pusher, 
  boundary_conditions       = [["remove", "remove"],["remove", "remove"], ],
)


######################### Diagnostics

list_fields_probes          = ['Ex','Ey','Bz']
list_fields_probes.extend(    ['Rho','Rho_bckgelectron','Rho_nitrogen5plus','Rho_electronfromion'])
list_fields_probes.extend(    ['Env_A_abs','Env_Chi','Env_E_abs'])

if (use_BTIS3_interpolation == True):
	list_fields_probes.append('BzBTIS3')

##### 1D Probe diagnostic on the x axis
DiagProbe(
        every               = int(50*um/dt), #500,
        origin              = [0. , 2.*dr, 2.*dr],
        corners             = [[Lx, 2.*dr, 2.*dr]],
        number              = [nx],
        fields              = list_fields_probes,
)

##### 2D Probe diagnostics on the xy plane
DiagProbe(
    every                   = int(100*um/dt),
    origin                  = [0., -nr*dr,0.],
    corners                 = [ [Lx,-Lr,0.], [0,Lr,0.] ],
    number                  = [nx, int(2*nr)],
    fields                  = list_fields_probes,
)

##### Diagnostic for the electron bunch macro-particles

def my_filter(particles):
    return ((particles.px>5.*MeV/c_normalized))
    
    
DiagTrackParticles(
  species                   = "electronfromion",
  every                     = int(50*um/dt),
  filter                    = my_filter,
  attributes                = ["x", "y", "z", "px", "py", "pz", "w"]
)


######################### Load balancing (for parallelization)                                                                                                                                                     
LoadBalancing(
    initial_balance         = False,
    every                   = 40,
    cell_load               = 1.,
    frozen_particle_load    = 0.1
)

##### Field diagnostics, used for 3D export
DiagFields(
   every                    = int(100*um/dt),
   fields                   = ["Env_E_abs"],
)

DiagFields(
   every                    = int(100*um/dt),
   fields                   = ["Rho_bckgelectron","Rho_electronfromion"],
)
