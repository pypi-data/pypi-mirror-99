from setuptools import find_packages, setup
import pathlib

HERE = pathlib.Path(__file__).parent


# Where the magic happens:
setup(
    name='covidcaput',
    version='1.1.1',
    description="Covid Caput!",
    author='Grupa Żywiec Data Science team',
    author_email='data.science@grupazywiec.pl',
    python_requires='>=3.6.0',
    packages=['covidcaput'],
    extras_require={},
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)