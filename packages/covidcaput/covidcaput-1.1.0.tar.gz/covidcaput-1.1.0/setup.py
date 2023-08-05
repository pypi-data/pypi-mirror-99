from setuptools import find_packages, setup

# Where the magic happens:
setup(
    name='covidcaput',
    version='1.1.0',
    description="Covid Caput!",
    author='Grupa Żywiec Data Science team',
    author_email='data.science@grupazywiec.pl',
    python_requires='>=3.6.0',
    packages=find_packages(exclude=('tests',)),
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