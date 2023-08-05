from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='gravity_interface',
    version='1.42',
    packages=find_packages(),
    author='PunchyArchy',
    author_email='ksmdrmvscthny@gmail.com',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    include_package_data=True,
    install_requires=[
        'pillow',
        'pypiwin32',
        'pyscreenshot',
        'tkcalendar'
    ],
)