# -------------------
# MY PYTHON VARIABLES
# -------------------

dx     = 1./64   # spatial resolution
ncells = 256     # number of cells
nppc = 25        # number of particle-per-cell

Te = 1e-6  # temperature in units of me c^2

# Initial plasma density profile
radius = 30.*dx
x0 = 40.*dx
y0 = 200.*dx
def ne(x,y):
    if (x-x0)**2 + (y-y0)**2 < radius**2:
        return 1.
    else:
        return 0.

# --------------------------------------
# SMILEI's VARIABLES (DEFINED IN BLOCKS)
# --------------------------------------

Main(
    geometry = "2Dcartesian",
    
    interpolation_order = 2,
    
    timestep_over_CFL = 0.95,
    simulation_time = 10.,
    
    cell_length = [dx, dx],
    number_of_cells  = [ncells, ncells],
    
    number_of_patches = [ 32, 32 ],
    
    EM_boundary_conditions = [ ['periodic'] ] ,

    solve_poisson = False,
    
    random_seed = smilei_mpi_rank
)

Species(
    name = 'eon',
    position_initialization = 'regular',
    momentum_initialization = 'maxwell-juettner',
    particles_per_cell = nppc,
    mass = 1.0,
    charge = -1.0,
    number_density = ne,
    temperature = [Te],
    mean_velocity = [0.3, 0., 0.],
    boundary_conditions = [
    	['periodic'],
    ]
)
Species(
    name = 'pon',
    position_initialization = 'regular',
    momentum_initialization = 'maxwell-juettner',
    particles_per_cell = nppc,
    mass = 1.0,
    charge = 1.0,
    number_density = ne,
    temperature = [Te],
    mean_velocity = [0.3, 0., 0.],
    boundary_conditions = [
    	['periodic'],
    ]
)

### DIAGNOSTICS

DiagParticleBinning(
    deposited_quantity = "weight",
    every = 10,
    species = ["eon"],
    axes = [
        ["x", 0., Main.grid_length[0], 200],
        ["y", 0., Main.grid_length[1], 200],
    ]
)

DiagPerformances(
    every = 10
)

