Thermal plasma
---------------------------

The goal of this tutorial is to get familiar with:

* the ``Species`` block that allows you to define a particle species,
* the ``ParticleBinning`` diagnostics to obtain particle energy spectra,
* the ``happi.multiPlot`` tool,
* the problem of `numerical heating` and the necessity to correctly `resolve the electron dynamics` in explicit PIC codes.


----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^

Download the input file `thermal_plasma_1d.py <thermal_plasma_1d.py>`_.

An `infinite` electron-ion plasma is let free to evolve in a 1D cartesian
geometry with periodic boundary conditions.



----

Check input file and run the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step is to check that your `input file` is correct.
To do so, you will run (locally) :program:`Smilei` in test mode:

.. code-block:: bash

    ./smilei_test thermal_plasma_1d.py

If your simulation `input file` is correct, you can now run the simulation.
Before going to the analysis of your simulation, check your *log* and/or
*error* output.

Check what output files have been generated: what are they?

----

Preparing the post-processing tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's now turn to analysing the output of your run with :program:`happi`.
To do so, open an ``ipython`` session:

.. code-block:: bash

    ipython

In *ipython*, import the :program:`happi` package:

.. code-block:: python

    import happi

then open your simulation:

.. code-block:: python

    S = happi.Open('/path/to/the/simulation')

.. warning::

    Use the correct simulation path.

You are now ready to take a look at your simulation's results.

----

The ``Field`` diagnostics using ``happi.multiPlot``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To have a quick access at your data and `check` what is going on, you will plot
the electron and ion densities together with the electrostatic field :math:`E_x`.

First, `prepare` the data:

.. code-block:: python

    # minus the electron density
    ne = S.Field(0,'-Rho_eon',vmin=-0.25,vmax=2, label="e- density")
    
    # ion density
    ni = S.Field(0,'Rho_ion', label="ion density")
    
    # Ex field
    ex = S.Field(0,'Ex', label="Ex field")

You may plot all these quantities independently using ``ex.plot()`` or ``ex.animate()``,
but you can also use the ``multiPlot`` function of :program:`happi`:

.. code-block:: python

    happi.multiPlot(ne,ni,ex)


----

The ``ParticleBinning`` diagnostics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, have a look at the ``ParticleBinning`` diagnostics, and in particular
at the electron energy distribution at initial and latest timesteps:

.. code-block:: python

    Nt        = int(S.namelist.tsim / S.namelist.dt)
    f_initial = S.ParticleBinning(0, data_log=True, timesteps=0 , label="initial")
    f_final   = S.ParticleBinning(0, data_log=True, timesteps=Nt, label="final")
    happi.multiPlot(f_initial, f_final)


----

Effect of spatial resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Have a look at the total energy and energy balance in your simulation
(remember the ``Utot`` and ``Ubal`` scalars).
Note the level of energy imbalance at the end of this simulation for which
the spatial resolution is equal to the Debye Length (:math:`\Delta x = \lambda_{\rm De}`).

Increase your spatial resolution to :math:`\Delta x = 16 \times \lambda_{\rm De}`.
Run the simulation again, and check the energy imbalance at the end of the simulation.
What do you observe?
Can you check the electron spectrum at the beginning and end of the simulation?
What is going on?

Finally, increase your spatial resolution to
:math:`\Delta x = 2\,c/\omega_{pe} = 2\,c\lambda_{\rm De}/v_{\rm th}`.
Check the evolution of the total energy.
What do you observe?
