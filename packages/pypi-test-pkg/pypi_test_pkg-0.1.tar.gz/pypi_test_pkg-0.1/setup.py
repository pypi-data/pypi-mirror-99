from distutils.core import setup
setup(
  name = 'pypi_test_pkg',         
  packages = ['pypi_test_pkg'],  
  version = '0.1',      
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Test package',   
  author = 'Joakim Johansen',                   
  author_email = 'jhjoh@equinor.com',      
  url = 'https://github.com/JoakimJohansen/pypi-package-test',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/JoakimJohansen/pypi-package-test/archive/refs/tags/v_01.tar.gz',    
  keywords = ['TEST', 'PYPI'],   
  install_requires=[            
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)