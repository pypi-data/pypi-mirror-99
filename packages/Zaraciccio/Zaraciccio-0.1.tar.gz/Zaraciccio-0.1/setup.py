try:
    import setuptools
except ModuleNotFoundError:
    raise RuntimeError("Must install setuptools before installing Zaraciccio")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    author="Zaraciccio De Zaracicci",
    author_email="zaradevelopment@outlook.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    description="Zaraciccio's Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "setuptools>=42",
        "wheel"
    ],
    keywords="Zaraciccio",
    name="Zaraciccio",
    package_dir={
        "": "src"
    },
    packages=[
        "Zaraciccio"
    ],
    version="0.1"
)
