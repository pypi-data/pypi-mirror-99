import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="createActiveTask2List",
    version="1.1",
    author="Antas",
    author_email="",
    description="Create asyncio.Task instance to a list, until it is done.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monk-after-90s/createActiveTask2List.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
