from setuptools import setup, find_packages
import re

required = [l.strip() for l in
            open('requirements.txt') if re.match('^[a-z]', l)]

setup(
    name='maintenance_api',

    description='A simple maintenance api',

    # The project's main homepage.
    url='https://github.com/srleyva/TDD-Python',

    # Author details
    author='Stephen Leyva',
    author_email='sleyva1297@gmail.com',
    license='MIT',

    version='0.2.0',
    zip_safe=True,

    install_requires=required,
    packages=find_packages(exclude=['tests']),
    entry_points={'console_scripts': ['mapi=maintenance_api:main']}
)
