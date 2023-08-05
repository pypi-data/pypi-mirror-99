import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "calcular_factorial_paralelo",
    version="0.0.2",
    author="msolazhe",
    description="Libreria que calcula los numeros factoriales en paralelo",
    long_description=long_description,
    author_email="msolazhe@mercadona.es",
    maintainer="Marcos",
    long_description_content_type="text/markdown",
    url="https://github.com/MSH-Marcos/Mr-Fix",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers"
    ],
    install_requires=[
    ],
    python_requires='>=3.6'
)