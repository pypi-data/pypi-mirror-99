import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="steam_nb_api",
    version="0.3.18", #Original: 0.3.18, test: 0.3.155
    author="TE-MPE",
    author_email="steam@cern.ch",
    description="A package with an API for STEAM.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/steam/steam-notebook-api",
    package_data = {'steam_nb_api': ["*.yaml"]},
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
