
# pySPEDAS
[![build](https://github.com/spedas/pyspedas/workflows/build/badge.svg)](https://github.com/spedas/pyspedas/actions)
[![Coverage Status](https://coveralls.io/repos/github/spedas/pyspedas/badge.svg)](https://coveralls.io/github/spedas/pyspedas)
[![Version](https://img.shields.io/pypi/v/pyspedas.svg)](https://pypi.org/project/pyspedas/)
![License](https://img.shields.io/pypi/l/pyspedas.svg)
![Status](https://img.shields.io/pypi/status/pyspedas.svg)

pySPEDAS is an implementation of the SPEDAS framework in python. 

The Space Physics Environment Data Analysis Software ([SPEDAS](http://spedas.org/wiki)) framework is written in IDL and contains data loading, data analysis and data plotting tools for various scientific missions (NASA, NOAA, etc.) and ground magnetometers.   

## Projects Supported
- [Advanced Composition Explorer (ACE)](https://github.com/spedas/pyspedas/blob/master/pyspedas/ace/README.md)
- [Arase (ERG)](https://github.com/spedas/pyspedas/blob/master/pyspedas/erg/README.md)
- [Cluster](https://github.com/spedas/pyspedas/blob/master/pyspedas/cluster/README.md)
- [Colorado Student Space Weather Experiment (CSSWE)](https://github.com/spedas/pyspedas/blob/master/pyspedas/csswe/README.md)
- [Deep Space Climate Observatory (DSCOVR)](https://github.com/spedas/pyspedas/blob/master/pyspedas/dscovr/README.md)
- [Equator-S](https://github.com/spedas/pyspedas/blob/master/pyspedas/equator_s/README.md)
- [Fast Auroral Snapshot Explorer (FAST)](https://github.com/spedas/pyspedas/blob/master/pyspedas/fast/README.md)
- [Geotail](https://github.com/spedas/pyspedas/blob/master/pyspedas/geotail/README.md)
- [Geostationary Operational Environmental Satellite (GOES)](https://github.com/spedas/pyspedas/blob/master/pyspedas/goes/README.md)
- [Imager for Magnetopause-to-Aurora Global Exploration (IMAGE)](https://github.com/spedas/pyspedas/blob/master/pyspedas/image/README.md)
- [Mars Atmosphere and Volatile Evolution (MAVEN)](https://github.com/spedas/pyspedas/blob/master/pyspedas/maven/README.md)
- [Magnetic Induction Coil Array (MICA)](https://github.com/spedas/pyspedas/blob/master/pyspedas/mica/README.md)
- [Magnetospheric Multiscale (MMS)](https://github.com/spedas/pyspedas/blob/master/pyspedas/mms/README.md)
- [OMNI](https://github.com/spedas/pyspedas/blob/master/pyspedas/omni/README.md)
- [Polar Orbiting Environmental Satellites (POES)](https://github.com/spedas/pyspedas/blob/master/pyspedas/poes/README.md)
- [Polar](https://github.com/spedas/pyspedas/blob/master/pyspedas/polar/README.md)
- [Parker Solar Probe (PSP)](https://github.com/spedas/pyspedas/blob/master/pyspedas/psp/README.md)
- [Van Allen Probes (RBSP)](https://github.com/spedas/pyspedas/blob/master/pyspedas/rbsp/README.md)
- [Solar Orbiter (SOLO)](https://github.com/spedas/pyspedas/blob/master/pyspedas/solo/README.md)
- [Solar Terrestrial Relations Observatory (STEREO)](https://github.com/spedas/pyspedas/blob/master/pyspedas/stereo/README.md)
- [Time History of Events and Macroscale Interactions during Substorms (THEMIS)](https://github.com/spedas/pyspedas/blob/master/pyspedas/themis/README.md)
- [Two Wide-Angle Imaging Neutral-Atom Spectrometers (TWINS)](https://github.com/spedas/pyspedas/blob/master/pyspedas/twins/README.md)
- [Ulysses](https://github.com/spedas/pyspedas/blob/master/pyspedas/ulysses/README.md)
- [Wind](https://github.com/spedas/pyspedas/blob/master/pyspedas/wind/README.md)

## Requirements

Python 3.7+ is required.  

We recommend [Anaconda](https://www.continuum.io/downloads/) which comes with a suite of packages useful for scientific data analysis. 

## Installation

pySPEDAS supports Windows, macOS and Linux. To get started, install the `pyspedas` package using PyPI:

### PyPI

```bash
pip install pyspedas --upgrade
```

## Usage

To get started, import pyspedas and pytplot:

```python
import pyspedas
from pytplot import tplot
```

You can load data into tplot variables by calling `pyspedas.mission.instrument()`, e.g., 

To load and plot 1 day of THEMIS FGM data for probe 'd':
```python
thm_fgm = pyspedas.themis.fgm(trange=['2015-10-16', '2015-10-17'], probe='d')

tplot(['thd_fgs_gse', 'thd_fgs_gsm'])
```

To load and plot 2 minutes of MMS burst mode FGM data:
```python
mms_fgm = pyspedas.mms.fgm(trange=['2015-10-16/13:05:30', '2015-10-16/13:07:30'], data_rate='brst')

tplot(['mms1_fgm_b_gse_brst_l2', 'mms1_fgm_b_gsm_brst_l2'])
```

Note: by default, pySPEDAS loads all data contained in CDFs found within the requested time range; this can potentially load data outside of your requested trange. To remove the data outside of your requested trange, set the `time_clip` keyword to `True`

To load and plot 6 hours of PSP SWEAP/SPAN-i data:
```python
spi_vars = pyspedas.psp.spi(trange=['2018-11-5', '2018-11-5/06:00'], time_clip=True)

tplot(['DENS', 'VEL', 'T_TENSOR', 'TEMP'])
```

To download 5 days of STEREO magnetometer data (but not load them into tplot variables):
```python
stereo_files = pyspedas.stereo.mag(trange=['2013-11-1', '2013-11-6'], downloadonly=True)
```

### Standard Options
- `trange`: two-element list specifying the time range of interest. This keyword accepts a wide range of formats
- `time_clip`: if set, clip the variables to the exact time range specified by the `trange` keyword 
- `suffix`: string specifying a suffix to append to the loaded variables
- `varformat`: string specifying which CDF variables to load; accepts the wild cards * and ?
- `get_support_data`: if set, load the support variables from the CDFs
- `downloadonly`: if set, download the files but do not load them into tplot
- `no_update`: if set, only load the data from the local cache
- `notplot`: if set, load the variables into dictionaries containing numpy arrays (instead of creating the tplot variables)

## Getting Help
To find the options supported, call `help` on the instrument function you're interested in:
```python
help(pyspedas.themis.fgm)
```

You can ask questions by creating an issue or by joining the [SPEDAS mailing list](http://spedas.org/mailman/listinfo/spedas-list_spedas.org).

## Contributing
We welcome contributions to pySPEDAS; to learn how you can contribute, please see our [Contributing Guide](https://github.com/spedas/pyspedas/blob/master/CONTRIBUTING.md)

## Code of Conduct
In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation. To learn more, please see our [Code of Conduct](https://github.com/spedas/pyspedas/blob/master/CODE_OF_CONDUCT.md).

## Additional Information

For examples of pyspedas, see: https://github.com/spedas/pyspedas_examples

For MMS examples, see: https://github.com/spedas/mms-examples

For pytplot, see: https://github.com/MAVENSDC/PyTplot

For cdflib, see: https://github.com/MAVENSDC/cdflib

For SPEDAS, see http://spedas.org/
