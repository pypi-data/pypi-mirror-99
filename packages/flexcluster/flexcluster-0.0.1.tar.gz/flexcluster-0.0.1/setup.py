import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flexcluster",
    version="0.0.1",
    author="Humberto Marchezi",
    author_email="hcmarchezi@gmail.com",
    description="flexible clustering algorithm that allows user-define dissimilarity an centroid calculation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/flexcluster",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/voctree/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "flexcluster"},
    packages=setuptools.find_packages(where="flexcluster"),
    python_requires=">=3.6",
)