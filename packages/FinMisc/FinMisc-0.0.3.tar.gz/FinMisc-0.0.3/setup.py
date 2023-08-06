import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "FinMisc", # okg name
    version = "0.0.3",
    author = "Xuanhua Yin",
    author_email = "peteryin.sju@hotmail.com",
    description = "Miscellaneous functions for financial analysis, trading and visualization",
    long_description = long_description, # load README.md on python package index page
    long_description_content_type = "text/markdown",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry"
    ],
    keywords = "Finance, Trading, Visualization",
    # packages = setuptools.find_packages(), pandas, numpy, statistics, math
    # python_requires = ">=3.6",
    install_requires=[
          'pandas',
          'numpy',
          'statistics',
          'math',
          'matplotlib',
          'tushare'    
    ],
)