###### Laser Wake tutorial in Azimuthal Modes cylindrical geometry
 
dx = 0.125    # longitudinal resolution
dr = 1.5      # radial resolution

nx = 128*20   # number of grid points in the longitudinal direction
nr = 384      # number of grid points in the radial direction

Lx = nx * dx  # longitudinal size of the simulation window
Lr = nr * dr  # radial size of the simulation window

npatch_x = 256

dt = 0.96*dx  # integration timeestep
Niterations = 10000

Main(
    geometry = "AMcylindrical",
    number_of_AM = 2,
    timestep = dt,
    simulation_time = Niterations*dt, 
    cell_length  = [dx, dr],
    grid_length = [ Lx, Lr ],
    number_of_patches = [npatch_x, 32],
    EM_boundary_conditions = [
        ["silver-muller","silver-muller"],
        ["buneman","buneman"],
    ],
    solve_poisson = False,
    print_every = 100,
    random_seed = smilei_mpi_rank
)

# The window is much larger than the laser wais, 
# to allow the laser diffract 
# (no radial absorbing boundary conditions available)
# The physics of interest in this case is near the axis, 
# so no need to fill all the window with plasma

Radius_plasma = 200.
longitudinal_profile = trapezoidal(0.004, xvacuum=0., xplateau=1000000000, xslope1=1000.)
def nplasma(x,r):
    profile_r = 0.
    if (r<Radius_plasma):
        profile_r = 1.
    return profile_r*longitudinal_profile(x,r)


Species( 
    name = "electron",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell = 36,
    c_part_max = 1.0,
    mass = 1.0,
    charge = -1.0,
    charge_density = nplasma,
    mean_velocity = [0.0, 0.0, 0.0],
    pusher = "boris",    
    time_frozen = 0.0,
    boundary_conditions = [
        ["remove", "remove"],
        ["reflective", "remove"],
    ],
)

# Linear polarization on the y axis
laser_fwhm = 40.
laser_waist = 100.

LaserGaussianAM(
    box_side         = "xmin",
    a0              = 4.,
    focus           = [0., 0.],
    waist           = laser_waist,
    time_envelope   = tgaussian(center=3*laser_fwhm, fwhm=laser_fwhm)
)

MovingWindow(
    time_start = 380.,
    velocity_x = 1. 
)


# Grid diagnostic
DiagFields(
    every = 200,
)

# 1D Probe defined on a line parallel to the axis of propagation,
# at a distance sqrt(8)*dr from the axis.
# A Probe placed on the axis would be very noisy
DiagProbe(
    every = 200,
    origin = [0., 2*dr, 2*dr],
     corners = [
         [nx*dx, 0, 0],
     ],
     number = [nx],
     fields = ['Ex','Ey','Rho','Jx']
 )
 
# 2D Probe, defined on the plane parallel to the polarization axis of the laser
DiagProbe(
    every = 200,
    origin   = [0., -nr*dr,0.],
    corners  = [ [nx*dx,-nr*dr,0.], [0,nr*dr,0.] ],
    number   = [nx, 2*nr],
    fields = ['Ex','Ey','Rho','Jx']
)
