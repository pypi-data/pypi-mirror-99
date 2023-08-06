import os

import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='django-docker-entrypoint',  # Replace with package name
    version=os.environ.get('VERSION', '0.0.0'),
    author='a.Signz',
    author_email='a.Signz089@googlemail.com',
    description='Django docker entrypoint',
    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    long_description=long_description,
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    # url='https://github.com/pypa/sampleproject',
    python_requires='>=3.6',
)
