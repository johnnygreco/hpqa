from setuptools import find_packages, setup

install_requires = [
    "langchain==0.1.0",
    "langchain-openai==0.0.2.post1",
    "langchain-community==0.0.12",
    "langchain-core==0.1.10",
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
