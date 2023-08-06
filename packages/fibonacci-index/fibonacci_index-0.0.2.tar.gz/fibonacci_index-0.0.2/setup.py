import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fibonacci_index",
    version="0.0.2",
    author="Cassiana Silveira",
    author_email="cassianasilveira64@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ifcassianasl/fibonacci-index",
    project_urls={
        "Bug Tracker": "https://github.com/ifcassianasl/fibonacci-index/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)