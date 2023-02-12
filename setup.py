from setuptools import find_packages, setup

install_requires = ["langchain==0.0.81", "gradio==3.17.1", "faiss-cpu==1.7.2", "openai==0.26.5", "tiktoken==0.2.0"]

setup(
    name="hpqa",
    version="0.0.1",
    packages=find_packages("."),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=install_requires,
)
