import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='cassiopeia',
    version='1.0.0',
    url='',
    license='BSD',
    maintainer='Cassiopeia team',
    maintainer_email='',
    description='CS467 Capstone Project.',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)