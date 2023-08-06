from setuptools import setup

setup(
    name="harmoniums",
    version="0.1.0",
    download_url="https://gitlab.com/hylkedonker/harmonium-models/-/archive/0.1.0/harmonium-models-0.1.0.tar.gz",
    description=(
        "Harmoniums -- a.k.a. restricted Boltzmann machines -- with binary "
        "latent states for survival analysis."
    ),
    url="https://gitlab.com/hylkedonker/harmonium-models",
    author="Hylke C. Donker",
    author_email="h.c.donker@umcg.nl",
    license="Apache License 2.0",
    packages=["harmoniums"],
    package_data={"harmoniums": ["datasets/*.csv"]},
    keywords=[
        "survival analysis",
        "machine learning",
        "harmonium",
        "restricted Boltzmann machine",
    ],
    install_requires=[
        "lifelines>=0.25",
        "pandas>=1.1",
        "numpy>=1.19",
        "scikit-learn>=0.23",
        "numba>=0.52",
        "scikit-survival",
    ],
    classifiers=["Programming Language :: Python :: 3.8"],
    zip_safe=False,
)
