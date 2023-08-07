import pathlib

import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

# This call to setup() does all the work
setuptools.setup(
    name='decorit',
    version='0.1.0',
    description='Handy ready-to-use decorators.',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords='decorators',
    author='braniii',
    url='https://gitlab.com/braniii/decorit',
    license='BSD 3-Clause License',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 3 - Alpha',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    install_requires=['beartype'],
)
