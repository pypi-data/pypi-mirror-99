from setuptools import setup, find_packages

setup(
    name = 'FileAnalysis',
 
    version = "0.0.1",
    packages = find_packages(include=["FileAnalysis"]),
    install_requires = ["matplotlib"],

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
 
    description = "This package analyze emergence of characters in file (to decrypt with statistics).",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/FileAnalysis/',
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Topic :: Security",
    ],
 
    entry_points = {
        'console_scripts': [
            'FileAnalysis = FileAnalysis:analyze'
        ],
    },
    python_requires='>=3.6',
)