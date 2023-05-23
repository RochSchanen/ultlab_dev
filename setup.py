# file: setup.py
# content: setup file for ultlab package
# created: 2023 05 18
# author: roch schanen

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "ultlab",
    version = "0.0.0",
    author = "Roch Schanen",
    author_email = "r.schanen@lancaster.ac.uk",
    description = "micro-package",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/RochSchanen/ultlab_dev",
    packages = ['ultlab'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'numpy', 
        'matplotlib', 
        # 'pillow',
        ],
    # install_requires = [],
    python_requires = '>=3.0'
)
