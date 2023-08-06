from setuptools import setup, find_packages

desc = "This package contains codes/functions that are useful in school level python programming"

with open("README.md", "r") as rd:
    longDesc = rd.read()

setup(name = "CodeDrive",
    version = "1.2",
    author = "Stark-Corp (Himangshu De)",
    author_email = "dehimangshu2020@gmail.com",
    url = "https://github.com/Stark-Corp/CodeDrive",
    description = desc,
    long_description = longDesc,
    long_description_content_type = "text/markdown",
    packages = find_packages(),
    install_requires = [],
    keywords = ['python', 'school level programs'],
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires = ">=3.6"
)
