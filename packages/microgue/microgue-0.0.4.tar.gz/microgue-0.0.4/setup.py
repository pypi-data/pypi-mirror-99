from setuptools import setup, find_packages


setup(
    name='microgue',
    version='0.0.4',
    author='Michael Hudelson',
    author_email='michaelhudelson@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'flask',
        'flask-classful',
        'redis',
        'requests'
    ],
    python_requires=">=3.6",
)
