import setuptools
import os
import sys

with open("package_README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    packages=setuptools.find_packages('quantuiti'),
    name="quantuiti",
    version="0.1.0",
    author="Dylan Muraco",
    author_email="dylanjmuraco@gmail.com",
    description="quantuiti library for quantitative finance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/quantuiti/python-quantuiti",
    entry_points ={ 
        'console_scripts': [ 
            'quantuiti = quantuiti.__main__:main'
        ] 
    },
    project_urls={
        "Bug Tracker": "https://github.com/quantuiti/python-quantuiti/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    python_requires=">=3.6",
)
