import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iamend_ci", 
    version="0.0.3",
    author = "carabedo",
    author_email = "fernandocarabedo@cnea.gov.ar",
    description = "Libreria para la estimacion de la permeabilidad relativa efectiva.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carabedo/iamend_ci",
    project_urls={
        "Bug Tracker": "https://github.com/carabedo/iamend_ci/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.5",
)