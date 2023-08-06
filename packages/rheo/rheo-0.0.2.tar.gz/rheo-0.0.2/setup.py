from pathlib import Path

from setuptools import setup
from rheo.version import __version__

setup(
    name='rheo',
    packages = ['rheo'],
    version=__version__,
    description='Rheo library',
    install_requires=Path('requirements.txt').read_text().split(),
    long_description=Path('README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    platforms=['Windows', 'POSIX', 'MacOS'],
    maintainer='Seven Bridges Genomics Inc.',
    maintainer_email='support@sbgenomics.com',
    url='https://github.com/sbg/rheo',
    license='Apache Software License 2.0',
    include_package_data=True,
    keywords=[
        'rheo', 'sevenbridges', 'automations', 'sbg', 'cgc',
        'cancer', 'genomics', 'cloud',
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
