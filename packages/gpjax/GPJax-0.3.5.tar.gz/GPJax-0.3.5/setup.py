from setuptools import setup, find_packages


def parse_requirements_file(filename):
    with open(filename, encoding="utf-8") as fid:
        requires = [l.strip() for l in fid.readlines() if l]
    return requires


# Optional Packages
EXTRAS = {
    "dev": [
        "black",
        "isort",
        "pylint",
        "flake8",
    ],
    "tests": [
        "pytest",
    ],
    "docs": [
        "furo==2020.12.30b24",
        "nbsphinx==0.8.1",
        "nb-black==1.0.7",
        "matplotlib==3.3.3",
        "sphinx-copybutton==0.3.5",
    ],
}

setup(
    name="GPJax",
    version="0.3.5",
    author="Thomas Pinder",
    author_email="t.pinder2@lancaster.ac.uk",
    packages=find_packages(".", exclude=["tests"]),
    license="LICENSE",
    description="Didactic Gaussian processes in Jax and ObJax.",
    long_description="GPJax aims to provide a low-level interface to Gaussian process models. Code is written entirely in Jax and Objax to enhance readability, and structured so as to allow researchers to easily extend the code to suit their own needs. When defining GP prior in GPJax, the user need only specify a mean and kernel function. A GP posterior can then be realised by computing the product of our prior with a likelihood function. The idea behind this is that the code should be as close as possible to the maths that we would write on paper when working with GP models.",
    install_requires=parse_requirements_file("requirements.txt"),
    extras_require=EXTRAS,
    keywords=["gaussian-processes jax machine-learning bayesian"],
)
