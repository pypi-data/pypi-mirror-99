from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="emw_serializer",
    version="0.0.1",
    description="Simple serializer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matthew-emw/emw-serializer",
    author="Eight Minutes West Limited",
    author_email="matthew@eightminuteswest.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": []
    },
)
