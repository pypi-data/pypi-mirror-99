from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nickffs-example-pkg", # Replace with your own username
    version="0.0.5",
    author="bhavnicksm",
    author_email="bhavnicksm@gmail.com",
    description="A template to create other PyPi packages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bhavnicksm/pypi-packaging-template",
    project_urls={
        "Bug Tracker": "https://github.com/Bhavnicksm/pypi-packaging-template/issues",
    },
    keywords = [
        'template',
    ],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages= find_packages(where="src"),
    python_requires=">=3.6",
)