import setuptools  # this is the "magic" import
from numpy.distutils.core import setup, Extension

lib = Extension(name='randomfield.randomq512', sources=['randomfield/randomq512.f'])
lib2 = Extension(name='randomfield.rando2asc', sources=['randomfield/rando2asc.f'])

setup(
    name='generate_field',
    version='0.1.0',
    packages=['randomfield'],
    ext_modules=[lib, lib2],
    install_requires=["numpy", "f2py"],
    entry_points={
        'console_scripts': [
            'hello = spam.cli:main',
        ],
    }
)
