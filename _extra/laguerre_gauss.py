import numpy as np

# Spatial and temporal resolution
dx         = 0.1
dtrans     = 3.
dt         = 0.09
# Mesh
nx         = 512
ntrans     = 80
Lx         = nx * dx
Ltrans     = ntrans*dtrans
npatch_x   = 64


Main(
    geometry = "3Dcartesian",
    
    interpolation_order = 2,

    timestep = dt,
    simulation_time = Lx,

    cell_length  = [dx, dtrans, dtrans],
    grid_length = [ Lx,  Ltrans, Ltrans],

    number_of_patches = [npatch_x, 4, 4],

    EM_boundary_conditions = [ ["silver-muller"] ],
    
    solve_poisson = False,
    print_every = 100,

    random_seed = smilei_mpi_rank
)

MovingWindow(
    time_start = Main.grid_length[0],
    velocity_x = 0.9997
)

LoadBalancing(
    initial_balance = False,
    every = 20,
    cell_load = 1.,
    frozen_particle_load = 0.1
)


# We build a Laguerre-Gauss laser from scratch instead of using LaserGaussian3D
# The goal is to test the space_time_profile attribute
omega = 1.
a0 = 6.
focus = [0., Main.grid_length[1]/2., Main.grid_length[2]/2.]
waist = 10.
laser_fwhm = 20.
time_envelope = tgaussian(center=2**0.5*laser_fwhm, fwhm=laser_fwhm)

Zr = omega * waist**2/2.
w  = math.sqrt(1./(1.+(focus[0]/Zr)**2))
invWaist2 = (w/waist)**2
coeff = -omega * focus[0] * w**2 / (2.*Zr**2)

m=1 # azimuthal index
def phase(y,z):
	return -m*np.arctan2((z-Ltrans/2.), (y-Ltrans/2.))
	

def By(y,z,t):
	return 0.
def Bz(y,z,t):
	r2 = (y-focus[1])**2 + (z-focus[2])**2
	omegat = omega*t - coeff*r2
	return a0 * w * math.exp( -invWaist2*r2  ) * time_envelope( omegat/omega ) * math.sin( omegat - phase(y,z))
Laser(
    box_side = "xmin",
    space_time_profile = [By, Bz]
)


# Plasma density profile
def my_profile(x,y,z):
	center = [Lx/4.,Ltrans/2.,Ltrans/2.]
	Radius = 20. 
	Length = 5.
	if ((abs(x-center[0])<Length) and ((y-center[1])**2+(z-center[2])**2<Radius*Radius)):
		return 1
	else:
		return 0

# Add some test electrons
Species( 
    name = "electron",
    position_initialization = "random",
    momentum_initialization = "cold",
    particles_per_cell = 0.1,
    c_part_max = 1.0,
    mass = 1,
    charge = -1,
    charge_density = my_profile,  
    mean_velocity = [0., 0., 0.],
    time_frozen = 0.0,
    pusher = "boris",
    is_test = True,
    boundary_conditions = [
       ["remove", "remove"],
       ["remove", "remove"],
       ["remove", "remove"],
    ],

)

# Diagnostics 

list_fields = ['Ex','Ey','Ez','Rho','Jx']

DiagFields(
    every = 20,
    fields = list_fields
)

DiagProbe(
	every = 50,
	origin = [0., Main.grid_length[1]/2., Main.grid_length[2]/2.],
	corners = [
	    [Main.grid_length[0], Main.grid_length[1]/2., Main.grid_length[2]/2.]
	],
	number = [nx],
	fields = list_fields,
)

DiagProbe(
	every = 50,
	origin = [0., Main.grid_length[1]/4., Main.grid_length[2]/2.],
	corners = [
	    [Main.grid_length[0], Main.grid_length[1]/4., Main.grid_length[2]/2.],
	    [0., 3*Main.grid_length[1]/4., Main.grid_length[2]/2.],
	],
	number = [nx, ntrans],
	fields = list_fields,
)

DiagScalar(every = 10, vars=['Uelm','Ukin_electron','ExMax','ExMaxCell','EyMax','EyMaxCell', 'RhoMin', 'RhoMinCell'])

DiagTrackParticles(
    species = "electron",
    every = 20,
    attributes = ["x","y", "z", "px", "py", "pz","weight"]
)
