# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="gobbletgobblers.py",
    packages=["gobbletgobblers"],

    version="1.0.1",

    author="Aomi Vel / 碧海ベル",

    url='https://github.com/Req-kun/gobbletgobblers.py',

    description='有名ボドゲ、ゴブレットゴブラーズをPythonで使用可能にしたもの',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='gobbletgobblers gobblet gobblers',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)