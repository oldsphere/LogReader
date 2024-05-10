from setuptools import setup, find_packages

setup(
    name="LogReader",
    version="0.1",
    author="Carlos Rubio",
    author_email="crubio@nordsim.es",
    description="Lector de logs para OpenFOAM, generalizable a otros, basado en estructura de pyFoam",
    url="https://github.com/oldsphere/LogReader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    scripts=[],
)
