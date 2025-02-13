from setuptools import setup, find_packages

setup(
    name='fileops',
    version='0.1.0',
    description='File operations utilities',
    author='Foursquare Labs Inc.',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'test': [
            'pytest>=6.0.0',
            'pytest-cov>=2.10.0',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
