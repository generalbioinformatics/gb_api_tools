from setuptools import setup, find_packages

setup(
    name='gb_api_tools',
    version='0.0.1',
    python_requires='>=3.6',
    packages=find_packages(include=["gb_api_tools", "gb_api_tools.*"]),
    author_email='michael.way@generalbioinformatics.com',
    license_files = ('LICENSE.txt'),
    install_requires=[
        'pandas>=1.1.5',
        'requests>=2.26.0',
        'openpyxl>=3.0.0',
        'biopython>=1.79',
        'ratelimit',
        'backoff'
        ],
    include_package_data=True
    )
