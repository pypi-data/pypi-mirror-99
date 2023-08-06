from distutils.core import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'pypi_test_pkg_jhjoh',          
  version = '0.0.3',      
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository 
  author = 'Joakim Johansen',
  description="Test package by jhjoh",
  long_description=long_description,
  long_description_content_type="text/markdown",                   
  author_email = 'jhjoh@equinor.com',      
  url = 'https://github.com/JoakimJohansen/pypi-package-test',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/JoakimJohansen/pypi-package-test/archive/refs/tags/v_003.tar.gz',    
  keywords = ['TEST', 'PYPI'],   
  install_requires=[            
          'numpy',
  ],
  classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
  ],
  package_dir={"": "pypi_test_pkg"},
  packages=setuptools.find_packages(where="pypi_test_pkg"),
  python_requires=">=3.6",
)