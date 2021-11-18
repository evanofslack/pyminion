import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyminion",
    version="0.1.5",
    author="Evan Slack",
    author_email="evan.slack@outlook.com",
    description="Dominion but make it python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evanofslack/pyminion",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(
        exclude=(
            "tests",
            "tests.*",
            "examples",
            "examples.*",
        )
    ),
    python_requires=">=3.8",
)
