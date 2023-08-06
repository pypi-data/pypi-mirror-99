import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testing_tool_theg",
    version="0.0.1",
    author="yxyfer",
    author_email="riviermathieu@gmail.com",
    description="A simple testing tool for python Epita THEG class.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yxyfer/simple_testing_tool_python",
    project_urls={
        "Bug Tracker": "https://github.com/yxyfer/simple_testing_tool_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
