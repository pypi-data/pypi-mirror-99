# coding: utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seleniumqt",
    version="0.0.1",
    author="poseidon",
    author_email="seleniumqt@gmail.com",
    description="test@qtp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/lll/seleniumqt',
    project_urls={
        "seleniumqt": "http://github.com/lll/seleniumqt",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)