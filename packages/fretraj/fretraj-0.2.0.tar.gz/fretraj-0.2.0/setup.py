# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fretraj']

package_data = \
{'': ['*'], 'fretraj': ['UI/*', 'examples/*', 'skripts/*']}

install_requires = \
['PyQt5>=5.12.3,<6.0.0',
 'astunparse==1.6.2',
 'importlib-metadata>=3.7.2,<4.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'mdtraj>=1.9.5,<2.0.0',
 'nglview>=2.7.7,<3.0.0',
 'numba<=0.50.1',
 'numpy<1.20.0',
 'pandas>=1.2.2,<2.0.0',
 'pybind11>=2.6.2,<3.0.0',
 'tqdm>=4.59.0,<5.0.0']

entry_points = \
{'console_scripts': ['fretraj = fretraj.cloud:main',
                     'fretraj_gui = fretraj.fretraj_gui:main',
                     'pymol_vis = fretraj.console:pymol_vis',
                     'vmd_vis = fretraj.console:vmd_vis']}

setup_kwargs = {
    'name': 'fretraj',
    'version': '0.2.0',
    'description': 'Predicting FRET with accessible-contact volumes',
    'long_description': '<img src="https://raw.githubusercontent.com/fdsteffen/fretraj/master/docs/images/fretraj_logo_readme.png">\n\n[![Build Status](https://github.com/fdsteffen/fretraj/workflows/FRETraj%20build/badge.svg)](https://github.com/fdsteffen/fretraj/actions)\n[![Docs Status](https://github.com/fdsteffen/fretraj/workflows/FRETraj%20docs/badge.svg)](https://github.com/fdsteffen/fretraj/actions)\n[![PyPI](https://img.shields.io/pypi/v/fretraj)](https://pypi.org/project/fretraj/)\n[![Anaconda-Server Badge](https://img.shields.io/badge/Install%20with-conda-green.svg)](https://anaconda.org/rna-fretools/fretraj)\n[![codecov](https://codecov.io/gh/fdsteffen/fretraj/branch/master/graph/badge.svg?token=A2E70FbycQ)](https://codecov.io/gh/fdsteffen/fretraj)\n\n*FRETraj* is a Python module for calculating **multiple accessible-contact volumes** (multi-ACV) and predicting **FRET efficiencies**. It provides an interface to the [*LabelLib*](https://github.com/Fluorescence-Tools/LabelLib) library to simulate fluorophore dynamics. The package features a user-friendly **PyMOL plugin**<sup>[1](#pymol)</sup> which can be used to explore different labeling positions when designing FRET experiments. In an AV simulation the fluorophore distribution is estimated by a shortest path search (Djikstra algorithm) using a coarse-grained dye probe. *FRETraj* further implements a **Python-only** version of the geometrical clash search used in *LabelLib*. This should facilitate prototyping of new features for the ACV algorithm.\n\n<img src="https://raw.githubusercontent.com/fdsteffen/fretraj/master/docs/images/graphical_abstract.png">\n     \nA recent addition to the original AV model (Kalinin et al. *Nat. Methods*, 2012) is the so-called **contact volume** (Steffen et. al. *PCCP* 2016). Here, the accessible volume is split into a free volume (FV, transparent) where the dye is freely diffusing and a contact volume (CV, opaque) where the dye stacks to the biomolecular surface. Time-resolved anisotropy experiments suggest that certain fluorophores, among those the commonly used cyanines Cy3 and Cy5, are particularly prone to interact with both proteins and nucleic acids. The contact volume accounts for this effect by reweighting the point-cloud. By choosing different experimental weights for the free and contact component the AV dye model is refined, making *in silico* FRET predictions more reliable.\n\n## Installation\nFollow the instructions for your platform [here](https://rna-fretools.github.io/fretraj/getting_started/installation)\n\n## References\nIf you use **FRETraj** in your work please refer to the following paper:\n\n- F.D. Steffen, R.K.O. Sigel, R. Börner, *Phys. Chem. Chem. Phys.* **2016**, *18*, 29045-29055. [![](https://img.shields.io/badge/DOI-10.1039/C6CP04277E-blue.svg)](https://doi.org/10.1039/C6CP04277E)\n\n### Additional readings\n- S. Kalinin, T. Peulen, C.A.M. Seidel et al. *Nat. Methods*, **2012**, *9*, 1218-1225.\n- T. Eilert, M. Beckers, F. Drechsler, J. Michaelis, *Comput. Phys. Commun.*, **2017**, *219*, 377–389.\n- M. Dimura, T. Peulen, C.A.M. Seidel et al. *Curr. Opin. Struct. Biol.* **2016**, *40*, 163-185.\n- M. Dimura, T. Peulen, C.A.M Seidel et al. *Nat. Commun.* **2020**, *11*, 5394.\n\n---\n\n<sup><a name="pymol">1</a></sup> PyMOL is a trademark of Schrödinger, LLC.\n',
    'author': 'Fabio Steffen',
    'author_email': 'fabio.steffen@chem.uzh.ch',
    'maintainer': 'Fabio Steffen',
    'maintainer_email': 'fabio.steffen@chem.uzh.ch',
    'url': 'https://rna-fretools.github.io/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.9',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
