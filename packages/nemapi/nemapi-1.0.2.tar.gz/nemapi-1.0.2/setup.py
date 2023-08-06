import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

setup(
    name="nemapi",
    version="1.0.2",
    url="", #package url
    license='MIT',

    author="Jonathon Emerick",
    author_email="jonathon.emerick@uq.net.au",

    description="Access to public National Electricity Market data through nemmarket API.",
    long_description=README,
    long_description_content_type="text/markdown",

    packages=find_packages(exclude=('tests','examples')),

    install_requires=['datetime', 'requests', 'pandas'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)