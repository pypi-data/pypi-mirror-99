import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pipverify",
    version="0.0.3",
    scripts=['pipverify'],
    author="Philipp Mayr",
    author_email="me@philipp-mayr.de",
    description="A tool to verify GPG signatures of supporting packages on PIP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeberg.org/PhilippMayrTH/pipverify",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'python-gnupg', 'click'],
    license="ISC",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
