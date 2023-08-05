from setuptools import setup
from setuptools import find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name="cached_task",
    version="2021.3.7",
    description="cached_task",
    long_description=readme,
    author="Bogdan Mustiata",
    author_email="bogdan.mustiata@gmail.com",
    license="BSD",
    install_requires=[],
    packages=packages,
    package_data={
        "": ["*.txt", "*.rst"],
        "cached_task": ["py.typed"],
    },
)
