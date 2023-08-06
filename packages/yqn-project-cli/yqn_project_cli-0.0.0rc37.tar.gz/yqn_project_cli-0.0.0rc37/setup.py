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
        version='0.0.0rc37',
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
            'aniso8601>=9.0.1',
            'bleach>=3.3.0',
            'Brotli>=1.0.9',
            'certifi>=2020.12.5',
            'cffi>=1.14.5',
            'chardet>=4.0.0',
            'click>=7.1.2',
            'colorama>=0.4.4',
            'cryptography>=3.4.6',
            'DBUtils>=2.0',
            'docutils>=0.16',
            'Flask>=1.1.2',
            'Flask-Compress>=1.8.0',
            'Flask-Cors>=3.0.10',
            'Flask-JSON>=0.3.4',
            'flask-restx>=0.2.0',
            'Flask-SQLAlchemy>=2.4.4',
            'idna>=2.10',
            'importlib-metadata>=3.7.3',
            'itsdangerous>=1.1.0',
            'jeepney>=0.6.0',
            'Jinja2>=2.11.3',
            'jsonschema>=2.6.0',
            'keyring>=23.0.0',
            'MarkupSafe>=1.1.1',
            'packaging>=20.9',
            'pika>=1.2.0',
            'pkginfo>=1.7.0',
            'pyasn1>=0.4.8',
            'pycparser>=2.20',
            'Pygments>=2.8.1',
            'PyMySQL>=1.0.2',
            'pyodps>=0.10.6',
            'pyparsing>=2.4.7',
            'pytz>=2021.1',
            'PyYAML>=5.4.1',
            'readme-renderer>=29.0',
            'redis>=3.5.3',
            'requests>=2.25.1',
            'requests-toolbelt>=0.9.1',
            'rfc3986>=1.4.0',
            'SecretStorage>=3.3.1',
            'six>=1.15.0',
            'SQLAlchemy>=1.3.23',
            'termcolor>=1.1.0',
            'tqdm>=4.59.0',
            'urllib3>=1.26.3',
            'webencodings>=0.5.1',
            'Werkzeug>=1.0.1',
            'zipp>=3.4.1',
        ],
        entry_points={
            'console_scripts': [
                'yqn-project = yqn_project_cli.init_project:main',
            ],
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
