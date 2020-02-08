from distutils.core import setup

setup(
  name='abm',
  description='Allow loading non Python module formats as modules',
  version='0.2.0',
  author='Salvador de la Puente González',
  author_email='salva@unoyunodiez.com',
  url='https://github.com/delapuente/abm',
  packages=('abm', 'abm.loaders'),
  long_description=open('README.rst').read(),
  keywords=['abstract', 'module', 'import'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries'
  ]
)
