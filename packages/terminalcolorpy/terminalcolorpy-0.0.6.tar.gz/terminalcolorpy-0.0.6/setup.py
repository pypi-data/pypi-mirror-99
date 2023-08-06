import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="terminalcolorpy",
    version="0.0.6",
    author="ammarsys",
    author_email="amarftw1@gmail.com",
    description="This is a simple package to print colored messages using ASCI to the terminal built with python 3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ammar-sys/terminalcolorpy",
    project_urls={
        "Bug Tracker": "https://github.com/ammar-sys/terminalcolorpy/issues",
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