Practical 3: Weibel and two-stream instabilities
================================================

Goal of the tutorial
^^^^^^^^^^^^^^^^^^^^

The goal of this tutorial is to run to physics simulation relating to streaming instabilities,
and in particular to the electron Weibel and two-stream instabilities.

This tutorial will also allow you to:

* get familiar to the ``streak`` tool of :program:`Happi` that allows to plot quantities as a function of both time and space,

* extract instability growth rates,

* construct and extract phase-space distribution using the ``ParticleBinning`` diagnostics.

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^

In both simulations, a plasma with density :math:`n_0` is initialized (:math:`n_0 = 1` so that code units are plasma
units, i.e. times are normalized to the inverse of the electron plasma frequency 
:math:`\omega_{p0} = \sqrt{e^2 n_0/(\epsilon_0 m_e)}`, distances to the electron skin-depth :math:`c/\omega_{p0}`, etc...).
Ions are frozen during the whole simulation and just provide a neutralizing background.
Two electron species are initialized with density :math:`n_0/2` and a mean velocity :math:`\pm \bf{v_0}`.

* for the Weibel study, :math:`\bf{v_0} = v_0 \hat{\bf{z}}`,

* for the two-stream study, :math:`\bf{v_0} = v_0 \hat{\bf{x}}`.

Content of the tutorial
^^^^^^^^^^^^^^^^^^^^^^^
This tutorial consist in a single directory :program:`Practical3` containing:
 
* `weibel_1d.py`: the input file for the Weibel simulation.

* `two_stream_1d.py`: the input file for the two-stream simulation.

Setup the tutorial
^^^^^^^^^^^^^^^^^^

* If you're not yet there, connect on `Poincare` via `ssh` using the `-X` option:

.. code-block:: bash

    ssh -X poincare

* Copy the content of this tutorial in the `$SCRATCHDIR` of `Poincare`:

.. code-block:: bash

    cp -r Smilei/HandsOn/Practical3 $SCRATCHDIR/.

* Copy the executable files in the new folder:

.. code-block:: bash

    cp -r Smilei/smilei $SCRATCHDIR/Practical3/.
    cp -r Smilei/smilei_test $SCRATCHDIR/Practical3/.

* Go the tutorial directory:

.. code-block:: bash

    cd $SCRATCHDIR/Practical3

* Create to distinct directories for the two different studies (Weibel and two-stream):

.. code-block:: bash

    mkdir weibel
    mkdir two_stream

and move the respective `input files` in their respectives directory:

.. code-block:: bash

    mv weibel_1d.py weibel/.
    mv two_stream_1d.py two_stream/.

Now, depending on which study you wanna consider, go to either the ``weibel`` or ``two_stream`` directory.
All forthcoming information are given considering that you are either in one or the other directory.


Check input file and run the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step is to check that your `input files` are correct.
To do so, you will run (locally) :program:`SMILEI` in test mode:

.. code-block:: bash

    ../smilei_test 2 2 weibel_1d.py
    ../smilei_test 2 2 two_stream_1d.py

.. warning::

    Pay attention in which directory you are!
    At this point, you should be either in the ``weibel`` or ``two_stream`` directory.

If your simulation `input files` are correct, you can run your job.

.. code-block:: bash

    ../smilei 2 2 weibel_1d.py
    ../smilei 2 2 two_stream.py

Before going to the analysis of your simulation, check your ``log`` file!


Weibel study: analysing your datas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, in an :program:`ipython` terminal, open the simulation:

.. code-block:: ipython

    S = happi.Open('/gpfsdata/training[01-30]/Practical3/weibel/')

then, using the ``streak`` tool of :program:`Happi`, have a look at the total current density :math:`J_z` and 
magnetic field :math:`B_y` evolution in time:

.. code-block:: ipython

    S.Field(0,'Jz').streak()    
    S.Field(0,'By_m').streak()

Do you have any clue what is going on? 
Do not hesitate to use the ``animate`` tool if you do not get it:

.. code-block:: ipython

    jz = S.Field(0,'Jz')
    by = S.Field(0,'By_m',vmin=-0.5,vmax=0.5)
    happi.multiPlot(jz,by)

Now, using the ``Scalar`` diagnostics, check the temporal evolution of the energies in the magnetic (:math:`B_y`)
and electrostatic (:math:`E_z`) fields. Can you distinguish the linear and non-linear phase of the instability?

Have a closer look at the growth rates. Use the ``data_log=True`` options when loading your diagnostics, 
and the ``happi.multiPlot()`` tool and plot both energies as a function of time.
Can you extract the growth rates? What do they tell you?

If you have time, run the simulation for different wavenumbers :math:`k`.
Check the growth rate as a function of :math:`k`.

For those interested, you'll find more on: `Grassi et al., Phys. Rev. E 95, 023203 (2017) <https://journals.aps.org/pre/abstract/10.1103/PhysRevE.95.023203>`_.



Two-stream study: analysing your datas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, in an :program:`ipython` terminal, open the simulation:

.. code-block:: ipython

    S = happi.Open('/gpfsdata/training[01-30]/Practical3/two_stream/')

then, have a first look at your simulation results:

.. code-block:: ipython

    ne  = S.Field(0,'-Rho_eon1-Rho_eon2',xmin=0,xmax=1.3)
    ex  = S.Field(0,'Ex',xmin=0,xmax=1.3)
    phs = S.ParticleBinning(0)
    happi.multiPlot(ne,ex,phs)

Any clue what's going on? 

Now, let's have a look at the energy in the electrostatic field :math:`E_x`:

* can you distinguish the linear and non-linear phase of the instability?

* checking at the :math:`(x,p_x)`-phase-space distribution, can you get any clue on what leads the instability to saturate?

Then, try changing the simulation box size (which is also the wavelength of the considered perturbation), e.g. taking: 
:math:`L_x =` 0.69, 1.03 or 1.68 :math:`c/\omega_{p0}`. What do you observe?

Now, take :math:`L_x =` 0.6, 0.31 or 0.16 :math:`c/\omega_{p0}`. What are the differences? Can you explain them?



