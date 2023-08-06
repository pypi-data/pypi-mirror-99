import setuptools

with open('README.md', 'r') as file:
	long_description = file.read()


setuptools.setup(
	name = 'text_hammer', #this should be unique,
	version = '0.1.4',
	include_package_data=True,
	author = 'Abhishek Jaiswal',
	author_email = 'abhishek.jaiswal26102001@gmail.com',
	description = 'This is text preprocessing package',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	packages = setuptools.find_packages(),
	install_requires = ['beautifulsoup4==4.9.1','pandas','numpy','spacy','TextBlob'],
	license = 'Apache License 2.0'
	)
