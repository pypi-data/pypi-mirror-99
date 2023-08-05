import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hola_mundo_mercadona",
    version="0.0.1",
    author="Martín San José",
    author_email="martin@imaginagroup.com",
    maintainer= "Martín San José",
    description="Mi primer Package subido a Pypi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/masajo/mercadona-pypi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers"
    ],
    python_requires='>=3.6'
)
