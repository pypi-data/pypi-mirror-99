from setuptools import setup, find_packages

setup(
    name="vivek2dropoffnan",
    version="0.0.1",
    author="Vivek Suresh Raj",
    author_email="vivek.sureshraj@ucalgary.ca",
    description="A simple package to perform basic data cleaning in EDA",
    long_description= open('README.txt').read()+ '\n\n' + open('CHANGELOG.txt').read(),
    packages=find_packages(),
    keywords = 'data cleaning',
    License= 'MIT',
    classifiers=[
    	"Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Intended Audience :: Education"],
    install_requires = ['']
    )