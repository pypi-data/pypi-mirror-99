from setuptools import setup

setup(
	name='rest-oc',
	version='0.7.8',
	url='https://github.com/ouroboroscoding/rest-oc-python',
	description='RestOC is a library of python 3 modules for rapidly setting up REST microservices.',
	keywords=['rest','microservices'],
	author='Chris Nasr - OuroborosCoding',
	author_email='ouroboroscode@gmail.com',
	license='Apache-2.0',
	packages=['RestOC'],
	install_requires=[
		'arrow==0.17.0',
		'bottle==0.12.19',
		'format-oc==1.5.12',
		'gunicorn==20.0.4',
		'hiredis==1.1.0',
		'Jinja2==2.11.2',
		'pdfkit==0.6.1',
		'Pillow==8.0.1',
		'PyMySQL==0.10.1',
		'redis==3.5.3',
		'requests==2.25.0',
		'rethinkdb==2.4.7'
	],
	zip_safe=True
)
