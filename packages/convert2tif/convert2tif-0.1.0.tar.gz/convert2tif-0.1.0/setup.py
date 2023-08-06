import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

REQUIRED = [
    'Pillow'
]

setuptools.setup(
    name="convert2tif",
    version="0.1.0",
    author="Dakota Porter",
    author_email="dakotap3045@gmail.com",
    description="Small package that converts image(s) to .tif file format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dakotagporter/convert2tif",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIRED,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
