from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name = 'fast_layers',
    packages = ['fast-layers'],
    version = '0.0.1',  
    license = 'MIT',
    description = 'Fast-Layers is a python library for Keras and Tensorflow users: The fastest way to build complex deep neural network architectures with sequential models',
    author = 'Alexandre Mahdhaoui',
    author_email = 'alexandre.mahdhaoui@gmail.com',
    url = 'https://github.com/AlexandreMahdhaoui/fast-layers',
    download_url = 'https://github.com/AlexandreMahdhaoui/fast-layers.git',
    keywords = ['keras', 'tensorflow'],
    classifiers = [],
    install_requires = [
        'tensorflow'
    ],
    long_description = long_description,
    long_description_content_type = 'text/markdown',
)