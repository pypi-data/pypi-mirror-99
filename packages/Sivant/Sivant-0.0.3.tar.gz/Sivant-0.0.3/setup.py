from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="Sivant",
    version="0.0.3",
    description="A Python package",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/sivant1361/sivant_hello",
    author="Sivant M",
    author_email="sivant1313@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["SivantClass"],
    include_package_data=True,
)