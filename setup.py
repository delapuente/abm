from distutils.core import setup

setup(
  name='abm',
  description='Allow loading non Python module formats as modules',
  version='0.1.1',
  author='Salvador de la Puente González',
  author_email='salva@unoyunodiez.com',
  url='https://github.com/delapuente/abm',
  packages=['abm'],
  long_description=open('README.rst').read(),
  keywords=['abstract', 'module', 'import'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries'
  ]
)
