import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="haibao",
    version="1.2.1",
    author="seal",
    author_email="seal.xu@qq.com",
    description="seal tools(add some other coins)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'ws4py',
    ],
    python_requires='>=2.7',
)
