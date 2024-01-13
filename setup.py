from setuptools import find_packages, setup

install_requires = [
    "langchain==0.1.0",
    "gradio==4.14.0",
    "faiss-cpu==1.7.4",
    "openai==1.7.2",
    "tiktoken==0.5.2",
]

setup(
    name="hpqa",
    version="0.0.2",
    packages=find_packages("."),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=install_requires,
)
