from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT='-e .'

def get_requirements(file_path:str)->List[str]:
    " This Function Will Return List of Requirements"
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","")for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)


setup(
name='Student Performance Measure',
version='0.0.1',
author='Nitin',
author_email='itsnits333@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
)