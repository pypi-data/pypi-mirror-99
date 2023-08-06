# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maser',
 'maser.data',
 'maser.data.cdpp',
 'maser.data.cdpp.demeter',
 'maser.data.cdpp.interball',
 'maser.data.cdpp.isee3',
 'maser.data.cdpp.viking',
 'maser.data.cdpp.wind',
 'maser.data.nancay',
 'maser.data.nancay.nda',
 'maser.data.padc',
 'maser.data.padc.lesia',
 'maser.data.padc.lesia.cassini',
 'maser.data.padc.radiojove',
 'maser.data.pds',
 'maser.data.pds.cassini',
 'maser.data.pds.cassini.rpws',
 'maser.data.pds.galileo',
 'maser.data.pds.ppi',
 'maser.data.pds.ppi.voyager',
 'maser.data.pds.voyager',
 'maser.data.psa',
 'maser.data.psa.mex',
 'maser.data.psa.mex.marsis',
 'maser.data.tests',
 'maser.data.wind',
 'maser.data.wind.waves',
 'maser.services',
 'maser.utils',
 'maser.utils.cdf',
 'maser.utils.cdf.cdf',
 'maser.utils.cdf.cdfcompare',
 'maser.utils.cdf.serializer',
 'maser.utils.cdf.validator',
 'maser.utils.das2stream',
 'maser.utils.time',
 'maser.utils.toolbox']

package_data = \
{'': ['*'],
 'maser': ['support/cdf/*', 'support/data/*'],
 'maser.data.tests': ['data/*']}

install_requires = \
['astropy',
 'jinja2',
 'numpy',
 'openpyxl',
 'python-dateutil',
 'pytz',
 'scipy',
 'spacepy==0.2.2',
 'toml']

extras_require = \
{'tests': ['pytest>=5.2,<6.0',
           'pytest-cov==2.10.1',
           'pytest-timeout>=1.4,<2.0']}

entry_points = \
{'console_scripts': ['maser = maser.script:main']}

setup_kwargs = {
    'name': 'maser4py',
    'version': '0.9.0',
    'description': 'maser4py offers tools to handle low frequency radioastronomy data',
    'long_description': '[![PyPI version](https://badge.fury.io/py/maser4py.svg)](https://img.shields.io/pypi/pyversions/maser4py)\n[![license](https://img.shields.io/pypi/l/maser4py)](https://pypi.python.org/pypi/maser4py)\n[![Documentation Status](https://readthedocs.org/projects/maser/badge/?version=latest)](https://maser.readthedocs.io)\n\nAbout maser4py\n==============\n\n**maser4py** python package offers tools for radioastronomy at low frequency.\n\nIt contains modules to deal with services, data and tools provided in the framework\nof the MASER portal (http://maser.lesia.obspm.fr).\n\nRead maser4py [documentation][maser4py readthedocs] for more information.\n\n[maser4py readthedocs]: https://maser.readthedocs.io/en/latest\n\nInstallation\n==============\n\nPrerequisites\n--------------\n\n\nPython 3 must be available (tested with 3.6 and 3.8).\n\nThe maser4py also requires the NASA CDF software to be run (visit http://cdf.gsfc.nasa.gov/ for more details). Especially the CDFLeapSeconds.txt file\nshould be on the local disk and reachable from the $CDF_LEAPSECONDSTABLE env. variable. If it is not the case, maser4py offers tools to read and/or download\nthis file from the NASA Web site (see user manual for more details).\n\nUsing pip\n----------\n\nFrom a terminal, enter:\n\n   pip install maser4py\n\nUsing source\n-------------\n\nFrom a terminal, enter:\n\n    git clone https://github.com/maserlib/maser4py\n\nThen, from the maser4py directory, enter:\n\n    pip install -r requirements.txt\n\nThen,\n\n    python3 setup.py install\n\n\nUsage\n======\n\nFrom Python, enter "import maser".\nThe module also offers specific command line interfaces.\n\nFor more details, see the maser4py user manual.\n\nContent\n=========\n\nThe maser4py directory contains the following items:\n\n::\n\n    doc/  stores the maser4py documentation (source and build)\n\n    maser/ stores the maser4py source files\n\n    scripts/ store scripts to run/test/manage maser4py\n\n    __main__.py python script to run maser.main program\n\n    CHANGELOG.rst software change history log\n\n    MANIFEST.in files to be included to the package installation (used by   tup.py)\n\n    pyproject.tom Python package pyproject file\n\n    README.md current file\n\n    requirements.txt list of python package dependencies and versions\n\n    setup.cfg file used by sphinx to build the maser4py doc.\n\n    setup.py maser4py package setup file\n\nAbout MASER project\n====================\n\nThe MASER (Measuring, Analyzing & Simulating Emissions in the Radio range) portal is offering access to a series of tools and databases linked to low frequency radioastronomy (a few kilohertz to a few tens of megahertz). Radio measurements in this spectral range are done with ground based observatories (for frequencies above the terrestrial ionosphere cutoff at 10 MHz) or from space based platforms (at low frequencies).\n\nIn this frequency range, the main radio sources are the Sun and the magnetized planets. Measurements of the low frequency electric and magnetic field fluctuations can also provide local plasma diagnostics and in-situ observations of plasma waves phenomena in the Solar Wind or in planetary environments.\n\n* For more information about the MASER project: http://maser.lesia.obspm.fr/\n* For more information about MASER4PY: https://github.com/maserlib/maser4py\n\nAcknowledgements\n==================\n\nThe development of the MASER library is supported by Observatoire de Paris, CNRS (Centre National de la Recherche Scientique) and CNES (Centre National d\'Etudes Spatiales). The technical support from PADC (Paris Astronomical Data Centre) and CDPP (Centre de Données de la Physique des Plasmas) is also acknowledged.\n\nThe project has also received support from the European Union through:\n* HELIO (Heliophysics Integrated Observatory), which received funding from Capacities Specific Programme of the European Commission\'s Seventh Framework Programme (FP7) under grant agreement No 238969;\n* EPN2020RI (Europlanet 2020 Research Infrastructure project), which received funding from the European Union\'s Horizon 2020 research and innovation programme under grant agreement No 654208.\n',
    'author': 'Xavier BONNIN',
    'author_email': 'xavier.bonnin@obspm.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/maser4py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
