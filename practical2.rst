Practical 2: Thermal plasma (infinite size using periodic)
----------------------------------------------------------

Goal of the tutorial
^^^^^^^^^^^^^^^^^^^^

The goal of this tutorial is to get familiar with:

* how to submit a job on a super-computer (here the :program:`Poincare` machine) using its queuing system,

* the ``Species`` block that allows you to define a particle species in :program:`Smilei`,

* the ``ParticleBinning`` diagnostics to build up (e.g.) particle energy spectra,

* the :program:`Happi` ``multiPlot`` tool,

* the problem of `numerical heating` and the necessity to correctly `resolve the electron dynamics` in explicit PIC codes.

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^

An `infinite` electron-ion plasma is let free to evolve in a 1D cartesian geometry with periodic boundary conditions.


Content of the tutorial
^^^^^^^^^^^^^^^^^^^^^^^
This tutorial consist in a single directory :program:`Practical2` containing:
 
* `thermal_plasma_1d.py`: the input file for the simulation,

* `launcher.sh`: the submission script to launch your job on :program:`Poincare`.

Setup the tutorial
^^^^^^^^^^^^^^^^^^

* If you're not yet there, connect on `Poincare` via `ssh` using the `-X` option:

.. code-block:: bash

    ssh -X poincare

* Copy the content of this tutorial in the `$SCRATCHDIR` of `Poincare`:

.. code-block:: bash

    cp -r Smilei/handson/Practical2 $SCRATCHDIR/.

* Copy the executable files in the new folder:

.. code-block:: bash

    cp -r Smilei/smilei $SCRATCHDIR/Practical2/.
    cp -r Smilei/smilei_test $SCRATCHDIR/Practical2/.

* Go the tutorial directory:

.. code-block:: bash

    cd $SCRATCHDIR/Practical2



Check input file and run the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step is to check that your `input file` is correct.
To do so, you will run (locally) :program:`SMILEI` in test mode:

.. code-block:: bash

    ./smilei_test 2 2 thermal_plasma_1d.py

If your simulation `input file` is correct, you can now `submit your job`.
In the previous practical, this was done `interactively`.
Now, we will proceed by submitting the job to the ``queuing system``.

Have a look at the ``submission script``:

.. code-block:: bash

    vim launcher

Once you've understand what's in the ``launcher``, just submit your job:

.. code-block:: bash

    llsubmit launcher

To check if your job is running:

.. code-block:: bash

    llq

Before going to the analysis of your simulation, check your ``log`` and ``err`` files `smilei.out` and `smilei.err`!


Preparing the post-processing tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, check what output files have been generated: what are they?

Let's now turn to analysing the output of your run with :program:`Happi` Python post-processing package.
To do so, open an ``ipython`` session:

.. code-block:: bash

    ipython

In the python session:

* import the :program:`Happi` package:

.. code-block:: python

    import happi

* open your simulation:

.. code-block:: python

    S = happi.Open('/gpfsdata/training[01-30]/Practical2/')

.. warning::

    Use your correct `training` identification number!

You are now ready to take a look at your simulation's results.

Having a look at the ``Field`` diagnostics using ``happi.multiPlot``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, to have a quick access at your data and `check` what is going on, you will plot the electron and ion densities 
together with the electrostatic field :math:`E_x`.

First, you have to load the data:

.. code-block:: python

    ne = S.Field(0,'-Rho_eon',vmin=-0.25,vmax=2)
    ni = S.Field(0,'Rho_ion')
    ex = S.Field(0,'Ex')

Now, you can plot all these quantities independently, e.g., using:

.. code-block:: python

    ex.plot()

or 

.. code-block:: python

    ex.animate()

But you can also use the ``multiPlot`` function of :program:`Happi`:

.. code-block:: python

    happi.multiPlot(ne,ni,ex)


Having a look at the ``ParticleBinning`` diagnostics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, have a look at the ``ParticleBinning`` diagnostics, and in particular at the electron energy distribution at initial and latest timesteps:

.. code-block:: python

    Nt    = int(S.namelist.tsim / S.namelist.dt)
    f_ini = S.ParticleBinning(0,data_log=True,timesteps=0)
    f_fin = S.ParticleBinning(0,data_log=True,timesteps=Nt)
    happi.multiPlot(f_ini,f_fin)




 
Effect of spatial resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before checking the effect of spatial resolution, first have a look at the total energy and energy balance in your simulation.
Note the level of energy imbalance at the end of this simulation for which :math:`\Delta x = \lambda_{\rm De}`.

Then, increase your spatial resolution to :math:`\Delta x = 16 \times \lambda_{\rm De}`.
Check again, from the ``Scalar`` diagnostics the level of energy imbalance at the end of the simulation.
What do you observe?
Can you check the electron spectrum at the beginning and end of the simulation?
What is going on?

Finally, increase your spatial resolution to :math:`\Delta x = 2\,c/\omega_{pe}`.
Check the evolution of the total energy.
What do you observe?
