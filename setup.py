import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="material-palette-generator",
    version="0.0.1",
    author="Stefano Baldan",
    author_email="singintime@gmail.com",
    description="Web service that generates Material color palettes out of hex codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/singintime/material-palette-generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
