"""
sumo: Heavy weight plotting tools.
"""

from setuptools import setup, find_packages
from sumo import __version__


with open("README.rst", "r") as file:
    long_description = file.read()

setup(
    name="sumo",
    version=__version__,
    description=(
        "Heavy weight plotting tools for ab initio " "solid-state calculations"
    ),
    url="https://github.com/smtg-ucl/sumo",
    author="Alex Ganose, Adam J. Jackson",
    author_email="d.scanlon@ucl.ac.uk",
    long_description=long_description,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    keywords="chemistry pymatgen dft vasp dos band",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "spglib",
        "numpy",
        "scipy",
        "h5py",
        "pymatgen>=2020.10.20",
        "phonopy>=2.1.3",
        "matplotlib",
        "seekpath",
        "castepxbin==0.1.0",
    ],
    extras_require={
        "docs": ["sphinx", "sphinx-argparse"],
        "tests": ["pytest"]
    },
    package_data={
        "sumo": [
            "symmetry/bradcrack.json",
            "plotting/orbital_colours.conf",
            "plotting/sumo_base.mplstyle",
            "plotting/sumo_bs.mplstyle",
            "plotting/sumo_dos.mplstyle",
            "plotting/sumo_optics.mplstyle",
            "plotting/sumo_phonon.mplstyle",
        ]
    },
    data_files=["examples/orbital_colours.conf", "LICENSE"],
    entry_points={
        "console_scripts": [
            "sumo-bandplot = sumo.cli.bandplot:main",
            "sumo-bandstats = sumo.cli.bandstats:main",
            "sumo-dosplot = sumo.cli.dosplot:main",
            "sumo-kgen = sumo.cli.kgen:main",
            "sumo-phonon-bandplot = sumo.cli.phonon_bandplot:main",
            "sumo-optplot = sumo.cli.optplot:main",
        ]
    },
)
