import os
import pathlib
from setuptools import find_packages, setup


def readme():
    with open(f'{pathlib.Path(__file__).parent}/README.md', 'r') as f:
        return f.read()


def version():
    file = os.path.join(os.path.dirname(__file__), 'eyedrop/.versioning.txt')
    try:
        with open(file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return 'dev.dev.dev'


setup(
    name="eyedrop",
    version=version(),
    summary='Gathers colour characteristics from images and videos',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/lumikapp/eyedrop/",
    author='Lumik',
    author_email="open_source@lumik.app",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=("doc", "test")),
    include_package_data=True,
    install_requires=[],
)
