from setuptools import setup, find_packages
VERSION = "VERSION"
DESCRIPTION = "DESCRIPTION"
LONG_DESCRIPTION = "DESCRIPTION"

setup(
    name="NAME",
    version=VERSION,
    author="AUTHOR",
    author_email="MAIL",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)