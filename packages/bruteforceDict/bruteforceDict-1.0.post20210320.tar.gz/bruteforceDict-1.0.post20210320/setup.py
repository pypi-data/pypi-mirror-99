from setuptools import setup
with open("README.md", "r") as fh:
	long_description = fh.read()
setup(name='bruteforceDict',
      version='1.0',
      description='Bruteforce to file, to array',
      long_description=long_description,
      packages=['bruteforceDict'],
      author_email='yura@anisimoff.tel',
      zip_safe=False)