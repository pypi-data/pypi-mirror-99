from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='kerfex',
    version='0.0.1',
    url='https://github.com/caiocarneloz/kerfex',
    license='MIT License',
    author='Caio Carneloz',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='caiocarneloz@gmail.com',
    keywords=['keras', 'feature-extraction', 'CNN', 'Imagenet'],
    description=u'Generic feature extraction using keras pre-built CNN\'s with imagenet weights.',
    packages=['kerfex'],
    install_requires=['pandas', 'numpy', 'keras', 'tensorflow', 'sklearn'],)