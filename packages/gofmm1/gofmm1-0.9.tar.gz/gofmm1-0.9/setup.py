# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56

from distutils.core import setup
setup(
  name = 'gofmm1',         # How you named your package folder (MyLib)
  packages = ['gofmm1'],   # Chose the same as "name"
  version = '0.9',      # Start with a small number and increase it with every change you make
  license='TUM',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
  author = 'Tianyi Ge',                   # Type in your name
  author_email = 'tianyi.ge@tum.de',      # Type in your E-Mail
  url = 'https://github.com/doernermannT/gofmm',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/doernermannT/gofmm/archive/master.zip',    # I explain this later on
  keywords = ['gofmm', 'swig', 'KDE'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',      #Specify which pyhton versions that you want to support
  ],
)
