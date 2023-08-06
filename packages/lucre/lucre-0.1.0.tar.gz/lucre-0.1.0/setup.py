from setuptools import setup, find_packages


setup(
    name="lucre",
    version="0.1.0",
    author="Steve McCartney",
    author_email="python+lucre@reconvergent.com",
    url="https://github.com/stevemccartney/lucre",
    packages=find_packages(),
    license="Apache-2.0",
    description="Plain Text Accounting",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Typing :: Typed",
    ],
)