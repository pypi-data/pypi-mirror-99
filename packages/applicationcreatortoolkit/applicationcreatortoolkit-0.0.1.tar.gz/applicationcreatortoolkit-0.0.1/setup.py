from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='applicationcreatortoolkit',
  version='0.0.1',
  description='A GUI library built on top of tkinter',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Voltcharge 2021',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='gui', 
  packages=find_packages(),
  install_requires=[''] 
)