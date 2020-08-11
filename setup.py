import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apexofficeprint",
    version="0.0.1", # TODO
    author="United Codes",
    author_email="info@united-codes.com",
    description="python interface for apexofficeprint",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/United-Codes/apexofficeprint-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        #"License :: OSI Approved :: MIT License", # TODO
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
