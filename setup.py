from distutils.core import setup
import thefuckingweather

setup(name="thefuckingweather",
      version="1.0.1",
      description="Python API for The Fucking Weather",
      author="Ian Weller",
      author_email="ian@ianweller.org",
      url="http://repo.or.cz/w/python-thefuckingweather.git",
      py_modules=["thefuckingweather"],
      license="""\
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar
  14 rue de Plaisance, 75014 Paris, France
 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.

""",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: End Users/Desktop",
          "License :: Freely Distributable",
          "Operating System :: OS Independent",
          "Topic :: Utilities",
      ]
     )
