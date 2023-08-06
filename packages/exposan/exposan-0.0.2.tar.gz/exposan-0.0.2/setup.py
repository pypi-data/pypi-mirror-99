#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
EXPOsan: Exposition of sanitation and resource recovery systems

This module is developed by:
    Yalin Li <zoe.yalin.li@gmail.com>

This module is under the University of Illinois/NCSA Open Source License. Please refer to
https://github.com/QSD-Group/EXPOsan/blob/master/LICENSE.txt
for license details.
'''

from setuptools import setup

setup(
    name='exposan',
    packages=['exposan'],
    version='0.0.2',
    license='UIUC',
    author='Quantitative Sustainable Design Group',
    author_email='zoe.yalin.li@gmail.com (Yalin Li)',
    description='Exposition of sanitation and resource recovery systems',
    long_description=open('README.rst').read(),
    url="https://github.com/QSD-Group/EXPOsan",
    install_requires=['qsdsan',],
    package_data=
        {'exposan': [
                    'bwaise/*',
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