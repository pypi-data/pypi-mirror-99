from setuptools import setup
from setuptools import find_namespace_packages
from typing import List


def requirements() -> List[str]:
    with open('requirements.txt', 'r') as file_handler:
        package_list = file_handler.readlines()
        package_list = [package.rstrip() for package in package_list]

    return package_list


setup(
    name='aws.paramstore',
    description='Parameter Store class that allows dict-like access.',

    version='1.0.1',

    install_requires=requirements(),
    packages=find_namespace_packages(include=[
        "aws.*",
    ]),
    python_requires='>=3.7'
)
