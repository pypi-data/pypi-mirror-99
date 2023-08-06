import os

from setuptools import setup

current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except OSError:
    long_description = ''

setup(name='lbk-cli',
      packages=[
          'lbk'
      ],
      version='0.1.4',
      license='MIT',
      description='Terminal client for Logbook',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Marcel Härle',
      author_email='marcel.haerle@sonnvest.de',
      url='https://github.com/sonnvest/lbk-client',
      keywords='Logbook, cli',
      install_requires=[
          'halo'
      ],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Documentation'
      ],
      entry_points={
          'console_scripts': ['lbk = lbk.client:main']
      })
