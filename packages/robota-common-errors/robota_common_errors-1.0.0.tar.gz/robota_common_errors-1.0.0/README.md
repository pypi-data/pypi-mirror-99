# RoboTA-common-errors
## Automated software engineering assessment

RoboTA (Robot Teaching Assistant) is a group of Python packages that provide a framework for
the assessment of software engineering practices. The focus of RoboTA is the assessment of
student software engineering coursework, though it has a wider scope in the assessment of
general good practice in software engineering.

The robota-core package collects information about a project from a number of sources,
git repositories, issue trackers, ci-servers. It is designed to be provider agnostic, for example
repository data can come from GitLab or GitHub.

The robota-common-errors package then uses this information to assess the project against a number
of common software engineering errors or bad practices. Examples include committing non-project files
to a git repository or merging a git branch into the remote tracking branch instead of the local one.
The included errors are designed to be general and project agnostic but it would be easy to add new methods
to enforce project or group specific standards such as a standard format for git commit messages or ensuring
that issues are always assigned to an individual as soon as they are opened.

RoboTA was developed in the [Computer Science](https://www.cs.manchester.ac.uk/) department
at the [University of Manchester](https://www.manchester.ac.uk/).
From 2018 to March 2021, development of RoboTA was funded by the
[Institute of Coding](https://ioc.cs.manchester.ac.uk/).

## Installation


To install as a Python module, type

``python -m pip install .``

from the root directory. 
For developers, you should install in linked .egg mode using

``python -m pip install robota-core -e``

If you are using a Python virtual environment, you should activate this first before using the above commands.

## RoboTA Config

RoboTA requires access to a number of data sources to collect data to operate on. 
Details of these data sources and information required to connect to them is provided in the robota config yaml file.
Documentation on the config file can be found in the `data_sources` section of the documentation.