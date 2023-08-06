from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
	name='headerbreakdown',
	version='0.1.1',
	author='James Bonifield',
	author_email='bonifield.tools@gmail.com',
	description='flattens a collection of HTTP headers into a JSON structure for automated analysis',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/bonifield/HeaderBreakdown/',
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	py_modules=["headerbreakdown"]
)