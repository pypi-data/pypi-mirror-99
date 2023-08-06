import setuptools
import re


VERSIONFILE="powerprotect/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="powerprotect",  # Replace with your own username
    version=verstr,
    author="Brad Soper",
    author_email="bradley.soper@dell.com",
    description="PowerProtect Python Class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EMC-Underground/powerprotect",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.24.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
