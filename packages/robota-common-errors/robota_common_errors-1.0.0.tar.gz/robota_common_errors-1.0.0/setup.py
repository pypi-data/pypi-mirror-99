from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='robota_common_errors',
    version='1.0.0',
    description='Identification of common errors in software engineering.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='University of Manchester',
    url='https://gitlab.cs.man.ac.uk/institute-of-coding/robota-core',
    packages=find_packages(),
    install_requires=['robota-core>=2.0.0',
                      'tqdm',
                      'jsonpickle',
                      'jinja2',
                      'pandas',
                      'python-dateutil',
                      'plotly']
)
