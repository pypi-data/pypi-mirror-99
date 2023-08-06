import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="automation-api-deffets",
    version="0.0.12",
    license='apache-2.0',
    author="Sylvain Deffet",
    description="Python API for the automation server database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/deffets/automation/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

