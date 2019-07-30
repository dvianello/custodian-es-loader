from setuptools import setup

setup(name="custodian-es-loader",
      version='0.1',
      py_modules=['custodian-es-loader'],
      entry_points={'console_scripts': ['c7n-es-loader=custodian_es_loader.cli:main']},
      install_requires=['Click', 'smart_open'])
