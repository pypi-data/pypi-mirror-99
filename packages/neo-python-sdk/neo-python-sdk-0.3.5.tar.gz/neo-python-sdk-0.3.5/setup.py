
from distutils.core import setup
setup(
  name = 'neo-python-sdk',
  packages = ['neo-python-sdk'],
  version = '0.3.5',
  python_requires='>=3.5',
  license='	apache-2.0',
  description = 'Neo SDK for Python with some additional libraries to support the development of Neo Sentinels (NSX).',
  author = 'Jan-Eric Gaidusch <Neohelden GmbH>',
  url = 'https://github.com/neohelden/neo-python-sdk',
  keywords = ['neohelden', 'neo', 'neo-sdk'],
  install_requires=[            # I get to this in a second
          'python>=3.5',
          'asyncio-nats-client==0.10.0',
          'asyncio==3.4.3',
          'sentry-sdk==1.0.0'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)