import os
import setuptools
from datetime import datetime

DESCRIPTION = 'my utils'
here = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().split()


setuptools.setup(
    name='my_utils',
    version=datetime.now().strftime('%Y%m%d'),
    author='Miles',
    author_email='15070926843@163.com',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wlccgp3/my_utils.git',
    packages=setuptools.find_packages(exclude=('tests', 'temp')),
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
