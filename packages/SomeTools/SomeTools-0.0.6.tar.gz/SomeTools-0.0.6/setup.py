from setuptools import setup
from setuptools import find_packages

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='SomeTools',
      version='0.0.6',
      description="Some python tools",
      author="zhangkun",
      author_email="zk.kyle@foxmail.com",
      project_urls={
          'Documentation': 'https://github.com/584807419/SomeTools',
          'Funding': 'https://github.com/584807419/SomeTools',
          'Source': 'https://github.com/584807419/SomeTools',
          'Tracker': 'https://github.com/584807419/SomeTools',
      },
      keywords=("Python", "Tools"),
      license='',
      long_description=long_description,  # 包的详细介绍，一般在README.md文件内
      long_description_content_type="text/markdown",
      url="https://pypi.org/project/SomeTools/",  # 自己项目地址，比如github的项目地址
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',  # 对python的最低版本要求
      packages=find_packages(),
      install_requires=[
          "datetime",
          "loguru",  # 高效优雅的日志显示
          # "orjson",  # 底层使用了rust，Python下最快的json库,比 ujson 快 3 倍，比 json 快 6 倍
      ],
      py_modules=['sometools'],
      include_package_data=True,
      platforms="any",
      scripts=[],
      )
# python setup.py sdist bdist_wheel
# python -m twine upload --repository pypi dist/*
# pip install SomeTools -i https://pypi.python.org/simple
