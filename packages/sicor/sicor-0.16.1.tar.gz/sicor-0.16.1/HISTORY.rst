=======
History
=======


0.x.x (coming soon)
--------------------

New features:
*

Bugfixes:
*


0.16.1 (2021-03-24)
--------------------

New features:
* 'make lint' now directly prints errors instead of only logging them to logfiles.
* Automatic retraining of S2 novelty detector in case pretrained scikit-learn random forest model is out of date.

Bugfixes:
* Pinned gdal to version<=3.1.2 to avoid import error.
* Fixed bug in empirical line function, which caused one single remaining unprocessed segmentation label.
* Replaced deprecated gdal imports to fix "DeprecationWarning: gdal.py was placed in a namespace, it is now available as osgeo.gdal".
* Updated cerberus schema for SicorValidator to avoid missing path warning in case of LUT file.
* Updated download link and file size of S2 novelty detector and unpinned scikit-learn version.


0.16.0 (2021-02-23)
--------------------

New features:
* Transformation of VNIR data cube to SWIR sensor geometry to enable accurate segmentation and first guess retrievals.
* Well-arranged separation between EnMAP-specific AC and generic AC.
* Added incorporation of uncertainties due to model unknowns.
* Extended options files with additional parameters:
  * Prior mean and standard deviation of state vector parameters
  * Standard deviations of model unknowns
  * Inversion parameters
* Extended optional output of Optimal Estimation:
  * Jacobian of solution state
  * Convergence message
  * Number of iterations
  * Gain matrix
  * Averaging kernel matrix
  * Value of cost function
  * Degrees of freedom
  * Information content
  * Retrieval noise
  * Smoothing error
* Updated first guess retrievals.

Bugfixes:
* Updated keyword for excluding patterns from URL check.
* Fixed bug in LUT file assertion.
* Removed slow inversion method based on downhill simplex algorithm.
* Removed option to turn off ice retrieval.


0.15.6 (2021-02-05)
--------------------

New features:
* Two optional processing modes for EnMAP data: 'land only' and 'land + water' based on water mask.

Bugfixes:
* Fixed bug in LUT file assertion.
* Replaced pandas xlrd dependency by openpyxl.


0.15.5 (2021-01-21)
--------------------

New features:
* Improved handling of clear and cloudy fraction. Additional logger warnings and infos are now printed.

Bugfixes:
* Fixed Qhull error within water vapor retrieval, which occurred while processing extremely cloudy images.


0.15.4 (2021-01-13)
--------------------

New features:
>>>>>>> HISTORY.rst
* Improved consistency in the logging of ECMWF errors within ac_gms().
* Default values and units for multispectral AC are now printed to the logs.

Bugfixes:
* Deprecated raise of assertion error in case the LUT file only represents an LFS pointer.
* Fixed "RuntimeWarning: overflow encountered in reduce" within ac_gms().
* Implemented CWV default value for AC of Landsat data in case no ECMWF data are available.


0.15.3 (2020-11-12)
--------------------

New features:
* Separated CI Jobs for optionally testing AC of EnMAP and/or Sentinel-2 data.

Bugfixes:
* Fixed Qhull error caused by scipy griddata function in except clause of ac_interpolation.
* Fixed error in getting ECMWF data.
* Modified input points and values for scipy RegularGridInterpolator to avoid NaN in interpolated variable.


0.15.2 (2020-10-22)
--------------------

New features:
* New handling of Sentinel-2 and Landsat-8 options files.

Bugfixes:
* Improved multispectral AC tables download during runtime by implementing an automatic check for table availability.


0.15.1 (2020-10-16)
--------------------

New features:
* Re-enabled and updated CI job for testing AC of Sentinel-2 data.

Bugfixes:
* Fixed scipy QHull error in interpolation function within Sentinel-2 AC.
* Updated package requirements.


0.15.0 (2020-10-12)
--------------------

New features:
* SICOR is now available as conda package on conda-forge.


0.14.6 (2020-10-05)
-------------------

New features:
* All needed AC tables both for hyper- and multispectral mode are now downloaded during runtime
* 'deploy_pypi' CI job is finally working after fixing some bugs.

Bugfixes:
* Fixed documentation links.
* Fixed pip install error caused by basemap library.


0.14.5 (2020-09-23)
-------------------

New features:
* Additional tables for multispectral mode are now downloaded during pip install.

Bugfixes:
* Moved imports of scikit-image from module level to function level to avoid
  'ImportError: dlopen: cannot load any more object with static TLS'.
* Fixed DeprecationWarnings h), i), and j) from issue #53.


0.14.4 (2020-09-07)
-------------------

New features:
* AC LUT is now downloaded during setup.py.

Bugfixes:
* Fixed issue #62 (ecmwf-api-client ImportError after following the installation instructions for the hyperspectral
  part of SICOR).


0.14.3 (2020-09-02)
-------------------

New features:
* The package is now available on the Python Package Index.
* Added 'deploy_pypi' CI job.


0.14.2 (2020-05-14)
-------------------

New features:
* Segmentation of input radiance data cubes to enhance processing speed.
* Empirical line solution for extrapolating reflectance spectra based on segment averages.


0.14.1 (2019-02-18)
-------------------

New features:
* Optimal estimation for atmospheric and surface parameters.
* Calculation of retrieval uncertainties.


0.14.0 (2019-02-11)
-------------------

New features:
* New EnMAP atmospheric correction.
* 3 phases of water retrieval for hyperspectral data.


0.13.0 (2018-12-18)
-------------------

* Development by Niklas Bohn started.
