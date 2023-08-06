from setuptools import setup, find_packages

desc = "This package contains codes/functions that are useful in school level python programming"

longDesc = "You can use this module for executing the school level programming tasks like Palindrome tests, Armstrong number tests, etc. All the things are included in this python package and will be updated more in future."

setup(name = "CodeDrive",
    version = "1.1",
    author = "Stark-Corp (Himangshu De)",
    author_email = "dehimangshu2020@gmail.com",
    url = "https://github.com/Stark-Corp/CodeDrive",
    description = desc,
    long_description = longDesc,
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
