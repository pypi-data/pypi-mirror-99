from distutils.core import setup
setup(
  name = 'prettyGraphics',         
  packages = ['prettyGraphics'],   
  version = '1.0',      
  license='MIT',        
  description = 'All sorts of tables and graphics for console (for now just tables)',   
  author = 'Benjamin Ramirez',                   
  author_email = 'chilerito12@gmail.com',      
  url = 'https://github.com/Kyostenas/prettyGraphics',   
  download_url = 'https://github.com/Kyostenas/prettyGraphics/archive/v1.0-beta.1.tar.gz',    
  keywords = ['console', 'graphics'],   
  install_requires=[ 
      'nltk'
      'prettyTables'         
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)