from setuptools import setup, find_packages
with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["openpyxl>=3"]

setup(
    name="modelpyxl",
    version="0.0.6",
    author="Petr Borisenko",
    author_email="borisenko.petr.a@gmail.com",
    description="Python package for creation model of excel documents based on a workbook template.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pborisenko/modelpyxl/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
