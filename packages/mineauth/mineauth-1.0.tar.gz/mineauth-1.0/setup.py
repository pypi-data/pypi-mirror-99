from distutils.core import setup
setup(
  name = 'mineauth',         # How you named your package folder (MyLib)
  packages = ['mineauth'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Minecraft authentication API wrapper',   # Give a short description about your library
  author = 'Foster Reichert',                   # Type in your name
  author_email = 'fosterhreichert@gmail.com',      # Type in your E-Mail
  install_requires=[            # I get to this in a second
          'requests',
      ]
)
