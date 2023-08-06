from setuptools import setup, find_packages

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setup(
    name='eGUI',
    version='0.0.7',
    keywords='Python',
    description='基于Python的GUI界面，函数使用中文命名，使用简单，界面丰富，上手方便，持续更新。',
    license='MIT License',
    url='https://space.bilibili.com/365335499',
    author='Python生态',
    author_email='3157024351@qq.com',
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'PySimpleGUI~=4.37.0',
    ],
)
