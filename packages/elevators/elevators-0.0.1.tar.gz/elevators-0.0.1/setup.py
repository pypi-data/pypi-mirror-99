import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="elevators",
    version="0.0.1",
    author="Alexis Baird",
    author_email="alexis.elevator.developer@gmail.com",
    description="Software for operating elevators and running simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abaird1992/elevators",
    project_urls={
        "Bug Tracker": "https://github.com/abaird1992/elevators/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"elevators": "elevators"},
    packages=setuptools.find_packages(where="elevators"),
    python_requires=">=3.7",
)
