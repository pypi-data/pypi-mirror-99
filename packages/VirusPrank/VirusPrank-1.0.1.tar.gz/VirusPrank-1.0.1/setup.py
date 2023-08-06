
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="VirusPrank",
    version="1.0.1",
    description="Harmless virus prank",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Dev Shah",
    author_email="dgm82832@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["virus"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "VirusPrank=virus.__main__:main",
        ]
    },
)
