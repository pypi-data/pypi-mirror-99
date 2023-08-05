import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
	name="clickboxer-watertracker",
	version="0.0.1",
	description="An API server for the watertracker app",
	long_description=README,
	long_description_content_type="text/markdown",
	url="https://github.com/dotslashbin/py-waterlogger-api",
	author="Joshua Fuentes",
	author_email="joshuarpf@gmail.com",
	license="MIT",
	classifiers=[
			"License :: OSI Approved :: MIT License",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.9",
	],
	# packages=["jotest"],
	include_package_data=True,
	# install_requires=["feedparser", "html2text"],
	# entry_points={
	# 		"console_scripts": [
	# 				"jotest=jotest.__main__:main",
	# 		]
	# },
)