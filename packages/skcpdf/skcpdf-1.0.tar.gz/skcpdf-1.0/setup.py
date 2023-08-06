import setuptools
from pathlib import Path
setuptools.setup(
    name="skcpdf",
    version=1.0,
    long_description=Path("README.MD").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"]),

)

