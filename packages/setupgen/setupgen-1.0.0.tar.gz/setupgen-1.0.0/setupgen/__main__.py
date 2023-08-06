import sys
import os

if sys.argv[1] == 'require':
    setup = f'''
from setuptools import setup

setup(
    name='{os.environ['setup_name']}',
    version='{os.environ['setup_version']}',
    description='{os.environ['setupdesc']}',
    long_description='{os.environ['setuplongdesc']}',
    install_requires=[{os.environ['requirements']}],
    packages=[{os.environ['packages']}]
    )
'''
    print(setup)

if sys.argv[1] == 'norequire':
    setup = f'''
from setuptools import setup

setup(
    name='{os.environ['setup_name']}',
    version='{os.environ['setup_version']}',
    description='{os.environ['setupdesc']}',
    long_description='{os.environ['setuplongdesc']}',
    packages=[{os.environ['packages']}]
    )
'''
    print(setup)

if sys.argv[1] == '--help':
    conditions = [
        sys.argv[2] != 'windows',
        sys.argv[2] != 'linux'
        ]
    if all(conditions):
        print('Usage: --help [windows, linux]')
    if sys.argv[2] == 'windows':
        print('''
Example 1 (Package with requirements):

set setup_name=mypackage
set setup_version=1.0.0
set setupdesc=Test
set setuplongdesc=open('README.txt').read()
set packages="one", "two"
set requirments="flask", "pyautogui"

python -m setupgen require > setup.py

Example 2 (Package with no requirements):

set setup_name=mypackage
set setup_version=1.0.0
set setupdesc=Test
set setuplongdesc=open('README.txt').read()
set packages="one", "two"

python -m setupgen norequire > setup.py

Example 3 (Using .scfg files to manage prexisting projects):

In the .scfg, it should look like (note, this is only for windows):

setup_name=mypackage
setup_version=1.0.0
setupdesc=Test
setuplongdesc=open('README.txt').read()
packages="one", "two"
requirments="flask", "pyautogui"

Here is how to install one:

for /f "tokens=*" %i in ('type file_name.scfg') DO set %i
python -m setupgen require/norequire here > setup.py


''')
    if sys.argv[2] == 'linux':
        print('''
Example 1 (Package with requirements):

export setup_name='mypackage'
export setup_version='1.0.0'
export setupdesc='Test'
export setuplongdesc=open('README.txt').read()
export packages='"one", "two"'
export requirments='"flask", "pyautogui"'

python -m setupgen require > setup.py

Example 2 (Package with no requirements):

export setup_name='mypackage'
export setup_version='1.0.0'
export setupdesc='Test'
export setuplongdesc='open('README.txt').read()'
export packages='"one", "two"'

python -m setupgen norequire > setup.py
'''
      )        

              


        
    
    
