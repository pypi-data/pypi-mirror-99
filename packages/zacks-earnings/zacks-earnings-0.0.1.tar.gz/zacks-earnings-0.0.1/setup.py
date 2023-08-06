import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zacks-earnings",
    version="0.0.1",
    author="Steve Kidd",
    author_email="",
    description="Get earnings releases from zacks.com/earnings/earnings-reports by date",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swkidd/zacks-earnings",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)