from setuptools import setup, find_packages

setup(
    name='aganalyze',
    version='1.0',
    long_description=__doc__,
    packages=['analyze'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)
