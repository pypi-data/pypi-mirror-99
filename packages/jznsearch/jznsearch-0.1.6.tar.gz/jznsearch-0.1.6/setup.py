import pathlib
from setuptools import setup
from jznsearch.version import VERSION

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='jznsearch',
    version=VERSION,
    description='Simple search in JSON files',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/jsanotheraccount/jznsearch',
    author='Jane Skvortsova',
    author_email='jane.skvortsova@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['jznsearch'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'jznsearch=jznsearch:main',
        ]
    },
)
