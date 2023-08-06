import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="boydem",
    version="0.0.0",
    author="Omri Rozenzaft",
    author_email="omrirz@gmail.com",
    description="Simple Persistent Python Storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omrirz/boydem",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["dill"]
)
