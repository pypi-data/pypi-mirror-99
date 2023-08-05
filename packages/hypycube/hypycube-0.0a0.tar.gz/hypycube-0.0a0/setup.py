"""HyPyCube framework"""


import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='hypycube',
    version='0.0a0',
    author='Jakub Walczak, Mirko Stojiljkovic, Marco Mancini',
    author_email='jakub.walczak@cmcc.it, mirko.stojiljkovic@cmcc.it, marco.mancini@cmcc.it',
    description='HyPyCube framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hypycube/hypycube',
    packages=setuptools.find_packages(),
    install_requires=[
        'attrs==20.2.0',
        'bottleneck==1.3.2',
        'cftime==1.2.1',
        'click==7.1.2',
        'distributed==2.20.0',
        'dask-jobqueue==0.7.1',
        'dask==2.20.0',
        'intake==0.5.5',
        'numpy==1.18.1',
        'pandas==1.0.3',
        'xarray==0.16.0',
        'packaging==20.4',
        'pyparsing==3.0.0a2',
        'pytest-cov==2.10.0',
        'pytest==5.4.2',
        'bokeh==2.0.1',
        'sortedcontainers==2.2.2',
        'urllib3==1.25.11',
        'zarr==2.5.0',
        's3fs<0.4',
        'netCDF4==1.5.6'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Hydrology'
    ],
    python_requires='>=3.7',
    license='Apache License, Version 2.0'
)
