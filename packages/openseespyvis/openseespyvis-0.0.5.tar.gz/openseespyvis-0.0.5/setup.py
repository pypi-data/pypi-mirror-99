
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openseespyvis", # Replace with your own username
    version="0.0.5",
    author="anurag upadhyay",
    author_email="iitg.anurag@gmail.com",
    description="A development package of openseespy visualization commands.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/u-anurag/openseespyvis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)