from setuptools import setup, find_packages

d_version = {}
with open("./pytuna/version.py") as fp:
    exec(fp.read(), d_version)
version = d_version['VERSION']

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pytuna',
    author='Visym Labs',
    author_email='info@visym.com',
    version=version,
    packages=find_packages(),
    description='Visym Python Tools for Visual Network Tuning',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/visym/pytuna',
    download_url='https://github.com/visym/pytuna/archive/%s.tar.gz' % version,
    install_requires=["vipy", "pycollector"],
    keywords=['computer vision machine learning ML CV privacy video image'],    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]
)
