Practical 3: Weibel and two-stream instabilities
================================================

The goal of this tutorial is to run to physics simulation relating to streaming instabilities,
and in particular to the electron Weibel and two-stream instabilities.

This tutorial will also allow you to:

* get familiar with the ``happi.streak`` tool
* extract instability growth rates
* construct and extract phase-space distribution using the ``ParticleBinning`` diagnostics

----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^

Download the two input files `weibel_1d.py <weibel_1d.py>`_ and
`two_stream_1d.py <two_stream_1d.py>`_.

In both simulations, a plasma with density :math:`n_0` is initialized (:math:`n_0 = 1`).
This makes code units equal to plasma units, i.e. times are normalized to the inverse of
the electron plasma frequency :math:`\omega_{p0} = \sqrt{e^2 n_0/(\epsilon_0 m_e)}`,
distances to the electron skin-depth :math:`c/\omega_{p0}`, etc...

Ions are frozen during the whole simulation and just provide a neutralizing background.
Two electron species are initialized with density :math:`n_0/2` and
a mean velocity :math:`\pm \bf{v_0}`.

----

Check input file and run the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step is to check that your `input files` are correct.
To do so, you will run (locally) :program:`Smilei` in test mode:

.. code-block:: bash

    ./smilei_test weibel_1d.py
    ./smilei_test two_stream_1d.py

If your simulation `input files` are correct, you can run the simulations.

Before going to the analysis, check your *logs*.


----

Weibel instability: analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In an :program:`ipython` terminal, open the simulation:

.. code-block:: python

    S = happi.Open('/path/to/your/simulation/weibel_1d')

The ``streak`` function of :program:`happi` can plot any 1D diagnostic as a function of time.
Here, we look total the current density :math:`J_z` and magnetic field :math:`B_y`
evolution in time:

.. code-block:: python

    S.Field(0,'Jz').streak()    
    S.Field(0,'By_m').streak()

Do you have any clue what is going on? 
Do not hesitate to use the ``animate`` function:

.. code-block:: python

    jz = S.Field(0,'Jz')
    by = S.Field(0,'By_m',vmin=-0.5,vmax=0.5)
    happi.multiPlot(jz,by)

Now, using the ``Scalar`` diagnostics, check the temporal evolution of the energies
in the magnetic (:math:`B_y`) and electrostatic (:math:`E_z`) fields.
Can you distinguish the linear and non-linear phase of the instability?

Have a closer look at the growth rates. Use the ``data_log=True`` options when loading
your scalar diagnostics, then use ``happi.multiPlot()`` to plot both energies as a
function of time. Can you extract the growth rates? What do they tell you?

If you have time, run the simulation for different wavenumbers :math:`k`.
Check the growth rate as a function of :math:`k`.

For those interested, you will find more in:
`Grassi et al., Phys. Rev. E 95, 023203 (2017) <https://journals.aps.org/pre/abstract/10.1103/PhysRevE.95.023203>`_.



----

Two-stream instability: analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In an :program:`ipython` terminal, open the simulation:

.. code-block:: ipython

    S = happi.Open('/path/to/your/simulation/two_stream_1d')

then, have a first look at your simulation results:

.. code-block:: ipython

    ne  = S.Field(0,'-Rho_eon1-Rho_eon2',xmin=0,xmax=1.3)
    ex  = S.Field(0,'Ex',xmin=0,xmax=1.3)
    phs = S.ParticleBinning(0)
    happi.multiPlot(ne,ex,phs)

Any clue what's going on? 

Let's have a look at the energy in the electrostatic field :math:`E_x`:

* can you distinguish the linear and non-linear phase of the instability?
* check the :math:`(x,p_x)`-phase-space distribution, can you get any clue on what leads the instability to saturate?

Try changing the simulation box size (which is also the wavelength of the considered perturbation), e.g. taking: 
:math:`L_x =` 0.69, 1.03 or 1.68 :math:`c/\omega_{p0}`. What do you observe?

Now, take :math:`L_x =` 0.6, 0.31 or 0.16 :math:`c/\omega_{p0}`. What are the differences? Can you explain them?



