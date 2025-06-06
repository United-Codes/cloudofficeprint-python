import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudofficeprint",
    version="21.2.0",
    author="United Codes",
    author_email="info@united-codes.com",
    description="Python interface for Cloud Office Print",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/United-Codes/cloudofficeprint-python",
    packages=setuptools.find_packages(),
    license="GNU",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['requests','pandas'],
)
