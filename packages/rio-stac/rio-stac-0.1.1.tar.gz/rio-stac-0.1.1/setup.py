"""Setup rio-stac."""

from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

inst_reqs = [
    "rasterio",
    "pystac>=0.5,<0.6",
]

extra_reqs = {
    "dev": ["pytest", "pytest-cov", "pre-commit", "requests"],
    "test": ["pytest", "pytest-cov", "requests"],
    "docs": ["mkdocs", "mkdocs-material", "pygments", "pdocs"],
}


setup(
    name="rio-stac",
    version="0.1.1",
    description="Create STAC Items from raster datasets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="COG STAC rasterio",
    author=u"Vincent Sarago",
    author_email="vincent@developmentseed.org",
    url="https://github.com/developmentseed/rio-stac",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    package_data={"rio_stac": ["templates/*.json"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points="""
      [rasterio.rio_plugins]
      stac=rio_stac.scripts.cli:stac
      """,
)
