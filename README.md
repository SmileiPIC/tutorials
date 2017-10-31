 L'aspect doc n'étant pas disponible sur le calculateur (voir en bas de ce mail), si on veut faire on compiler la doc il faudra que les sources soient à un moment disponible sur la station de travail.
Du coup je privilégie la solution github qui transite par la station décrite ci-dessous :


    # la définition de GIT_SSH_COMMAND sera embarquée dans le .bash_profile du compte training, il ne sera pas nécessaire de la taper
    # J'ai associé à mon compte github la clé ssh des comptes training
    training@mdlspc147:~$  export GIT_SSH_COMMAND='ssh -i ~/.ssh/id-rsa-poincare -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'

    training@mdlspc147:~$  git clone --depth=1 git@github.com:SmileiPIC/Smilei.git
    ...
    training@mdlspc147:~$  scp -r Smilei poincare:~/
    ...


    training@mdlspc147:~$ ssh poincare -X
    ...
    # l'environnement Smilei sera chargé dans le .bash_profile
    # il devra être précisé et expliqué (IntelMPI, thread_multiple, HDF5 ...) dans les consignes/slides à disposition
    # mais l'idée est de ne pas perdre de temps sur cet aspect en faisant manipuler l'environnement aux utilisateurs
    [training08@poincareint01:~] $ module list # module
    Currently Loaded Modulefiles:
      1) intel/15.0.0                    3) hdf5/1.8.16_intel_intelmpi_mt   5) gnu/4.7.2
      2) intelmpi/5.0.1                  4) python/anaconda-2.1.0

    [training08@poincareint01:~/Smilei] $ make -j 8
    ...

    [training08@poincareint01:~/Smilei] $ s smilei
    smilei

    # session batch interactive, N noeuds (16 cores dédiés pendant H heures)
    [training08@poincareint01:~/Smilei] $ llinteractif N clallmds+ H
    [training08@poincare003:~/Smilei] mpirun -np blabla ./smilei truc.py
    ...

    # le post-processing se fait depuis les frontales de Poincaré, pas en batch
    [training08@poincareint01:~/Smilei] ipython -i 
    ... 


Sphinx n'est pas et ne sera disponible sur le calculateur (pas de navigateur web sur le calculateur) mais sur les stations de travail.

    training@mdlspc147:~/Smilei$ make doc
    ...
    training@mdlspc147:~/Smilei$ ls doc/html/Sphinx/html/index.html
    doc/html/Sphinx/html/index.html 
    [training08@poincareint01:~/Smilei] $ make happi
    Installing /gpfshome/mds/grptraining/training08/.local/lib/python2.7/site-packages/smilei.pth
    [training08@poincareint01:~/Smilei] $ python
    ...
    >>> import happi
    >>>

Concernant les benchs qui ne seraient pas disponible sur le repository, on peut mettre à disposition un répertoire sur Poincaré dans lequel serait stockées toutes les données pertinentes :

    [training08@poincareint01:~/Smilei]$ ls /gpfslocal/pub/smilei.data
