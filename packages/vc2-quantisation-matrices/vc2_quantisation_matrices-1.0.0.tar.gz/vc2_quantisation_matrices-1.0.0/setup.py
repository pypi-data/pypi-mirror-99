import os

from setuptools import setup, find_packages

version_file = os.path.join(
    os.path.dirname(__file__),
    "vc2_quantisation_matrices",
    "version.py",
)
with open(version_file, "r") as f:
    exec(f.read())

readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_file, "r") as f:
    long_description = f.read()

setup(
    name="vc2_quantisation_matrices",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/bbc/vc2_quantisation_matrices",
    author="BBC R&D",
    description="Routines for computing quantisation matrices for the SMPTE ST 2042-2 VC-2 professional video codec.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="GPL-3.0-only",
    classifiers=[
        "Development Status :: 5 - Production/Stable",

        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Telecommunications Industry",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="smpte-RP-2042-3 vc2 dirac dirac-pro quantisation-matrix bit-width",
    install_requires=["vc2_data_tables >=0.1,<2.0", "sympy"],
    entry_points = {
        'console_scripts': [
            'vc2-make-quantisation-matrix=vc2_quantisation_matrices.cli_tool:main',
        ],
    },
)
