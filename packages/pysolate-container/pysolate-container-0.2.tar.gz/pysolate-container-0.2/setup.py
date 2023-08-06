from setuptools import setup, find_packages

setup(
    name='pysolate-container',
    version='0.2',
    packages=find_packages(),
    url='',
    license='MIT',
    author="Keane O'Kelley",
    author_email='keane.m.okelley@gmail.com',
    description='',
    install_requires=[
        'colorful'
    ],
    entry_points={
        'console_scripts': [
            'c=pysolate.cli:main',
            'pysolate=pysolate.cli:main',
        ]
    },
)
