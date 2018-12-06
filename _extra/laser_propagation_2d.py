# ----------------------------------------------------------------------------------------
# 					SIMULATION PARAMETERS FOR THE PIC-CODE SMILEI
# ----------------------------------------------------------------------------------------

from math import pi, sqrt

l0 = 2. * pi             # laser wavelength [in code units]
t0 = l0                  # optical cycle
Lsim = [32.*l0, 32.*l0]  # length of the simulation
Tsim = 50.*t0            # duration of the simulation
resx = 16.               # nb of cells in one laser wavelength
rest = resx*sqt(2.)/0.95 # nb of timesteps in one optical cycle 

Main(
    geometry = "2Dcartesian",
    
    interpolation_order = 2 ,
    
    cell_length = [l0/resx,l0/resx],
    grid_length  = Lsim,
    
    number_of_patches = [ 8, 8 ],
    
    timestep = t0/rest,
    simulation_time = Tsim,
     
    EM_boundary_conditions = [
        ['silver-muller'],
        ['silver-muller'],
    ],
    
    random_seed = smilei_mpi_rank
)

LaserGaussian2D(
    a0              = 1., # normalized amplitude
    omega           = 1.,
    focus           = [Lsim[0]/2., Lsim[1]/2.], # coordinates of laser focus
    waist           = 5.*l0,
    incidence_angle = 0.,
    time_envelope   = tgaussian(fwhm=4*t0, center=0.15*Tsim)
)


DiagScalar(
    every = rest
)

DiagFields(
    every = rest,
    fields = ['Ex','Ey','Ez','Bx','By','Bz']
)

# 2-dimensional grid diagnostic
DiagProbe(
    every = 100,
    number = [100, 100], # number of points in the grid
    origin = [0., 10.*l0], # coordinates of origin point
    corners = [
        [20.*l0, 0.*l0], # coordinates of first corner of the grid
        [3.*l0 , 40.*l0], # coordinates of second corner of the grid
    ],
    fields = []
)

# probe diagnostic with 1 point
DiagProbe(
    every = 10,
    origin = [0.1*Lsim[0], 0.5*Lsim[1]],
    fields = []
)


