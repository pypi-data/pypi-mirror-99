About
=====

`SPRING <http://spring.fz-juelich.de/>`_ (**S** \ingle **P** \article **R** \econstruction from **I** \mages \
of k\ **N** \own **G** \eometry) is a single-particle based helical reconstruction package for electron \
cryo-micrographs and has been used to determine 3D structures of a variety of highly ordered and less ordered \
specimens. Spring provides the entire single-particle based work-flow required for helical reconstruction including:

* Classification

* Helical symmetry determination and refinement tools

* High-resolution structure refinement 

* Multi-symmetry structure refinement

Spring is still maintained in the `Sachse <http://sachse.fz-juelich.de>`_ lab at the
`Ernst-Ruska Centre <http://www.fz-juelich.de/er-c/er-c-3>`_ of the `Research Centre Juelich <http://www.fz-juelich.de>`_ for the Unix operating systems of MacOSX and Linux. 


Reference
---------

If you find Spring useful for your research, please cite:

Desfosses, A., Ciuffa, R., Gutsche, I., and Sachse, C. (2014). SPRING - an image processing package for single-particle based helical reconstruction from electron cryomicrographs. `J Struct Biol 185, 15-26. <http://dx.doi.org/10.1016/j.jsb.2013.11.003>`_

For further information find more Spring-related `publications <http://spring.fz-juelich.de/publications.html>`_.


Installation
------------

We provide binary downloads that include all required components and build recipes for all dependencies. 
Follow `install <http://spring.fz-juelich.de/install.html>`_ instructions for more details.


Acknowledgements
----------------

Spring is released under the modified BSD lisence and integrates several different electron-microscopy specific and \
other open-source packages. Spring is entirely written in `Python <http://www.python.org>`_ and is based on the EM \
functions and libraries of:

#. `EMAN2.91 <http://blake.bcm.edu/emanwiki/EMAN2>`_ 

#. `SPARX <http://sparx-em.org/sparxwiki/SparxWiki>`_ 

#. `CTFFIND/CTFTILT <http://grigoriefflab.janelia.org/ctf>`_ 


Dependencies
------------

Spring makes use of a number of scientific computing packages:

* `Numpy and Scipy <http://numpy.scipy.org>`_ 

* `Mpi4py <http://mpi4py.scipy.org>`_

* `Matplotlib <http://matplotlib.sourceforge.net/>`_

* `Vispy <http://vispy.org>`_

* `SQLAlchemy <http://www.sqlalchemy.org>`_

