"""
Configuration de l'installation du package.
"""
from setuptools import setup, find_packages

setup(
    name='project-parser',
    version='0.1.0',
    description='Outil de parsing multi-format (CSV, JSON, XML)',
    author='Nicolas GOUY, Josué ADAMI, Alexis REDAUD',
    author_email='',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        # Pas de dépendances externes (utilise stdlib)
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'flake8>=6.1.0',
            'black>=23.7.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'project-parser=project_parser.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
