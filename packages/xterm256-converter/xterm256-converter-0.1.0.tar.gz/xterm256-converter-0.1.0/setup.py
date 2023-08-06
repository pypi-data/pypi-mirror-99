from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="xterm256-converter",
    version="0.1.0",
    description="This util can convert hex color code to nearest xterm 256 color.",
    license="MIT",
    author="averak",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={
        'console_scripts': [
            'xterm256-converter=xterm256_converter.core:main',
        ]
    },
)
