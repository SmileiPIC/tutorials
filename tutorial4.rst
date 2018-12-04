Tutorial 4: Field ionization
=============================

The goal of this tutorial is to present a simulation using an advanced physics module,
namely the field (tunnel) ionization module.
In the presence of tunnel ionization, one needs to set a reference temporal/spatial scale.
In :program:`Smilei`, this is done by defining, in SI units, the reference angular
frequency parameter: ``reference_angular_frequency_SI``.

Briefly, this tutorial will help you:

* use the ``reference_angular_frequency_SI``
* use the ``.getData()`` tool of :program:`happi` to analyse your data and make your own figures.

----

Physical configuration
^^^^^^^^^^^^^^^^^^^^^^

Download the input file `tunnel_ionization_1d.py <tunnel_ionization_1d.py>`_ as well as
the analysis scripts `analysis.py <analysis.py>`_ and `solve_rate_eqs.py <solve_rate_eqs.py>`_.

In a 1D cartesian geometry, a thin layer of neutral carbon is irradiated (thus ionized)
by a linearly-polarized laser pulse with intensity :math:`I = 5\times 10^{16}~{\rm W/cm^2}`
and a gaussian time profile.

----

Check the input file and run the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step is to check that your `input file` is correct.
To do so, you will run (locally) :program:`Smilei` in test mode:

.. code-block:: bash

    ./smilei_test tunnel_ionization_1d.py

If your simulation `input file` is correct, you can run the simulation.

.. warning::

    For this simulation, we have specified in the input file that only 1 patch is created.
    Therefore, this simulation can be run using a single processor only!

Before going to the analysis of your simulation, check your ``log`` file!


----

Analyse the simulation
^^^^^^^^^^^^^^^^^^^^^^^^^

You can access the various data of the simulation as done before.
However, for this particular tutorial, we have prepared a *python* script that will
do the work for you.
Open the ``analysis.py`` file and have look at what it does.
Note that it calls for the ``solve_rate_eqs.py`` file that is used to compute
the rate equations (obtained theoretically).

.. warning::

    Before running ``analysis.py``, give the correct path to your simulation results by defining the
    ``simulation_to_analyse`` variable!

In an *ipython* prompt, run the analysis file:

.. code-block:: python

    %run analysis.py

What do you obtain? Check also if any ``.eps`` file is generated.

.. warning::

    Note that in ``analysis.py`` some lines containing LateX commands have been commented.
    If your machine has LateX installed, it might be useful to have higher-quality figures.