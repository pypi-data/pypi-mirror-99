from setuptools import setup, find_packages


with open("README.md", "r") as file:
    readme = file.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()



setup(
    name="pencil_pusher",
    version="0.9.2",
    description="A python package that compiles source documentation and publishes it to the repo wiki",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Stephen Davis",
    author_email="stephenedavis17@gmail.com",
    packages=find_packages(),
    url="https://github.com/stephend017/pencil-pusher",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=required
)
