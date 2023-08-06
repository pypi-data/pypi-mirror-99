import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noodle-logging",
    version="0.3",
    author="Ali Askar",
    author_email="aliaskar1024@gmail.com",
    description="Logging in JSON the easy way!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/beingaskar/noodle_logging",
    packages=setuptools.find_packages(),
    install_requires=[
        'six==1.12.0',
        'structlog==21.1.0',
        'python-json-logger==2.0.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
