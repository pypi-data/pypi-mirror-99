from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='skyiris',
  version='0.0.6',
  description='machine leanring with iris_dataset',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='SkyKang',
  author_email='godsky@naver.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='skyiris', 
  packages=find_packages(),
  install_requires=[''] 
)