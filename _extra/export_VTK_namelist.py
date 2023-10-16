import numpy as np
import cmath


geometry   = "3Dcartesian" # or "AMcylindrical"

# Spatial and temporal resolution
dx         = 0.1
dtrans     = 3.
dt         = 0.085
# Mesh
nx         = 512
ntrans     = 80
Lx         = nx * dx
Ltrans     = ntrans*dtrans
npatch_x   = 64

if (geometry  == "3Dcartesian"):
	cell_length             = [dx      , dtrans, dtrans]
	grid_length             = [Lx      , Ltrans, Ltrans]
	number_of_patches       = [npatch_x, 4     , 4     ]
	EM_boundary_conditions =  [["silver-muller"]]
    
elif (geometry  == "AMcylindrical"):
	cell_length             = [dx      , dtrans ]
	# remember that in AM cylindrical geometry the grid represents the half plane (x,r)
	# thus Ltrans is the transverse window size, i.e. from r=0 to r=Ltrans
	grid_length             = [Lx      , Ltrans ]
	number_of_patches       = [npatch_x, 4      ]
	EM_boundary_conditions  =  [["silver-muller","silver-muller"],["buneman","buneman"],]

Main(
     geometry               = geometry,
     interpolation_order    = 2,
     number_of_AM           = 2, # this variable is used only in AMcylindrical geometry
     timestep               = dt,
     simulation_time        = Lx,
     cell_length            = cell_length,
     grid_length            = grid_length,
     number_of_patches      = number_of_patches,
     EM_boundary_conditions = EM_boundary_conditions,
     solve_poisson          = False,
     print_every            = 100,
     random_seed            = smilei_mpi_rank
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


if (geometry  == "3Dcartesian"):

	boundary_conditions = [["remove", "remove"],["remove", "remove"],["remove", "remove"],]
	particles_per_cell  = 0.1
    
	# We build a Laguerre-Gauss laser from scratch instead of using LaserGaussian3D
	# The goal is to test the space_time_profile attribute
	omega               = 1.
	a0                  = 6.
	focus               = [0., Main.grid_length[1]/2., Main.grid_length[2]/2.]
	waist               = 10.
	laser_fwhm          = 20.
	time_envelope       = tgaussian(center=2**0.5*laser_fwhm, fwhm=laser_fwhm)

	Zr                  = omega * waist**2/2.
	w                   = math.sqrt(1./(1.+(focus[0]/Zr)**2))
	invWaist2           = (w/waist)**2
	coeff               = -omega * focus[0] * w**2 / (2.*Zr**2)

	m                   = 1 # azimuthal index
	def phase(y,z):
		return -m*np.arctan2((z-Ltrans/2.), (y-Ltrans/2.))

	def By(y,z,t):
		return 0.
	def Bz(y,z,t):
		r2 = (y-focus[1])**2 + (z-focus[2])**2
		omegat = omega*t - coeff*r2
		return a0 * w * math.exp( -invWaist2*r2  ) * time_envelope( omegat/omega ) * math.sin( omegat - phase(y,z))
	
	# Define the laser pulse	
	Laser( box_side = "xmin",space_time_profile = [By, Bz])

	# Define Plasma density profile
	def my_profile(x,y,z):
		center_plasma = [Lx/4.,Ltrans/2.,Ltrans/2.]
		Radius = 20. 
		Length = 5.
		if ((abs(x-center_plasma[0])<Length) and ((y-center_plasma[1])**2+(z-center_plasma[2])**2<Radius*Radius)):
			return 1.
		else:
			return 0.
 
if (geometry  == "AMcylindrical"):

	boundary_conditions = [["remove", "remove"],["remove", "remove"],]
	particles_per_cell  = 1
    
	# We build a simple Gaussian laser from scratch instead of using LaserGaussianAM
	
	# The goal is to test the space_time_profile_AM attribute
	omega         = 1.
	a0            = 6.
	focus         = [0., 0.]
	waist         = 10.
	laser_fwhm    = 20.
	time_envelope = tgaussian(center=2**0.5*laser_fwhm, fwhm=laser_fwhm)

	Zr            = omega * waist**2/2.
	w             = math.sqrt(1./(1.+(focus[0]/Zr)**2))
	invWaist2     = (w/waist)**2
	coeff         = -omega * focus[0] * w**2 / (2.*Zr**2)

	def Br_mode0(r,t):
		return 0.*(1.+0.*1j)	
	def Bt_mode0(r,t):
		return 0.*(1.+0.*1j)	
	def Br_mode1(r,t):
		return 0.*(1.+0.*1j)	
	def Bt_mode1(r,t):
		omegat = omega*t - coeff*r**2
		return a0 * w * math.exp( -invWaist2*r**2  ) * time_envelope( omegat/omega ) * math.sin( omegat )*(1.+0.*1j)	
	
	# Define the laser pulse	
	Laser( box_side = "xmin",space_time_profile_AM = [Br_mode0, Bt_mode1, Br_mode0, Bt_mode1])

	# Define Plasma density profile
	def my_profile(x,r):
		center_plasma = Lx/4.
		Radius = 20. 
		Length = 5.
		if ((abs(x-center_plasma)<Length) and (r<Radius)):
			return 1.
		else:
			return 0.

# Add some test electrons
Species( 
    name                    = "electron",
    position_initialization = "random",
    momentum_initialization = "cold",
    particles_per_cell      = particles_per_cell,
    c_part_max              = 1.0,
    mass                    = 1,
    charge                  = -1,
    charge_density          = my_profile,  
    mean_velocity           = [0., 0., 0.],
    time_frozen             = 0.0,
    pusher                  = "boris",
    is_test                 = True,
    boundary_conditions     = boundary_conditions,
    )

# Prepare lists of fields for Probes and Field Diagnostics and the extrema for the Probe diagnostics
# Note how the Probes in AMcylindrical geometry use another origin for the axes (see documentation)

list_fields_probes_diagnostic = ['Ex','Ey','Ez']

if (geometry  == "3Dcartesian"):

	list_fields_field_diagnostic  = list_fields_probes_diagnostic
	
	origin_1D_probes              =  [0.                 , Main.grid_length[1]/2.  , Main.grid_length[2]/2.]
	corners_1D_probes             = [[Main.grid_length[0], Main.grid_length[1]/2.  , Main.grid_length[2]/2.]]
	
	origin_2D_probes              =  [0.                 , Main.grid_length[1]/4.  , Main.grid_length[2]/2.]
	corners_2D_probes             = [[Main.grid_length[0], Main.grid_length[1]/4.  , Main.grid_length[2]/2.],[0., 3*Main.grid_length[1]/4., Main.grid_length[2]/2.],]
	
elif (geometry  == "AMcylindrical"):
	list_fields_field_diagnostic  = ["El","Er","Et"]
	
	origin_1D_probes              =  [0.                 , 0.                      , 0.]
	corners_1D_probes             = [[Main.grid_length[0], 0.                      , 0.]]
	
	origin_2D_probes              =  [0.                 , -Main.grid_length[1]/4. , 0.]
	corners_2D_probes             = [[Main.grid_length[0], -Main.grid_length[1]/4. , 0.                    ],[0.,  Main.grid_length[1]/4. , 0.],]
	

DiagFields(
    every      = 20,
    fields     = list_fields_field_diagnostic
)

DiagProbe(
	every      = 50,
	origin     = origin_1D_probes,
	corners    = corners_1D_probes,
	number     = [nx],
	fields     = list_fields_probes_diagnostic,
)

DiagProbe(
	every      = 50,
	origin     = origin_2D_probes,
	corners    = corners_2D_probes,
	number     = [nx, ntrans],
	fields     = list_fields_probes_diagnostic,
)

DiagTrackParticles(
    species    = "electron",
    every      = 20,
    attributes = ["x","y", "z", "px", "py", "pz","weight"]
)
