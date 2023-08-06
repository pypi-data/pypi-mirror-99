import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fonsim",
    version="0.1a0",
    author="abaeyens",
    author_email="2arne.baeyens@gmail.com",
    description="Fluidic Object-Oriented Network Simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/abaeyens/fonsim",
    keywords='simulator, simulation, flow, fluids, fluidic, soft robot, soro, soft robotics, soft robots',
    package_dir={'': 'fonsim'},
    packages=setuptools.find_packages(where='fonsim'),
    package_data={'fonsim': ['data/*']},
    install_requires=['numpy', 'scipy', 'matplotlib'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
