import pathlib
from setuptools import find_packages, setup

HERE=pathlib.Path(__file__).parent

VERSION='0.0.1'
PACKAGE_NAME='Random_Spanish_Words'
AUTHOR='Reydel Romeu Alonso'
AUTHOR_EMAIL='reydelromeu@gmail.com'
URL='https://github.com/08wwwxxxwww80'

LICENSE='MIT'
DESCRIPTION='Libreria para obtener palabras o listas de palabras en Español de forma aleatoria'
LONG_DESCRIPTION=(HERE/"README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE='text/markdown'


INSTALL_REQUIRES=[]

setup(
	name=PACKAGE_NAME,
	version=VERSION,
	description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	long_description_content_type=LONG_DESC_TYPE,
	author=AUTHOR,
	author_email=AUTHOR_EMAIL,
	url=URL,
	install_requires=INSTALL_REQUIRES,
	license=LICENSE,
	packages=find_packages(),
	include_package_data=True
	)
