###### Namelist for plasma wake excited by a relativistic electron bunch

import math

dx = 0.2 
dtrans = 0.5
dt = 0.18
nx = 1280
ntrans = 640
Lx = nx * dx
Ltrans = ntrans*dtrans
npatch_x = 128

# Plasma density
n0 = 0.0017

# Bunch position and rms dimensions (gaussian density distribution)
bunch_sigma_x = 15.
bunch_sigma_r = 15. 
center_bunch = 12*bunch_sigma_x

# Bunch normalized density
alpha = 0.6

# Bunch mean energy
gamma= 200.                     # relativistic lorentz factor
beta = math.sqrt(1.-1/gamma**2) # normalized speed of the beam



# normalized density of a bunch with gaussian density
def nbunch_(x,y):
        
	profile_x = math.exp(-(x-center_bunch)**2/2./bunch_sigma_x**2)
	profile_r = math.exp(-((y-Main.grid_length[1]/2.)**2)/2./bunch_sigma_r**2)
        profile = alpha*n0*profile_x*profile_r
	
	if ( (  (x-center_bunch)**2/(4.*bunch_sigma_x)**2 + ((y-Main.grid_length[1]/2.)**2)/(4.*bunch_sigma_r)**2 ) < 1. ):
		return profile
	else:
		return 0.

Main(
    geometry = "2Dcartesian",

    interpolation_order = 2,

    timestep = dt,
    simulation_time = dt*4000., #int(1*Lx/dt)*dt,

    cell_length  = [dx, dtrans],
    grid_length = [ Lx,  Ltrans],

    number_of_patches = [npatch_x, 64],
    
    clrw = nx/npatch_x,

    EM_boundary_conditions = [ ["silver-muller"] ],

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


Radius_plasma = 6.*bunch_sigma_r
longitudinal_profile = polygonal(xpoints=[center_bunch+60.,center_bunch+110.,200.*bunch_sigma_x,225.*bunch_sigma_x],xvalues=[0.,n0,n0,0.])
def nplasma(x,y):
    profile_r = 0.
    if ((y-Main.grid_length[1]/2.)**2<Radius_plasma**2):
        profile_r = 1.
    return profile_r*longitudinal_profile(x,y)

Species(
    name = "electron",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell = 4,
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


Species(
    name = "bunch_electrons",
    position_initialization = "regular",
    momentum_initialization = "cold",
    relativistic_field_initialization = True,
    particles_per_cell = 4,
    c_part_max = 1.0,
    mass = 1.0,
    charge = -1.0,
    charge_density = nbunch_,
    mean_velocity = [beta, 0.0, 0.0], 
    pusher = "boris",
    time_frozen = 0.0,
    boundary_conditions = [
       ["remove", "remove"],
       ["remove", "remove"],
    ],
)



list_fields = ['Ex','Ey','Rho','Jx','Jy']

DiagFields(
    every = 200,
        fields = list_fields
)

DiagProbe(
        every = 200,
        origin = [0., Main.grid_length[1]/2.],
        corners = [
            [Main.grid_length[0], Main.grid_length[1]/2.]
        ],
        number = [nx],
        fields = ['Ex','Ey','Rho','Jx']
)
