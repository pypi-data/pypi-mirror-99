from distutils.core import setup
setup(
  name = 'powerx_energy_api',      
  packages = ['powerx_energy_api'],
  version = '0.2',
  license='MIT',
  description = 'Powerx Energy API Wrapper',
  author = 'powerx',
  author_email = 'admin@powerx.co',
  url = 'https://github.com/user/reponame',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['PowerX'],
  install_requires=[ 
          'requests==2.25.1'
      ],
  classifiers=[
    'Programming Language :: Python :: 3'
  ],
)