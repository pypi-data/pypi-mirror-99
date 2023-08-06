import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybarracuda",
    version="0.0.5",
    author="Burhan Cabiroglu",
    author_email="burhancabiroglu97@gmail.com",
    description="high performance deep neural network genetic algorithm library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BurhanCabiroglu/Barracuda",
    project_urls={
        "Bug Tracker": "https://github.com/BurhanCabiroglu/Barracuda",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.5",
    install_requires=["numpy"]
)