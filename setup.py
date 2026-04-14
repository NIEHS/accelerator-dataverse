from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    install_requires = [line.strip() for line in f if line.strip()]

setup(
    name="accelerator_dataverse",
    version="0.1.0",
    description="accelerator components for dataverse",
    author="Mike Conway",
    author_email="mike.conway@nih.gov",
    url="https://github.com/NIEHS/accelerator-dataverse",
    packages=find_packages(),
    install_requires=[open("requirements.txt").read()],
    license="BSD 3-Clause",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    package_data={"accelerator_dataverse": ["dataverse_utils/templates/*.*"]},
    include_package_data=True,
)
