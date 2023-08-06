"""
Setup the mokapot package.
"""
import setuptools

with open("README.md", "r") as readme:
    LONG_DESC = readme.read()

DESC = "Semi-supervised learning for peptide detection by pretrained models"

CATAGORIES = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]

setuptools.setup(
    name="mokapot",
    author="William E. Fondrie",
    author_email="fondriew@gmail.com",
    description=DESC,
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    url="https://github.com/wfondrie/mokapot",
    packages=setuptools.find_packages(),
    license="Apache 2.0",
    entry_points={"console_scripts": ["mokapot = mokapot.mokapot:main"]},
    classifiers=CATAGORIES,
    install_requires=[
        "numpy>=1.18.1",
        "pandas>=1.0.3",
        "scikit-learn>=0.22.1",
        "numba>=0.48.0",
        "triqler>=0.3.0",
        "matplotlib>=3.1.3",
        "lxml>=4.6.2",
    ],
    extras_require={
        "docs": [
            "numpydoc>=1.0.0",
            "sphinx-argparse>=0.2.5",
            "sphinx-rtd-theme>=0.5.0",
            "nbsphinx>=0.7.1",
            "ipykernel>=5.3.0",
            "recommonmark>=0.5.0",
        ],
        "dev": ["pre-commit>=2.7.1", "black>=19.10b0"],
    },
)
