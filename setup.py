from setuptools import setup, find_packages

setup(name='python-busgokr',
      version='0.0.1',
      description='Python Module to access the bus.go.kr API',
      author='izolight',
      author_email='izolight@gmail.com',
      url='https://github.com/izolight/python-busgokr',
      packages=find_packages(), requires=['requests']
      )