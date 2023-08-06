import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pklib",
    version="0.0.1",
    author="Parthiban Kannan",
    author_email="parthiban_kannan@outlook.com",
    description="Machine Learning Simplified Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires=">=3.6",
)
