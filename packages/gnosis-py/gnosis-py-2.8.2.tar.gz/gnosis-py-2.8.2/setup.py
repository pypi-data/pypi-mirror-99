import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requirements = [
    "cached-property>=1.5.1",
    "django>=2",
    "django-filter>=2",
    "ethereum>=2.3.2",
    "packaging",
    "py-eth-sig-utils>=0.3.0",
    "requests>=2",
    "web3>=5",
]

setup(
    name='gnosis-py',
    version='2.8.2',
    packages=find_packages(),
    package_data={'gnosis': ['py.typed']},
    install_requires=requirements,
    include_package_data=True,
    license='MIT License',
    description='Gnosis libraries for Python Projects',
    long_description=README,
    url='https://github.com/gnosis/gnosis-py',
    author='Uxío',
    author_email='uxio@gnosis.pm',
    keywords=['ethereum', 'django', 'rest', 'gnosis'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
