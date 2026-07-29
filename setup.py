from setuptools import setup, find_packages

setup(
    name='third_party_services',
    version='0.1.8',
    author='Sunday Deogratias',
    author_email='sundaydeogratias8@gmail.com',
    description='A wrapper package for YTL external services',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/iras-test/third_party_services',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'Django',
        'djangorestframework',
        'urllib3'

    ],
)
