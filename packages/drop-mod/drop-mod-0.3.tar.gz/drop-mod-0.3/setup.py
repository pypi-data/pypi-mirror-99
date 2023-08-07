from setuptools import setup
from drop import __version__

with open('requirements.txt', 'r', encoding='utf-8') as f:
    install_requires = [line for line in f.read().splitlines() if len(line) > 0]

setup(name='drop-mod',
      version=__version__,
      description='A Python moderation toolkit built for chat bots',
      url='https://github.com/AtlasC0R3/drop-moderation',
      author='atlas_core',
      license='Apache 2.0',
      install_requires=install_requires,
      packages=['drop'],
      python_requires=">=3.7",
      zip_safe=True)
