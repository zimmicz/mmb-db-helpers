import setuptools

setuptools.setup(name='mmb_db_helpers',
      version='0.1',
      description='mapmybook database helpers',
      url='http://github.com/zimmicz/map-my-book-db-helpers',
      author='Michal Zimmermann',
      author_email='zimmi@tutanota.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=['flask', 'psycopg2'],
      zip_safe=False)

