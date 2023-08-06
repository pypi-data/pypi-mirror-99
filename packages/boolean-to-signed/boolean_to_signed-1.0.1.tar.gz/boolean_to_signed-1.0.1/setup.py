from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='boolean_to_signed',
    version='1.0.1',
    description='Returns -1 if input is false, or 1 if input is true.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Najim Islam',
    packages=find_packages(),
    keywords=['boolean', 'signed', 'convert', 'sign', 'conversion'],
)
