import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apexofficeprint",
    version="0.0.1",
    author="United Codes",
    author_email="info@united-codes.com",
    description="python interface for apexofficeprint",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/United-Codes/apexofficeprint-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "LICENSE :: OSI APPROVED :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['requests']
)
