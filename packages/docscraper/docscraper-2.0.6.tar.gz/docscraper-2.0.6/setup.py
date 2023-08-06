from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='docscraper',
    version='2.0.6',
    description='A web crawler to scrape documents from websites',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://docscraper.readthedocs.io/en/latest/',
    author='Patrick Ryan',
    author_email='pjryan126@gmail.com',
    license='MIT',
    install_requires=[
        'openpyxl',
        'numpy>=1.16.5',
        'pandas',
        'requests',
        'scrapy',
        'scrapy-wayback-machine'
    ],
    packages=find_packages(),
    test_suite='tests',
    zip_safe=False,
)