import setuptools

with open("README_stripped.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydraw",
    version="1.3.4",
    author="Noah Coetsee",
    author_email="noah@noahcoetsee.me",
    description="A package designed to make graphics with Python simple and easy!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pydraw/pydraw",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pillow'
    ],
    python_requires='>=3.6',
)
