from setuptools import setup, Extension

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='fast_layers',
    packages=['fast_layers'],
    version='0.1.4',
    license='MIT',
    description='Fast-Layers is a python library for Keras and Tensorflow users: The fastest way to build complex deep neural network architectures with sequential models',
    author='Alexandre Mahdhaoui',
    author_email='alexandre.mahdhaoui@gmail.com',
    url='https://github.com/AlexandreMahdhaoui/fast-layers',
    download_url='https://github.com/AlexandreMahdhaoui/fast-layers.git',
    keywords=['keras', 'tensorflow'],
    classifiers=[],
    install_requires=[
        'tensorflow'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
