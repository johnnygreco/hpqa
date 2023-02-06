from setuptools import find_packages, setup

install_requires = ["farm-haystack[faiss]==1.13.1", "gradio==3.17.1", "torch==1.13.1", "transformers==4.25.1"]

setup(
    name="hpqa",
    version="0.0.1",
    packages=find_packages("."),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=install_requires,
)
