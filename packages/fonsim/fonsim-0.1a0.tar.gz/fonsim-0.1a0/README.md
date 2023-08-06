# FONSIM
#### _Fluidic Object-oriented Network SIMulator_

An object-oriented Python 3 library designed for simulating pneumatic and hydraulic systems in soft robots.

This project is available under the GNU Affero General Public License v3.0 (**agpl-3.0**) license.

**Installation**:
The stable release version can be installed using `pip`.
See the [PyPi page]() for more information. 
 
### Features
* Powerful and fast simulation backend
  - Newton-Raphson method for handling nonlinear equations
  - Backward Euler time discretization for stability
* Implicit component equations
* Fluid class
  - custom fluids, e.g. non-Newtonian
  - fallback functionality
* Toolset focused on soft robotics (SoRo) research
  - read and process pv-curves
* Standard library of fluidic components
  - Tubes, nodes, pressure sources, volume sources, containers, one-way valves, ...
* Flow calculations
  - Compressible flow approximations
  - Laminar and turbulent flow based on Reynold number
  - Major and minor losses (Darcy, Haaland, K-factor etc.)
*  Preconfigured custom plot methods
* Export data for further processing as JSON file
* Cross platform



### How to get started
The directory _examples_ contains a set of examples showcasing various features of the simulator.
We suggest to start with running the examples.
Furthermore you may want to consult the documentation on
[readthedocs.org]().
The same documentation is also available by the
[Python help function](https://www.programiz.com/python-programming/docstrings#help).
If something is not fully clear, please let us know.

### Dependencies
* matplotlib
* numpy
* scipy



## Project development, contribution

### Contributing
Are you interested in contributing to this project?
Please get in touch so we can coordinate the development!

### Branching
The FONS project branching is based on the
[Driessen or git-flow model](https://nvie.com/posts/a-successful-git-branching-model/).
Put simply,
the `master` branch is reserved for production-ready code.
All software in `master` should be stable and usable.
The `dev` branch contains the latest developed features,
yet as a result the software is not as stable.
The actual features (and improvements in general) are developed in the
feature branches, for example `feature-plotting`.

### To get this repo locally
1. Clone the repo (notice the `$` - this means to do it in a terminal/console).
The directory with the project will be located in the current working directory of the terminal.
    ```
    $ git clone git@gitlab.com:abaeyens/fons.git
    ```
1. Go in the created directory (note: one can use `TAB` for autocompletion)
    ```
    $ cd fons
    ```
1. Add the remote, so you can push and pull from the remote repo on gitlab.com
    ```
    $ git remote add upstream git@gitlab.com:abaeyens/fons.git
    ```

### Create a local install
A local install allows to try out the library locally.
This can be useful during development.
First, rename the project root directory to `fonsim` (default name after Git clone: `fons`).
Second, run in the project root directory:
```
$ python -m pip install -e .
```
This installs the FONS package such that it is accessible
like all other Python packages, e.g. using `import fonsim`.
The `-e` option denotes that it uses a symbolic link:
code changes in the project directory (including branch switching)
take effect at the first following `import`.
No re-installation is required.

Note: `python` should refer to Python 3.
You may have to write `python3` to avoid using Python 2. 

Note: there appear to be problems with this method on some Windows machines.

Note: if you want to install several versions of the same package on your system,
for example a stable version from PyPi
and a development version from a local install,
you may want to use a
[Python virtual environment](https://docs.python.org/3/tutorial/venv.html).

### Development tools
A git repository history visualizer tool like
[gitg](https://wiki.gnome.org/Apps/Gitg/)
can be helpful in developing this software.
It shows the relations between version branches visually,
lists all commits and allows to see the exact changes
were made in a particular commit.
In addition, it can show uncommited changes.

Gitlab provides similar tools as a web version like the
[GitLab graph](https://gitlab.com/abaeyens/fons/-/network/master).

### Style guide
https://google.github.io/styleguide/pyguide.html.


## Problems, questions, suggestions
If you have a question the FAQ section does not answer sufficiently,
or you think you have encountered a bug,
you can reach out by creating an issue on the
[GitLab Issues](https://gitlab.com/abaeyens/fons/-/issues) page



## FAQ
...
