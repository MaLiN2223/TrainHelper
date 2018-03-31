from setuptools import setup, find_packages

with open("requirements-tests.txt", 'r') as f:
    test_requirements = f.read().split('\n')

with open("requirements.txt", 'r') as f:
    requirements = f.read().split('\n')

setup(
    name='TrainHelper',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/MaLiN2223/TrainHelper',
    license='MIT',
    author_email='',
    description='',
    install_requires=requirements,
    setup_requires=test_requirements,
    tests_require=test_requirements,
)
