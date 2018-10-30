#!usr/bin/env python
# -*- coding: utf -*-

setup(
    name='psync',
    version='1.0.0',
    description='CLI para sincronização automática de arquivos e diretórios - Computação@UFCG',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    author='Héricles Emanuel',
    author_email='hericles.me@gmail.com',
    url='https://github.com/P-Sync/P-Sync',
    packages=['psync'],
    install_requires=['hashlib', 'zlib', 'collections', 'struct', 'pyrebase', 'argparse']
)