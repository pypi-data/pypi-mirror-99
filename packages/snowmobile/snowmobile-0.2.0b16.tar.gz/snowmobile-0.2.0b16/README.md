# snowmobile

[![Documentation Status](https://readthedocs.org/projects/snowmobile/badge/?version=latest)](https://snowmobile.readthedocs.io/en/latest/?badge=latest#)
[![codecov](https://codecov.io/gh/GEM7318/Snowmobile/branch/0.2.1/graph/badge.svg?token=UCMCWRIIJ8)](https://codecov.io/gh/GEM7318/Snowmobile)
[![PyPI version](https://badge.fury.io/py/snowmobile.svg)](https://badge.fury.io/py/snowmobile)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/GEM7318/Snowmobile/blob/master/LICENSE.txt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`snowmobile` is a wrapper around the 
[Snowflake Connector for Python](https://docs.snowflake.com/en/user-guide/python-connector.html).

### Documentation
&nbsp;**[snowmobile.readthedocs.io](https://snowmobile.readthedocs.io/en/latest/index.html)**

### Installation
&nbsp;`pip install snowmobile`

---

### Development

#### Installs

- Core
    - pip: `pip install --user tested_requirements/requirements_37.reqs`
    - conda: `conda env create -f tested_requirements/environment.yml`
- docs: `pip install --user docs/requirements.txt`

#### Run

- test: `pytest --cov-report=xml --cov=snowmobile test/`
- docs: `sphinx-build -b html . _build`


<style>hr {height: 0.1em;}</style>
