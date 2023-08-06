# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/23
from distutils.core import setup

from setuptools import find_packages

with open('./yqn_project_cli/README.md') as reader:
    long_description = reader.read()

if __name__ == '__main__':
    setup(
        name='yqn_project_cli',
        version='0.0.0rc43',
        author='ZouKaihua',
        author_email="zoukaihua@aliyun.com",
        description='for more faster to create flask project',
        url='https://blog.zoukaihua.com',
        long_description=long_description,
        long_description_content_type="text/markdown",
        include_package_data=True,
        package_data={'yqn_project_cli': ['template/*', 'template/*/*', 'README.md']},
        packages=find_packages(),
        install_requires=[
            'DBUtils>=2.0',
            'Flask>=1.1.2',
            'Flask-Compress>=1.8.0',
            'Flask-Cors>=3.0.10',
            'flask-restx>=0.2.0',
            'PyMySQL>=1.0.2',
            'pyodps>=0.10.6',
            'requests>=2.25.1',
            'requests-toolbelt>=0.9.1',
            'termcolor>=1.1.0',
        ],
        entry_points={
            'console_scripts': [
                'yqn-project = yqn_project_cli.init_project:main',
                'yqn-handler = yqn_project_cli.init_project:auto_handler',
            ],
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
