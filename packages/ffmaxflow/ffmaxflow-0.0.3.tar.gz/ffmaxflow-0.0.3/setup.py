from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ffmaxflow',
  version='0.0.3',
  description='Implementation of the  Fork Fulkerson method to find the max posible flow of a network',
  #long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Equipo 2',
  author_email='a@b.c',
  license='MIT', 
  classifiers=classifiers,
  keywords='max flow',
  packages=find_packages(),
  install_requires=['collections-extended'] 
)
