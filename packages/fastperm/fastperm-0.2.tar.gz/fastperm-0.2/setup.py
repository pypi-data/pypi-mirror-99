from setuptools import setup

def parse_requirements(filename):
	lines = (line.strip() for line in open(filename))
	return [line for line in lines if line and not line.startswith("#")]

setup(name='fastperm',
        version='0.2',
        description='Package for online generation of large permutations without large upfront cost.',
        url='http://github.com/adityaramesh/fastperm',
        author='Aditya Ramesh',
        author_email='_@adityaramesh.com',
        license='BSD',
        packages=['fastperm'],
        install_requires=parse_requirements('requirements.txt'),
        zip_safe=True)
