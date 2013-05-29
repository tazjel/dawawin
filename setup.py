#!/usr/bin/python

from distutils.core import setup
from glob import glob


doc_files  = ['LICENSE-ar.txt', 'LICENSE-en', 'AUTHORS', 'ChangeLog', 'README', 'TODO']
data_files = [('share/applications/', ['dawawin.desktop']),
              ('share/icons/hicolor/scalable/apps', ['dawawin.svg']),
              ('share/doc/dawawin', doc_files),
	      ('share/dawawin/dawawin-data/icons', glob('dawawin-data/icons/*.png')),
              ('share/dawawin/dawawin-data/', ['dawawin-data/Help.db']),
	      ('share/icons/hicolor/22x22/actions', glob('dawawin-data/player-icons/*')),
              ('share/icons/hicolor/16x16/apps/', ['dawawin-data/hicolor/16x16/apps/dawawin.png']),
              ('share/icons/hicolor/22x22/apps/', ['dawawin-data/hicolor/22x22/apps/dawawin.png']),
              ('share/icons/hicolor/24x24/apps/', ['dawawin-data/hicolor/24x24/apps/dawawin.png']),
              ('share/icons/hicolor/32x32/apps/', ['dawawin-data/hicolor/32x32/apps/dawawin.png']),
              ('share/icons/hicolor/36x36/apps/', ['dawawin-data/hicolor/36x36/apps/dawawin.png']),
              ('share/icons/hicolor/48x48/apps/', ['dawawin-data/hicolor/48x48/apps/dawawin.png']),
              ('share/icons/hicolor/64x64/apps/', ['dawawin-data/hicolor/64x64/apps/dawawin.png']),
              ('share/icons/hicolor/72x72/apps/', ['dawawin-data/hicolor/72x72/apps/dawawin.png']),
              ('share/icons/hicolor/96x96/apps/', ['dawawin-data/hicolor/96x96/apps/dawawin.png']),
              ('share/icons/hicolor/128x128/apps/',['dawawin-data/hicolor/128x128/apps/dawawin.png']),
	      ('share/fonts/dawawin', glob('dawawin-data/fonts/*.*')),
              ]

setup(
      name="Dawawin",
      description='poetry of arab',
      long_description='poetry of arab',
      version="0.1.20",
      author='Ahmed Raghdi',
      author_email='asmaaarab@gmail.com',
      url="http://linuxac.org",
      license='Waqf License',
      platforms='Linux',
      scripts=['dawawin'],
      keywords=['poem', 'poet', 'arab', 'poetry'],
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: POSIX :: Linux',
          'Development Status :: 4 - Beta',
          'Environment :: X11 Applications :: Gtk',
          'Natural Language :: Arabic',
          'Intended Audience :: End Users/Desktop',
          'Topic :: Desktop Environment :: Gnome',
			],
      packages=['Dawawin'],
      data_files=data_files
      )
