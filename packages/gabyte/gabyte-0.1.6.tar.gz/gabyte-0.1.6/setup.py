import setuptools


setuptools.setup(
    name="gabyte",
    version="0.1.6",
    author="Francis B. Lavoie",
    author_email="francis.b.lavoie@usherbrooke.ca",
    description="Genetic algorithms with bytes",
    long_description="Genetic algorithms with bytes",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["tqdm"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ),
)