from setuptools import setup, find_packages

setup(
  name = 'egnn-pytorch',
  packages = find_packages(),
  version = '0.0.32',
  license='MIT',
  description = 'E(n)-Equivariant Graph Neural Network - Pytorch',
  author = 'Phil Wang, Eric Alcaide',
  author_email = 'lucidrains@gmail.com',
  url = 'https://github.com/lucidrains/egnn-pytorch',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'equivariance',
    'graph neural network'
  ],
  install_requires=[
    'einops>=0.3',
    'torch>=1.6', 
    'torch-scatter',
    'torch-sparse',
    'torch-cluster',
    'torch-spline-conv',
    'torch-geometric'
  ],
  setup_requires=[
    'pytest-runner',
  ],
  tests_require=[
    'pytest'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
