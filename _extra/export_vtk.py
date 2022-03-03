import happi;S=happi.Open()

# Export E**2 field, all available timesteps
E2 = S.Field.Field0("Ex**2+Ey**2+Ez**2")
E2.toVTK()

# Export particles, all available timesteps
chunk_size = 600000
species_name = "electron"
timesteps_track = S.TrackParticles(species = species_name).getAvailableTimesteps()

for timestep_track in timesteps_track:
    track_part             = S.TrackParticles(species = species_name, 
            chunksize=chunk_size,axes = ["x","y","z","px","py","pz","Id"],
            timesteps=timestep_track)
    track_part.toVTK()
    del track_part
