from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='nullbytes',
  version='1.0.0',
  description='The API used to connect to the Null-Bytes Databases for CRUD operations',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://nullbytes.pythonanywhere.com/',  
  author='Codejapoe',
  author_email='codejapoe@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='api', 
  packages=find_packages(),
  install_requires=['requests'] 
)