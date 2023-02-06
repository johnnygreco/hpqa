from setuptools import find_packages, setup

setup(
    name="hpqa",
    version="0.0.1",
    packages=find_packages("."),
    include_package_data=True,
    python_requires=">=3.8",
)