import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Pymars_india",
    version="1.0.3",
    description="Mars orbital mission",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Priteshraj10/Pymars_india",
    author="Pritesh Raj",
    author_email="priteshraj41@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["Pymars_india"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "Pymars_india=Pymars_india.__main__:main",
        ]
    },
)