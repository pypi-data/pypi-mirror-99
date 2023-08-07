from setuptools import setup

#读取readme
with open("README.md", "r", encoding="utf-8") as fh: long_description = fh.read()

#生成.whl文件
setup(
    name = "linpg",
    version = "3.0.1",
    author = "Tigeia-Workshop",
    author_email = "yudong9912@gmail.com",
    description = "A game engine based on pygame, which aims to make game development easier.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Tigeia-Workshop/linpg",
    license='LICENSE',
    project_urls={
        "Bug Tracker": "https://github.com/Tigeia-Workshop/linpg/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
    ],
    packages=['linpg'],
    include_package_data=True,
    python_requires = '>=3.6',
)
