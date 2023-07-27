from setuptools import setup, find_packages
VERSION = '0.0.4'
DESCRIPTION = 'PYPI and GitHub package uploader.'
LONG_DESCRIPTION = 'Manages all the commands to upload a package to PYPI and GitHub repo.'

setup(
    name='UploadHub',
    version=VERSION,
    author="Armando Chaparro",
    author_email="<pylejandria@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'twine',
        'ttkbootstrap'
    ],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    include_package_data=True,
    package_data={'': ['data/*.json']}
)