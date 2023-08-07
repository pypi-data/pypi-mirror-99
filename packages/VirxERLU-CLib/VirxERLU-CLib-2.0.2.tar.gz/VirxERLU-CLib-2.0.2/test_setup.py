from setuptools import setup, Extension

module = Extension('ctest', sources=['test.c'])

setup(name='ctest',
      version='1',
      description='tests',
      long_description="C tests",
      ext_modules=[module],
      license="MIT",
      author='VirxEC',
      author_email='virx@virxcase.dev',
      url="https://github.com/VirxEC/VirxERLU",
      python_requires='>=3.7'
      )
