import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='TextGeneratorRandomMaximun',
    version='0.0.1',
    author='Antonio Abril',
    author_email='mi_gran_email@gmail.com',
    description='Mi segundo package para PyPi. Este genera palabras aleatorias de un texto',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aabrilfl/prueba_package_pypi',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers"
    ],
    python_requires='>=3.6',

)
