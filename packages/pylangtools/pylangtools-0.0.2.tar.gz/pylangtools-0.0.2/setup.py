import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
    name="pylangtools", # Replace with your own package name
    version="0.0.2",
    author="Rosefun",
    author_email="rosefun@foxmail.com",
    description="繁体简体转换",
    long_description=long_description,
    #long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
)
