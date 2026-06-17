from setuptools import setup, find_packages

setup(
    name="nesy-mbst",
    version="0.1.0",
    description="Neuro-Symbolic Model-Based Statistical Testing Framework",
    author="Nathan G.",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
    ],
)
