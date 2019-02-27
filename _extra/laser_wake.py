
dx = 0.125
dy = 2.
dt = 0.124
nx = 128*20
ny = 320
Lx = nx * dx
Ly = ny * dy
npatch_x = 256
laser_fwhm = 40.
laser_waist = 200.
Niterations = 3000

Main(
    geometry = "2Dcartesian",
    interpolation_order = 2,
    timestep = dt,
    simulation_time = Niterations*dt, 
    cell_length  = [dx, dy],
    grid_length = [ Lx, Ly ],
    number_of_patches = [npatch_x, 32],
    clrw = nx/npatch_x,
    EM_boundary_conditions = [
        ["silver-muller","silver-muller"],
        ["silver-muller","silver-muller"],
    ],
    solve_poisson = False,
    print_every = 100,
    random_seed = smilei_mpi_rank
)

Species( 
    name = "electron",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell = 9,
    c_part_max = 1.0,
    mass = 1.0,
    charge = -1.0,
    charge_density = trapezoidal(0.003, xvacuum=0., xplateau=1000000000, xslope1=1000.),
    mean_velocity = [0.0, 0.0, 0.0],
    pusher = "boris",    
    time_frozen = 0.0,
    boundary_conditions = [
        ["remove", "remove"],
        ["remove", "remove"],
    ],
)

LaserGaussian2D(
    box_side         = "xmin",
    a0              = 4.,
    focus           = [0., Main.grid_length[1]/2.],
    waist           = laser_waist,
    time_envelope   = tgaussian(center=3*laser_fwhm, fwhm=laser_fwhm)
)


DiagProbe(
    every = 1000,
    origin = [0., Main.grid_length[1]/2.],
    corners = [
        [Main.grid_length[0], Main.grid_length[1]/2.],
    ],
    number = [nx],
    fields = ['Ex','Ey','Rho','Jx']
)

DiagProbe(
    every = 1000,
    origin = [0., 0.],
    vectors = [[Lx,0], [0,Ly]],
    number = [nx,ny],
    fields = ['Ex','Ey','Rho','Jx']
)

DiagParticleBinning(
    deposited_quantity = "weight",
    every = 1000,
    species = ["electron"],
    axes = [
        ["moving_x", 0, Lx, 300],
        ["ekin", 1, 400, 100]
    ]
)

DiagPerformances(
    every = 1000,
    patch_information = False,
)
