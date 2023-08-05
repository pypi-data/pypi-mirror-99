Changelog
=========

0.87.1717 (2021-03-08)
----------------------
* Internal upgrade to EMAN2 (v2.91 March 2021) and python3


0.86.1661 (2017-12-12)
----------------------
* MICHELIXTRACE: release of algorithm as published in Huber et al. 2017 including statistical thresholding, search for optimal parameter combination and persistence length pruning
* Web-based Helical Diffraction Simulator on http://spring.embl.de based on SEGLAYER2LATTICE.


0.85.1617 (2017-07-12)
----------------------
* MICCTFDETERMINE: updated to work with ctffind4.
* SEGCLASSRECONSTRUCT: updated to work with binning option.
* SEGMENTCLASS: updates to work with larger datasets for classification to reduce memory issues.
* SEGCLASSLAYER: addition of ‘B-factor’ option to adjust high-resolution layer-line contrast.
* SEGREFINE3DINSPECT: Bfactor/Resolution cutoff option separated from long helix option.
* MICHELIXTRACE: Algorithm update to increase robustness of filament tracing.
* SEGREFINE3DGRID/SEGGRIDEXPLORE: Now with out-of-plane deviation parameter.  
* SEGMENTPLOT/SEGREFINE3DPLOT: Now plots quantities on micrograph if subset micrograph chosen.
* Updated to work with SLURM cluster

0.84.1470 (2016-01-04)
----------------------
General bugfixes and improvement in stability.  Addition of explanatory tool tips.

1. SEGCLASSEXAM

* Multiple bugfixes including wrong computation of pixelsize.

2. SEGMENTREFINE3D

* Addition of new parameter "Choose out-of-plane tilt for amplitude correlation."

3. Installation procedures                          

* Updated dependencies GCC, matplotlib, libpng including build procedures.

0.83.1449 (2015-1-26)
---------------------
* Fixes in SEGMENTREFINE3D procedure, now also works for non-zero out-of-plane tilts.

0.83.1432 (2014-12-30)
----------------------

* Fixes and improvements

1. Installation procedures
                          
* Updated dependencies GCC, Numpy, Scipy, Openmpi including build procedures.

2. SEGMENTREFINE3D
                  
* Computation of persistence length at the end of each refinement run. Can be used now as a selection criterion for discarding less straight helices in the next refinement run.
* Selection criteria: Straight helices, Layer-line correlation and Projection matching cross-correlation are now selected in percent range of the distribution instead of cutoff values, e.g. upper 20 % --> 80 - 100 %.
* 'Continue refinement option' - in case no reference structure is given a 3D reconstruction based on the provided parameters is now created for further refinement.
* Improved segment-based motion correction, now accepts mrcs-stacks.
* Computation of structure-masked FSC with mask deconvolution according to Ultramicroscopy Chen et al. 2013 (Scheres and Henderson) for resolutions better than 12 Angstrom.
* Added error estimates for forward x-shift, forward out-of-plane tilt and in-plane rotation angles according to Sachse et al, 2007 J Mol Biol.
* Overhaul in symmetrization of volumes to make them perfectly even.
* Diagnostic power spectra are now always written out as EMAN2 image files in addition to diagnostic summary.

3. High-performance computing cluster 

* Added support for SLURM. 

4. SEGMENTCLASS, SEGLAYERLATTICE
                                
* Many minor fixes.

Note: old refinement.dbs and grid.dbs need to be upgraded to be readable by the latest Spring version.

.. code-block:: console

   % spring -udb='grid.db' -inp grid.db -out grid_upd.db
   % spring -udb=refinement.db -inp=refinement024.db -out=refinement024_up.db



0.82.1339 (2014-09-15)
----------------------

* Improved installation procedures including build and binary install scripts.



0.82.1339 (2014-04-25)
----------------------

* General fixes, optimizations and enhancements

1. SEGMENTREFINE3D
                  

* Fixes for data sets with large number of asymmetric units
* Fix/workaround for occasional database lock problems on cluster mounted nodes
* Fix in 'Absolute limit of x and y-shifts' handling. Now properly respects this.
* Declared some options as experimental: support remains limited.
* Occasional over-estimation of FSC fixed due to densities at upper and lower ends of filament
* Implementation of 'independent half-set' refinement (a.k.a. gold-standard refinement)

Note: the update will break reading your previous refinement.db files
Database files can be updated as follows:

.. code-block:: console

   % spring -udb=refinement.db -inp=refinement024.db -out=refinement024_up.db

2. SEGREFINE3DINSPECT
                     
* Additional option of signal-to-noise weighting using FSC file.

3. SEGLAYER2LATTICE
                   
* Simulation of layer-line pattern takes rotational symmetry into account



0.81.1282 (2014-01-26)
----------------------

* Fixes, enhancements and optimization

1.  SEGMENTREFINE3D
                   

* Disk requirements for temporary directories revised.
* Improved handling of selected segments. Spring processes helices as one entity and discards them later for 3D reconstruction.
* FSC only computed with cylinder mask.
* Improved experimental power spectra for high/maximum resolution analysis.

2. SEGMENT
          
* Fix in frame processing.
* Rotated stack only written if requested.

3. SEGMENTEXAM
              
* Addition of selection options from spring.db.

4. SEGCLASSEXAM
               
* Addition of mpi option.

5. SEGLAYER2LATTICE
                   
* Addition of tooltips of predicted Bessel orders.

6. SEGCLASSLAYER
                
* Accepts also power spectra as input.
* Added tooltips on Bessel look up table.

7. General
          
* Parameter input from prompt now works using Tab auto completion including file search.
