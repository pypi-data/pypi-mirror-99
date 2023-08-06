import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Aofex_SDK",
    version="1.1.0",
    author="Antas",
    author_email="",
    description="Aofex SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monk-after-90s/Aofex_SDK.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
