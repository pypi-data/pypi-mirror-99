import setuptools
import pathlib


setuptools.setup(
    name='crafter',
    version='0.12.0',
    description='Open world survival game for reinforcement learning.',
    url='http://github.com/danijar/crafter',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['crafter'],
    package_data={'crafter': ['assets/*']},
    entry_points={'console_scripts': ['crafter=crafter.run_gui:main']},
    install_requires=['numpy', 'imageio', 'gym', 'pillow', 'opensimplex'],
    extras_require={'gui': ['pygame']},
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
