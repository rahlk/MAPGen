try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'descriptiom': 'Memetic Algorithms for Configuring Large Scale Software Product Lines',
	'author': 'Rahul Krishna',
	'url': 'https://goo.gl/0Q7I2I',
	'download_url': 'https://goo.gl/1rzR7g',
	'author_email': 'i.m.ralk@gmail.com',
	'version':'0.1',
	'install_requires': ['nose'],
	'packages': ['memeSAT'],
	'scripts': [],
	'name': 'memeSAT'
}

setup(**config)
	
