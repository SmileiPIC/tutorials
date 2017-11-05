Practical 4: Field ionization
=============================

Goal of the tutorial
^^^^^^^^^^^^^^^^^^^^

The goal of this tutorial is to present a simulation using an advanced physics module, namely the field (tunnel) ionization module.
In the presence of tunnel ionization, one needs to fixe the reference time/spatial scale.
In :program:`Smilei`, this is done by defining in SI units, the reference angular frequency parameter: ``reference_angular_frequency_SI``.

Briefly, this practical will help you:

* get familiar with the use of an `advanced physics module` and with the use of ``reference_angular_frequency_SI``,

* use the ``.getData()`` tool of :program:`Happi` to analyse your data and make your own figures.

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^

In a 1D cartesian geometry, a thin layer of neutral Carbon is set-up in the simulation box.
It is irradiated and thus ionized by a linearly polarized light pulse with intensity :math:`I = 5\times 10^{16}~{\rm W/cm^2}` with Gaussian time profile.



Content of the tutorial
^^^^^^^^^^^^^^^^^^^^^^^
This tutorial consist in a single directory :program:`Practical4` containing:
 
* `tunnel_ionization_1d.py`: the input file for the simulation,

* `analysis.py`: a Python file that will be executed to analyse the simulation,

* `solve_rate_eqs.py`: a Python file called by ``analysis.py`` to solve the system of rate equations numerically.


Setup the tutorial
^^^^^^^^^^^^^^^^^^

* If you're not yet there, connect on `Poincare` via `ssh` using the `-X` option:

.. code-block:: bash

    ssh -X poincare

* Copy the content of this tutorial in the `$SCRATCHDIR` of `Poincare`:

.. code-block:: bash

    cp -r Smilei/handson/Practical4 $SCRATCHDIR/.

* Copy the executable files in the new folder:

.. code-block:: bash

    cp -r Smilei/smilei $SCRATCHDIR/Practical4/.
    cp -r Smilei/smilei_test $SCRATCHDIR/Practical4/.

* Go the tutorial directory:

.. code-block:: bash

    cd $SCRATCHDIR/Practical4



Check input file and run the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step is to check that your `input file` is correct.
To do so, you will run (locally) :program:`SMILEI` in test mode:

.. code-block:: bash

    ./smilei_test 1 1 tunnel_ionization_1d.py

.. warning::

    For this simulation, we have specified in the input file that only 1 patch is created.
    Therefore, this simulation can be run using a single processor only!

If your simulation `input file` is correct, you can `submit your first job`.
As a first step, you will do this in `interactive mode`, that is directly running:

.. code-block:: bash

    ./smilei 1 1 tunnel_ionization_1d.py

Before going to the analysis of your simulation, check your ``log`` file!


Analysing the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^

You can access the various data of the simulation as done before.
However, for this particular practical, we have preparer a Python script that will do the work for you.
Open the ``analysis.py`` file and have look at what it does.
Note that it calls for the ``solve_rate_eqs.py`` file that is used to compute the rate equations (obtained theoretically).

.. warning::

    Before running ``analysis.py``, pay attention to give the correct path to your simulation results by defining the
    ``simulation_to_analyse`` variable!

Then open an :program:`ipython` terminal 

.. code-block:: bash

    ./smilei 1 1 tunnel_ionization_1d.py

and run the ``analysis.py`` file:

.. code-block:: python

    %run analysis.py

What do you obtain? Check also if any .eps file is generated.

.. warning::

    Note that in ``analysis.py`` some lines containing LateX commands have been commented.
    This is because no LateX package is available on :program:`Poincare`.
    However, if such a package is available on your machine or super-computer, it might be useful to have higher quality figures.