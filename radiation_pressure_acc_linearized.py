# ----------------------------------------------------------------------------------------
#                     SIMULATION PARAMETERS FOR THE PIC-CODE SMILEI
# ----------------------------------------------------------------------------------------

import math

l0 = 2.0*math.pi       # laser wavelength
t0 = l0                # optical cycle
Lsim = [6.*l0,10.*l0]  # length of the simulation
Tsim = 10.*t0          # duration of the simulation
resx = 100.            # nb of cells in on laser wavelength
rest = 150.            # time of timestep in one optical cycle 

current_ncells_Y = Lsim[1] / (l0/resx)
target_ncells_Y = 1024.
target_cell_length_Y = (l0/resx*current_ncells_Y)/target_ncells_Y

#target_cell_length_Y = l0/resx

Main(
    geometry = "2Dcartesian",
    
    interpolation_order = 2 ,
    
    cell_length = [l0/resx,target_cell_length_Y],
    grid_length  = Lsim,
    
    number_of_patches = [ 8, 16 ],
    patch_arrangement = "linearized_YX", 
    #patch_arrangement = "linearized_XY", 
    
    timestep = t0/rest,
    simulation_time = Tsim,
     
    EM_boundary_conditions = [
        ['silver-muller'],
        ['periodic'],
    ],
)

#LoadBalancing(
#    every = 20,
#    )
#

# We build a gaussian laser from scratch instead of using LaserGaussian2D
# The goal is to test the space_time_profile attribute
omega = 1.
a0 = 150.
waist = 2.0*l0
Zr = omega * waist**2/2.
focus = [10.*l0, 5.*l0]

amplitude = a0 / math.sqrt(2)
w  = math.sqrt(1./(1.+(focus[0]/Zr)**2))
invWaist2 = (w/waist)**2
coeff = -omega * focus[0] * w**2 / (2.*Zr**2)
def By(y,t):
    B = amplitude * w * math.exp( -invWaist2*(y-focus[1])**2 ) \
        * math.sin(omega*t - coeff*(y-focus[1])**2 + math.pi*0.5)
    if t < t0: return t/t0 * B
    else     : return B
def Bz(y,t):
    B = amplitude * w * math.exp( -invWaist2*(y-focus[1])**2 ) \
        * math.sin(omega*t - coeff*(y-focus[1])**2)
    if t < t0: return t/t0 * B
    else     : return B

Laser(
    box_side           = "xmin",
    space_time_profile = [By, Bz]
)

Species(
    name = 'ion',
    position_initialization = 'regular',
    momentum_initialization = 'cold',
    particles_per_cell = 16,
    mass = 1836.0,
    charge = 1.0,
    number_density = trapezoidal(100.0,xvacuum=l0,xplateau=0.44*l0),
    boundary_conditions = [
        ["reflective", "reflective"],
        ["periodic", "periodic"],
    ],
)

Species(
    name = 'eon',
    position_initialization = 'regular',
    momentum_initialization = 'mj',
    particles_per_cell = 16,
    mass = 1.0,
    charge = -1.0,
    number_density = trapezoidal(100.0,xvacuum=l0,xplateau=0.44*l0),
    temperature = [0.001],
    boundary_conditions = [
        ["reflective", "reflective"],
        ["periodic", "periodic"],
    ], 
    time_frozen = 0.1
)



globalEvery = int(rest/2.)

DiagScalar(every=globalEvery)

DiagProbe(
    every = globalEvery,
    number = [512, 1024],
    origin = [0.*l0, 0.*l0],
    corners = [
        [4.*l0,  0.*l0],
        [0.*l0, 8.*l0]
        ],
    fields = ['Ex','Ey','Ez','Bx','By','Bz','Rho_ion','Rho_eon']
    )


DiagPerformances(
    every = globalEvery,
)