from distutils.core import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'mineauth',         # How you named your package folder (MyLib)
  packages = ['mineauth'],   # Chose the same as "name"
  version = '1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Minecraft authentication API wrapper',   # Give a short description about your library
  long_description=long_description,
  author = 'Foster Reichert',                   # Type in your name
  author_email = 'fosterhreichert@gmail.com',      # Type in your E-Mail
  install_requires=[            # I get to this in a second
          'requests',
      ]
)
