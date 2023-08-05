import setuptools
import koolstof as ks

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()
setuptools.setup(
    name="koolstof",
    version=ks.__version__,
    author="Humphreys, Matthew P.",
    author_email="m.p.humphreys@icloud.com",
    description="Miscellaneous tools for marine carbonate chemistry and other such things",
    url="https://github.com/mvdh7/koolstof",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
