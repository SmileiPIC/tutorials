
dx = 0.125
dr = 1.5
dt = 0.96*dx
nx = 128*20
nr = 384
Lx = nx * dx
Lr = nr * dr
npatch_x = 256
laser_fwhm = 40.
laser_waist = 100.
Niterations = 8000

Main(
    geometry = "AMcylindrical",
    number_of_AM = 2,
    timestep = dt,
    simulation_time = Niterations*dt, 
    cell_length  = [dx, dr],
    grid_length = [ Lx, Lr ],
    number_of_patches = [npatch_x, 32],
    clrw = nx/npatch_x,
    EM_boundary_conditions = [
        ["silver-muller","silver-muller"],
        ["buneman","buneman"],
    ],
    solve_poisson = False,
    print_every = 100,
    random_seed = smilei_mpi_rank
)

Species( 
    name = "electron",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell = 36,
    c_part_max = 1.0,
    mass = 1.0,
    charge = -1.0,
    charge_density = trapezoidal(0.004, xvacuum=0., xplateau=1000000000, xslope1=1000.),
    mean_velocity = [0.0, 0.0, 0.0],
    pusher = "boris",    
    time_frozen = 0.0,
    boundary_conditions = [
        ["remove", "remove"],
        ["reflective", "remove"],
    ],
)

LaserGaussian2D(
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
    every = 500,
)

# These diagnostics are not available in AM yet
# DiagProbe(
#     every = 1000,
#     origin = [0., Main.grid_length[1]/2.],
#     corners = [
#         [Main.grid_length[0], Main.grid_length[1]/2.],
#     ],
#     number = [nx],
#     fields = ['Ex','Ey','Rho','Jx']
# )
# 
# DiagProbe(
#     every = 1000,
#     origin = [0., 0.],
#     vectors = [[Lx,0], [0,Ly]],
#     number = [nx,ny],
#     fields = ['Ex','Ey','Rho','Jx']
# )
# 
# DiagParticleBinning(
#     deposited_quantity = "weight",
#     every = 1000,
#     species = ["electron"],
#     axes = [
#         ["moving_x", 0, Lx, 300],
#         ["ekin", 1, 400, 100]
#     ]
# )

DiagPerformances(
    every = 1000,
    patch_information = False,
)
