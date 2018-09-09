from distutils.code import setup

setup(
  name='abm',
  description='Allow loading non Python module formats as modules',
  version='0.1.0',
  author='Salvador de la Puente González',
  author_email='salva@unoyunodiez.com',
  url='https://github.com/delapuente/abm',
  packages=['abm'],
  long_description=open('README').read(),
  keywords=['abstract', 'module', 'import'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries'
  ]
)
