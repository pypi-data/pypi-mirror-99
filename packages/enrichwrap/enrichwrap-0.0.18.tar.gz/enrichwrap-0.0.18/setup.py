from importlib.resources import read_text

from setuptools import setup, find_packages
import pathlib

with open("README.md", "r", encoding="utf-8") as fh:
      long_description = fh.read()

here = pathlib.Path(__file__).parent.resolve()

setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install sampleproject
    #
    # And where it will live on PyPI: https://pypi.org/project/file-parsing-sample/
    #
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    name="enrichwrap",

      version='0.0.18',
      description="A small package testing calling out to third party enrichment", # Optional
      long_description=long_description,  # Optional
      long_description_content_type='text/markdown',  # Optional (see note above)
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Text Processing :: Linguistic',
      ],
      keywords='enrichment',
      url='http://github.com/suhens/enrichwrap',
      author='Sue Hannum',
      author_email='Sue.Hannum@sas.com',
      license='MIT',
      packages=['enrichwrap'],
      install_requires=[
            'markdown',
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/enrichwrap'],
      entry_points={
            'console_scripts': ['enrichmain=enrichwrap.command_line:main'],
      }
      )

