"""
Packaging.
"""

# 3rd party imports
from setuptools import setup


setup(
    name='sim21',
    version='0.1.0',
    description='Casino Blackjack Simulation',
    author='Conrad Mukai',
    author_email='conrad@mukai-home.net',
    packages=['sim21', 'sim21.strategies'],
    install_requires=[
        'jsonschema',
        'tabulate',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'sim21=sim21:main'
        ]
    }
)
