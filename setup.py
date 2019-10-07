from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='proglove',
    version='0.2.0',
    description='proglove, proto_lab',
    long_description=readme,
    author='proto_lab',
    author_email='kontakt@proto-lab.de',
    url='http://protolab-rosenheim.de/',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')), install_requires=['configparser', 'opcua-widgets', 'pyserial']
)
