################### 2D Laser Wakefield with envelope
dx = 1. 
dtrans = 1.5
dt = 0.8*dx
nx = 384
ntrans = 256 
Lx = nx * dx
Ltrans = ntrans*dtrans
npatch_x = 64
laser_fwhm = 70. 
center_laser = Lx-2.*laser_fwhm 
time_start_moving_window =  0.


Main(
    geometry = "2Dcartesian",

    interpolation_order = 2,

    timestep = dt,
    simulation_time = 4600.*dt,

    cell_length  = [dx, dtrans],
    grid_length = [ Lx,  Ltrans],

    number_of_patches =[npatch_x, 16],
    
    clrw = nx/npatch_x,

    EM_boundary_conditions = [ ["silver-muller"] ],
    

    solve_poisson = False,
    print_every = 100,

    random_seed = smilei_mpi_rank
)

MovingWindow(
    time_start = time_start_moving_window,
    velocity_x = 1. 
)

LoadBalancing(
    initial_balance = False,
        every = 20,
    cell_load = 1.,
    frozen_particle_load = 0.1
)

n0 = 0.002 # plasma plateau density 

Radius_plasma = 130.
longitudinal_profile = polygonal(xpoints=[center_laser+1.5*laser_fwhm,center_laser+2.*laser_fwhm,15000,20000],xvalues=[0.,n0,n0,0.])
def my_density_profile(x,y):
    r = abs(Ltrans/2.-y)
    profile_r = 0.
    if (r<Radius_plasma):
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
    charge_density = my_density_profile,
    mean_velocity = [0.0, 0.0, 0.0],
    temperature = [0.0],
    pusher = "ponderomotive_boris", # pusher to interact with envelope
    time_frozen = 0.0,
    boundary_conditions = [
       ["remove", "remove"],
       ["remove", "remove"],
    ],
)

LaserEnvelopeGaussian2D( 
    a0              = 2.7,     
    focus           = [1.1*center_laser, Main.grid_length[1]/2.],
    waist           = 70.,
    time_envelope   = tgaussian(center=center_laser, fwhm=laser_fwhm),
    envelope_solver = 'explicit',
    Envelope_boundary_conditions = [ ["reflective", "reflective"],
        ["reflective", "reflective"], ],
)


Checkpoints(
    dump_step = 0,
    dump_minutes = 0.0,
    exit_after_dump = False,
)

list_fields = ['Ex','Ey','Rho','Env_A_abs','Env_E_abs']

DiagFields(
   every = 400,
        fields = list_fields
)

DiagProbe(
        every = 400,
        origin = [0., Main.grid_length[1]/2.],
        corners = [
            [Main.grid_length[0], Main.grid_length[1]/2.]
        ],
        number = [nx],
        fields = ['Ex','Ey','Rho','Env_A_abs','Env_E_abs']
)


DiagScalar(every = 20, vars=['Env_A_absMax','Env_E_absMax'])


