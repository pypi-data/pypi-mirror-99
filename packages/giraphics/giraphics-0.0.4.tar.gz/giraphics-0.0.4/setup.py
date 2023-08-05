from distutils.core import setup
setup(
  name = 'giraphics',
  version = '0.0.4',
  license='MIT',
  package_dir={'':'src'},
  description = 'Lightweight graphing and animations',
  author = 'T. G. Hiranandani',
  author_email = 'src@protonmail.com',
  url = 'https://github.com/tghira/giraphics',
  keywords = ['graphs', 'animations', 'graphics', 'vector-graphics'],
  install_requires=[
          'numpy',
          'IPython'
      ],

  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Scientific/Engineering :: Astronomy",
    "Topic :: Scientific/Engineering :: Physics"]
)