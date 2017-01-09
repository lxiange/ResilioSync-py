
from setuptools import setup, find_packages


version = '0.1'

setup(name='resiliosync',
      version=version,
      description="A Python API client for Resilio Sync",
      long_description=open('readme.md').read(),
      classifiers=[
          'Intended Audience :: Developers',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
      ],
      keywords='api resilio sync',
      author='Shawn Lee',
      author_email='lxiange@gmail.com',
      url='https://github.com/lxiange/ResilioSync-py',
      license='MIT',
      packages=find_packages(exclude=['test']),
      data_files=[('.', ['requirements.txt', 'readme.md', 'LICENSE'])],
      include_package_data=True,
      zip_safe=False,
      install_requires=open('requirements.txt').readlines(),
      entry_points={},
      )
