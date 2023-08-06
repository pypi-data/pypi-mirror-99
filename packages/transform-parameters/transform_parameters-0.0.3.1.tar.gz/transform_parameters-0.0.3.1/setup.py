import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name='transform_parameters',
  version='0.0.3.1',
  author='Rogério Ferreira',
  author_email='rogeroficial1506@gmail.com',
  description='Small transformation package to specific project',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url="https://github.com/rogerzs/libraries",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  
  ],
  python_requires='>=3.6',
)
