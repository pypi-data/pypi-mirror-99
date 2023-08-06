#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
QSDsan: Quantitative Sustainable Design for sanitation and resource recovery systems

This module is developed by:
    Yalin Li <zoe.yalin.li@gmail.com>

This module is under the University of Illinois/NCSA Open Source License. Please refer to
https://github.com/QSD-Group/QSDsan/blob/master/LICENSE.txt
for license details.
'''

from setuptools import setup

setup(
    name='qsdsan',
    packages=['qsdsan'],
    version='0.2.1',
    license='UIUC',
    author='Quantitative Sustainable Design Group',
    author_email='zoe.yalin.li@gmail.com (Yalin Li)',
    description='Quantitative Sustainable Design for sanitation and resource recovery systems',
    long_description=open('README.rst').read(),
    url="https://github.com/QSD-Group/QSDsan",
    install_requires=['biosteam==2.24.11', 'thermosteam==0.24.6', 'exposan', 'matplotlib>=3.3.2',
                      'scikit-learn', 'scipy', 'SALib>=1.4.0b0', 'seaborn', 'sympy'],
    package_data=
        {'qsdsan': [
                    'data/*',
                    'data/sanunit_data/*',
                    'sanunits/*',
                    'units_of_measure.txt',
                    'utils/*',
                    'systems/bwaise/*'
                    ]},
    platforms=['Windows', 'Mac', 'Linux'],
    classifiers=['License :: OSI Approved :: University of Illinois/NCSA Open Source License',
                 'Environment :: Console',
                 'Topic :: Education',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Chemistry',
                 'Topic :: Scientific/Engineering :: Mathematics',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'Intended Audience :: Manufacturing',
                 'Intended Audience :: Science/Research',
                 'Natural Language :: English',
                 'Operating System :: MacOS',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'Operating System :: POSIX :: BSD',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: Unix',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 ],
    keywords=['quantitative sustainable design', 'sanitation', 'resource recovery', 'techno-economic analysis', 'life cycle assessment'],
)