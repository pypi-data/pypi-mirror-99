import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="l0n0lnet",
    version="2.4.1",
    author="l0n0l",
    author_email="1038352856@qq.com",
    description="一个简单的高性能c++网络库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/l00n00l/l0n0lnet",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    include_package_data = True,
    package_data = {
        "":["*.so"]
    },
    install_requires=[
        "cmake",
        "GitPython"
    ]
)
